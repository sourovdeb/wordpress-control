<?php
/**
 * Plugin Name:  Sourov Category & Tag Auto-Fixer
 * Description:  Bulk-repair missing categories and tags on all posts. Auto-assigns based on content keywords.
 * Version:      1.1.0
 * Author:       Sourov Deb
 *
 * REST Endpoints (all require X-Sourov-Key header):
 *   GET  /wp-json/sourov/v1/preview-fixes         Preview what would be changed (dry run)
 *   POST /wp-json/sourov/v1/fix-posts             Bulk-fix all posts
 *   POST /wp-json/sourov/v1/fix-post/{id}         Fix one post by ID
 *
 * Set your API key under Settings > Sourov Fixer in wp-admin.
 */

if ( ! defined( 'ABSPATH' ) ) exit;

// ---------------------------------------------------------------------------
// REST API Registration
// ---------------------------------------------------------------------------
add_action( 'rest_api_init', function () {

    register_rest_route( 'sourov/v1', '/preview-fixes', [
        'methods'             => 'GET',
        'callback'            => 'sourov_preview_fixes',
        'permission_callback' => 'sourov_verify_api_key',
    ]);

    register_rest_route( 'sourov/v1', '/fix-posts', [
        'methods'             => 'POST',
        'callback'            => 'sourov_bulk_fix_posts',
        'permission_callback' => 'sourov_verify_api_key',
    ]);

    register_rest_route( 'sourov/v1', '/fix-post/(?P<id>\\d+)', [
        'methods'             => 'POST',
        'callback'            => 'sourov_fix_single_post',
        'permission_callback' => 'sourov_verify_api_key',
    ]);
});

function sourov_verify_api_key( $request ) {
    $provided = $request->get_header( 'X-Sourov-Key' );
    $expected = get_option( 'sourov_fixer_api_key', '' );
    return ! empty( $provided ) && $provided === $expected;
}

// ---------------------------------------------------------------------------
// Keyword rules
// ---------------------------------------------------------------------------
function sourov_category_rules() {
    return [
        'Grammar'               => ['grammar','tense','verb','noun','adjective','modal','syntax'],
        'Listening & Phonology' => ['listening','pronunciation','phonology','phoneme','intonation'],
        'Speaking & Fluency'    => ['speaking','fluency','conversation','oral','dialogue'],
        'Vocabulary'            => ['vocabulary','lexis','lexical','collocation','idiom'],
        'Reading Skills'        => ['reading','comprehension','skimming','scanning'],
        'Writing Skills'        => ['writing','essay','paragraph','composition'],
        'CELTA'                 => ['celta','teaching practice','lesson plan','trainee teacher'],
    ];
}

function sourov_tag_rules() {
    return [
        'grammar'       => 'grammar',
        'listening'     => 'listening',
        'speaking'      => 'speaking',
        'pronunciation' => 'pronunciation',
        'vocabulary'    => 'vocabulary',
        'celta'         => 'CELTA',
        ' elt '         => 'ELT',
        ' esl '         => 'ESL',
        ' efl '         => 'EFL',
        'fluency'       => 'fluency',
        'lesson plan'   => 'lesson plan',
        'teacher'       => 'teaching',
        'reading'       => 'reading',
        'writing'       => 'writing',
        'cambridge'     => 'Cambridge',
        'ielts'         => 'IELTS',
        'toefl'         => 'TOEFL',
        'classroom'     => 'classroom',
    ];
}

// ---------------------------------------------------------------------------
// Detection helpers
// ---------------------------------------------------------------------------
function sourov_detect_best_category( $title, $content ) {
    $text   = strtolower( wp_strip_all_tags( $title . ' ' . $content ) );
    $scores = [];

    foreach ( sourov_category_rules() as $cat => $keywords ) {
        $score = 0;
        foreach ( $keywords as $kw ) {
            $score += substr_count( $text, $kw );
        }
        if ( $score > 0 ) {
            $scores[ $cat ] = $score;
        }
    }

    if ( empty( $scores ) ) return 'ELT Masterclass';

    arsort( $scores );
    return array_key_first( $scores );
}

function sourov_detect_tags( $title, $content ) {
    $text = strtolower( wp_strip_all_tags( $title . ' ' . $content ) );
    $tags = [];

    foreach ( sourov_tag_rules() as $keyword => $tag ) {
        if ( false !== strpos( $text, $keyword ) ) {
            $tags[] = $tag;
        }
    }

    return array_unique( $tags );
}

// ---------------------------------------------------------------------------
// Core fix logic for a single post
// ---------------------------------------------------------------------------
function sourov_fix_post( $post_id, $dry_run = false ) {
    $post = get_post( $post_id );
    if ( ! $post ) return [ 'error' => 'Post not found', 'post_id' => $post_id ];

    $title   = $post->post_title;
    $content = $post->post_content;

    // Current state
    $current_cats = wp_get_post_categories( $post_id, [ 'fields' => 'names' ] );
    $current_tags = wp_get_post_tags( $post_id, [ 'fields' => 'names' ] );

    $needs_cat_fix  = empty( $current_cats ) ||
                      ( count( $current_cats ) === 1 && strtolower( $current_cats[0] ) === 'uncategorized' );
    $needs_tag_fix  = empty( $current_tags );

    $suggested_cat  = sourov_detect_best_category( $title, $content );
    $suggested_tags = sourov_detect_tags( $title, $content );

    $record = [
        'post_id'            => $post_id,
        'title'              => $title,
        'needs_category_fix' => $needs_cat_fix,
        'needs_tags_fix'     => $needs_tag_fix,
        'current_category'   => implode( ', ', $current_cats ) ?: 'None',
        'suggested_category' => $suggested_cat,
        'current_tags'       => $current_tags,
        'suggested_tags'     => $suggested_tags,
        'category_fixed'     => false,
        'tags_fixed'         => false,
    ];

    if ( ! $dry_run ) {
        if ( $needs_cat_fix ) {
            $cat_id = get_cat_ID( $suggested_cat );
            if ( ! $cat_id ) {
                $cat_id = wp_create_category( $suggested_cat );
            }
            if ( $cat_id && ! is_wp_error( $cat_id ) ) {
                wp_set_post_categories( $post_id, [ (int) $cat_id ] );
                $record['category_fixed'] = true;
            }
        }

        if ( $needs_tag_fix && ! empty( $suggested_tags ) ) {
            wp_set_post_tags( $post_id, $suggested_tags );
            $record['tags_fixed'] = true;
        }
    }

    return $record;
}

