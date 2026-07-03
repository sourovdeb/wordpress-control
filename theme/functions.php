<?php
/**
 * Astra Theme + CalmFocus Automation — functions.php
 *
 * Uses PSR-style class autoloading so Astra classes are discovered on demand
 * without requiring a specific load order.
 *
 * @package Astra
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// ─── ASTRA CORE CONSTANTS ─────────────────────────────────────────────────

if ( ! defined( 'ASTRA_THEME_SETTINGS' ) ) {
    define( 'ASTRA_THEME_SETTINGS', 'astra-settings' );
}
if ( ! defined( 'ASTRA_THEME_VERSION' ) ) {
    define( 'ASTRA_THEME_VERSION', '4.8.4' );
}
if ( ! defined( 'ASTRA_THEME_DIR' ) ) {
    define( 'ASTRA_THEME_DIR', trailingslashit( get_template_directory() ) );
}
if ( ! defined( 'ASTRA_THEME_URI' ) ) {
    define( 'ASTRA_THEME_URI', trailingslashit( esc_url( get_template_directory_uri() ) ) );
}
if ( ! defined( 'ASTRA_THEME_TP' ) ) {
    define( 'ASTRA_THEME_TP', '' );
}
if ( ! defined( 'ASTRA_WEBSITE_BASE_URL' ) ) {
    define( 'ASTRA_WEBSITE_BASE_URL', 'https://wpastra.com' );
}

// ─── ASTRA CLASS AUTOLOADER ───────────────────────────────────────────────
//
// Astra classes follow the pattern: Astra_Some_Class → class-astra-some-class.php
// This autoloader scans known directories so classes are loaded on first use,
// eliminating manual dependency ordering.
//

spl_autoload_register( function ( $class_name ) {
    // Only handle Astra classes
    if ( strpos( $class_name, 'Astra' ) === false ) {
        return;
    }

    // Astra class-name → file-name convention
    $file = 'class-' . strtolower( str_replace( '_', '-', $class_name ) ) . '.php';

    $search_dirs = [
        ASTRA_THEME_DIR . 'inc/',
        ASTRA_THEME_DIR . 'inc/core/',
        ASTRA_THEME_DIR . 'inc/core/builder/',
        ASTRA_THEME_DIR . 'inc/core/markup/',
        ASTRA_THEME_DIR . 'inc/core/deprecated/',
        ASTRA_THEME_DIR . 'inc/modules/posts-structures/',
        ASTRA_THEME_DIR . 'inc/modules/related-posts/',
        ASTRA_THEME_DIR . 'inc/customizer/',
        ASTRA_THEME_DIR . 'inc/metabox/',
        ASTRA_THEME_DIR . 'inc/integrations/',
        ASTRA_THEME_DIR . 'inc/lib/',
        ASTRA_THEME_DIR . 'inc/admin/',
        ASTRA_THEME_DIR . 'inc/addons/',
        ASTRA_THEME_DIR . 'inc/abilities/',
    ];

    foreach ( $search_dirs as $dir ) {
        $path = $dir . $file;
        if ( file_exists( $path ) ) {
            require_once $path;
            return;
        }
    }
}, true, true ); // prepend = true, throws = true

// ─── ASTRA CORE BOOTSTRAP ─────────────────────────────────────────────────
//
// Load the main class first — it registers after_setup_theme and init hooks.
// All other classes are loaded on-demand via the autoloader above.
//

require_once ASTRA_THEME_DIR . 'inc/class-astra-after-setup-theme.php';

// ─── ASTRA FUNCTION FILES ─────────────────────────────────────────────────
//
// Free functions (not classes) must be explicitly required.
// Load common-functions first — almost everything else depends on it.
//

require_once ASTRA_THEME_DIR . 'inc/core/common-functions.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-theme-strings.php';
require_once ASTRA_THEME_DIR . 'inc/core/theme-hooks.php';
require_once ASTRA_THEME_DIR . 'inc/core/sidebar-manager.php';
require_once ASTRA_THEME_DIR . 'inc/extras.php';
require_once ASTRA_THEME_DIR . 'inc/markup-extras.php';
require_once ASTRA_THEME_DIR . 'inc/template-parts.php';

if ( file_exists( ASTRA_THEME_DIR . 'inc/template-tags.php' ) ) {
    require_once ASTRA_THEME_DIR . 'inc/template-tags.php';
}
if ( file_exists( ASTRA_THEME_DIR . 'inc/widgets.php' ) ) {
    require_once ASTRA_THEME_DIR . 'inc/widgets.php';
}
if ( file_exists( ASTRA_THEME_DIR . 'inc/w-org-version.php' ) ) {
    require_once ASTRA_THEME_DIR . 'inc/w-org-version.php';
}

// ─── CALMFOCUS DYNAMIC MENU AUTOMATION ───────────────────────────────────
//
// Publishes recent posts as nav submenu items automatically.
// Category slug → menu item title mapping below. Edit to add/remove entries.
// Cache clears automatically when a post in a mapped category is published.
//

class CalmFocus_Dynamic_Menu {

    /**
     * Category slug => Exact menu item title it should appear under.
     * This is your single source of truth — edit freely.
     */
    private $category_to_menu_map = [
        'english-lessons'          => 'English Lessons',
        'personal-blogs'           => 'Personal Blogs',
        'europe-travel'            => 'Europe Travel',
        'books-ideas'              => 'Books & Ideas',
        'photo-software'           => 'Photography & Software',
        'creator-life'             => 'Creator & Life',
        'philosophy-mental-health' => 'Philosophy & Mental Health',
        'resources'                => 'Resources',
        'tutorials'                => 'Tutorials',
    ];

    /** How many recent posts to show under each parent */
    private $posts_per_category = 8;

    public function __construct() {
        add_filter( 'wp_nav_menu_objects', [ $this, 'inject_recent_posts_as_submenu' ], 10, 2 );
        add_action( 'save_post', [ $this, 'clear_menu_cache_on_relevant_post' ], 10, 3 );
    }

    public function inject_recent_posts_as_submenu( $items, $args ) {
        if ( ! isset( $args->theme_location ) || $args->theme_location !== 'primary' ) {
            return $items;
        }

        $cache_key = 'calmfocus_dynamic_menu_' . md5( serialize( $this->category_to_menu_map ) );
        $cached    = get_transient( $cache_key );

        if ( false !== $cached ) {
            return array_merge( $items, $cached );
        }

        $new_items = [];

        foreach ( $items as $item ) {
            $new_items[] = $item;

            $matched_category = $this->get_matched_category_slug( $item->title );

            if ( $matched_category ) {
                $recent_posts = $this->get_recent_posts_for_category( $matched_category );

                foreach ( $recent_posts as $post ) {
                    $new_items[] = $this->create_dynamic_menu_item( $post, $item->ID );
                }
            }
        }

        set_transient( $cache_key, array_slice( $new_items, count( $items ) ), 12 * HOUR_IN_SECONDS );

        return $new_items;
    }

    private function get_matched_category_slug( $menu_title ) {
        foreach ( $this->category_to_menu_map as $cat_slug => $mapped_title ) {
            if ( trim( $menu_title ) === trim( $mapped_title ) ) {
                return $cat_slug;
            }
        }
        return false;
    }

    private function get_recent_posts_for_category( $category_slug ) {
        return get_posts( [
            'category_name'  => $category_slug,
            'posts_per_page' => $this->posts_per_category,
            'post_status'    => 'publish',
            'orderby'        => 'date',
            'order'          => 'DESC',
        ] );
    }

    private function create_dynamic_menu_item( $post, $parent_menu_id ) {
        $item = new stdClass();

        $item->ID                    = 1000000 + $post->ID;
        $item->db_id                 = $item->ID;
        $item->title                 = get_the_title( $post );
        $item->url                   = get_permalink( $post );
        $item->menu_item_parent      = $parent_menu_id;
        $item->menu_order            = 1000 + $post->ID;
        $item->type                  = 'custom';
        $item->object                = 'custom';
        $item->object_id             = $post->ID;
        $item->classes               = [ 'menu-item', 'menu-item-type-custom', 'calmfocus-dynamic-post' ];
        $item->target                = '';
        $item->attr_title            = '';
        $item->description           = '';
        $item->xfn                   = '';
        $item->current               = false;
        $item->current_item_ancestor = false;
        $item->current_item_parent   = false;

        return $item;
    }

    public function clear_menu_cache_on_relevant_post( $post_id, $post, $update ) {
        if ( $post->post_type !== 'post' || $post->post_status !== 'publish' ) {
            return;
        }

        $categories = wp_get_post_categories( $post_id, [ 'fields' => 'slugs' ] );

        foreach ( $categories as $cat_slug ) {
            if ( isset( $this->category_to_menu_map[ $cat_slug ] ) ) {
                delete_transient( 'calmfocus_dynamic_menu_' . md5( serialize( $this->category_to_menu_map ) ) );
                break;
            }
        }
    }
}

new CalmFocus_Dynamic_Menu();
