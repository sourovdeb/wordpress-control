<?php
/**
 * CalmFocus Theme - Single Post Template
 *
 * Calm, readable layout for all post types.
 * Designed for long reading sessions with low visual fatigue.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

get_header();
?>

<div id="primary" <?php astra_primary_class(); ?>>
    <?php astra_primary_content_top(); ?>

    <article id="post-<?php the_ID(); ?>" <?php post_class('calmfocus-single'); ?> style="max-width: 780px; margin: 0 auto; padding: 50px 20px;">

        <header class="entry-header" style="margin-bottom: 40px; border-bottom: 1px solid var(--wp--preset--color--border); padding-bottom: 30px;">
            <?php the_title( '<h1 class="entry-title" style="font-size: 36px; line-height: 1.3; margin-bottom: 16px;">', '</h1>' ); ?>
            <div class="entry-meta" style="font-size: 15px; color: var(--wp--preset--color--text-secondary);">
                <?php echo get_the_date(); ?>
                <?php if ( has_category() ) : ?>
                    &nbsp;&middot;&nbsp; <?php the_category( ', ' ); ?>
                <?php endif; ?>
            </div>
        </header>

        <?php if ( has_post_thumbnail() ) : ?>
            <div class="post-thumbnail" style="margin-bottom: 40px; border-radius: 8px; overflow: hidden;">
                <?php the_post_thumbnail( 'large' ); ?>
            </div>
        <?php endif; ?>

        <div class="entry-content" style="font-size: 18px; line-height: 1.75;">
            <?php the_content(); ?>
        </div>

        <?php if ( has_tag() ) : ?>
            <footer class="entry-footer" style="margin-top: 60px; padding-top: 30px; border-top: 1px solid var(--wp--preset--color--border);">
                <div style="font-size: 15px; color: var(--wp--preset--color--text-secondary);">
                    Tags: <?php the_tags( '', ', ', '' ); ?>
                </div>
            </footer>
        <?php endif; ?>

        <!-- YouTube + Connect CTA -->
        <aside style="margin-top: 48px; padding: 24px 28px; border: 1px solid var(--wp--preset--color--border); border-radius: 10px; background: var(--wp--preset--color--background, #f9f9f9);">
            <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 200px;">
                    <strong style="font-size: 16px; display: block; margin-bottom: 4px;">Treasure Hunters Digital</strong>
                    <span style="font-size: 14px; color: var(--wp--preset--color--text-secondary);">English teaching, language learning &amp; multilingual life in La R&eacute;union.</span>
                </div>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <a href="https://www.youtube.com/@TreasureHuntersDigital" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 6px; padding: 9px 16px; background: #FF0000; color: #fff; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: 600;">
                        &#9654; YouTube
                    </a>
                    <a href="https://wa.me/262693846168" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 6px; padding: 9px 16px; background: #25D366; color: #fff; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: 600;">
                        WhatsApp
                    </a>
                    <a href="mailto:sourovdeb.is@gmail.com" style="display: inline-flex; align-items: center; gap: 6px; padding: 9px 16px; background: var(--wp--preset--color--primary, #333); color: #fff; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: 600;">
                        Email
                    </a>
                </div>
            </div>
        </aside>

        <!-- Related Posts -->
        <?php
        $current_cats = wp_get_post_categories( get_the_ID(), [ 'fields' => 'ids' ] );
        if ( ! empty( $current_cats ) ) :
            $related = get_posts( [
                'category__in'   => $current_cats,
                'post__not_in'   => [ get_the_ID() ],
                'posts_per_page' => 4,
                'orderby'        => 'date',
                'order'          => 'DESC',
                'post_status'    => 'publish',
            ] );
            if ( $related ) :
        ?>
        <section class="related-posts" style="margin-top: 48px; padding-top: 30px; border-top: 1px solid var(--wp--preset--color--border);">
            <h3 style="font-size: 20px; margin-bottom: 20px;">More from this section</h3>
            <ul style="list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px;">
                <?php foreach ( $related as $rpost ) : ?>
                <li>
                    <a href="<?php echo esc_url( get_permalink( $rpost ) ); ?>" style="display: block; padding: 16px; border: 1px solid var(--wp--preset--color--border); border-radius: 8px; text-decoration: none; color: inherit;">
                        <span style="font-size: 16px; font-weight: 600; display: block; margin-bottom: 6px;"><?php echo esc_html( get_the_title( $rpost ) ); ?></span>
                        <span style="font-size: 13px; color: var(--wp--preset--color--text-secondary);"><?php echo get_the_date( '', $rpost ); ?></span>
                    </a>
                </li>
                <?php endforeach; ?>
            </ul>
        </section>
        <?php
            endif;
            wp_reset_postdata();
        endif;
        ?>

    </article>

    <?php astra_primary_content_bottom(); ?>
</div>

<?php
get_footer();