// ---------------------------------------------------------------------------
// REST callbacks
// ---------------------------------------------------------------------------
function sourov_preview_fixes( $request ) {
    $limit = max( 1, min( 500, (int) $request->get_param( 'limit' ) ?: 50 ) );

    $posts = get_posts([
        'numberposts' => $limit,
        'post_type'   => 'post',
        'post_status' => [ 'publish', 'draft', 'future' ],
    ]);

    $needs_fix = [];
    foreach ( $posts as $p ) {
        $r = sourov_fix_post( $p->ID, true );
        if ( $r['needs_category_fix'] || $r['needs_tags_fix'] ) {
            $needs_fix[] = $r;
        }
    }

    return new WP_REST_Response([
        'total_checked'     => count( $posts ),
        'posts_needing_fix' => count( $needs_fix ),
        'details'           => $needs_fix,
    ], 200 );
}

function sourov_bulk_fix_posts( $request ) {
    $limit   = max( 1, min( 500, (int) $request->get_param( 'limit' ) ?: 200 ) );
    $dry_run = $request->get_param( 'dry_run' ) === 'true';

    $posts = get_posts([
        'numberposts' => $limit,
        'post_type'   => 'post',
        'post_status' => [ 'publish', 'draft', 'future' ],
    ]);

    $results     = [];
    $fixed_count = 0;

    foreach ( $posts as $p ) {
        $r = sourov_fix_post( $p->ID, $dry_run );
        $results[] = $r;
        if ( $r['category_fixed'] || $r['tags_fixed'] ) {
            $fixed_count++;
        }
    }

    return new WP_REST_Response([
        'dry_run'     => $dry_run,
        'total_posts' => count( $posts ),
        'fixed_count' => $fixed_count,
        'results'     => $results,
    ], 200 );
}

function sourov_fix_single_post( $request ) {
    $post_id = (int) $request['id'];
    $result  = sourov_fix_post( $post_id, false );
    return new WP_REST_Response( $result, isset( $result['error'] ) ? 404 : 200 );
}

// ---------------------------------------------------------------------------
// Admin settings page
// ---------------------------------------------------------------------------
add_action( 'admin_menu', function () {
    add_options_page(
        'Sourov Fixer',
        'Sourov Fixer',
        'manage_options',
        'sourov-fixer',
        'sourov_settings_page'
    );
});

function sourov_settings_page() {
    if ( isset( $_POST['sourov_api_key'] ) && check_admin_referer( 'sourov_fixer_save' ) ) {
        update_option( 'sourov_fixer_api_key', sanitize_text_field( $_POST['sourov_api_key'] ) );
        echo '<div class="updated"><p>Settings saved.</p></div>';
    }
    $key = get_option( 'sourov_fixer_api_key', '' );
    ?>
    <div class="wrap">
        <h1>Sourov Category &amp; Tag Fixer</h1>
        <form method="post">
            <?php wp_nonce_field( 'sourov_fixer_save' ); ?>
            <table class="form-table">
                <tr>
                    <th><label>API Key</label></th>
                    <td>
                        <input type="text" name="sourov_api_key"
                               value="<?php echo esc_attr( $key ); ?>" size="50" />
                        <p class="description">Must match the X-Sourov-Key header in your scripts.</p>
                    </td>
                </tr>
            </table>
            <?php submit_button( 'Save Settings' ); ?>
        </form>

        <hr>
        <h2>How to Use</h2>
        <p>Call these endpoints with your API key in the <code>X-Sourov-Key</code> header:</p>
        <pre style="background:#f6f7f7;padding:12px;border-radius:4px"># Preview what would change (safe — no writes)
curl "<?php echo esc_url( get_rest_url( null, 'sourov/v1/preview-fixes?limit=50' ) ); ?>" \
  -H "X-Sourov-Key: YOUR_KEY"

# Fix all posts (actually writes changes)
curl -X POST "<?php echo esc_url( get_rest_url( null, 'sourov/v1/fix-posts' ) ); ?>" \
  -H "X-Sourov-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"limit": "200"}'

# Fix one post by ID
curl -X POST "<?php echo esc_url( get_rest_url( null, 'sourov/v1/fix-post/123' ) ); ?>" \
  -H "X-Sourov-Key: YOUR_KEY"</pre>

        <h2>Python Bulk Fix Script</h2>
        <pre style="background:#f6f7f7;padding:12px;border-radius:4px">import requests

headers = {'X-Sourov-Key': 'YOUR_KEY'}

# Preview first
preview = requests.get('<?php echo esc_url( get_rest_url( null, "sourov/v1/preview-fixes" ) ); ?>', headers=headers)
print(preview.json())

# Then fix
result = requests.post('<?php echo esc_url( get_rest_url( null, "sourov/v1/fix-posts" ) ); ?>',
                       json={'limit': '200'}, headers=headers)
print(f"Fixed: {result.json()['fixed_count']} posts")</pre>
    </div>
    <?php
}
