<?php
/**
 * CalmFocus Theme - Header
 */

if ( ! defined( 'ABSPATH' ) ) exit;
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<div id="page" class="site">
<a class="skip-link screen-reader-text" href="#content"><?php esc_html_e( 'Skip to content', 'astra' ); ?></a>

<?php astra_header_before(); ?>

<header id="masthead" class="site-header">
    <div class="calmfocus-header-inner" style="max-width:1100px;margin:0 auto;padding:20px 24px;display:flex;align-items:center;justify-content:space-between;">
        
        <!-- Site Title / Home Button (always prominent) -->
        <div class="site-branding">
            <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="site-title" style="font-size:24px;font-weight:600;color:var(--wp--preset--color--text-primary);text-decoration:none;">
                <?php bloginfo( 'name' ); ?>
            </a>
        </div>

        <!-- Primary Navigation -->
        <nav id="site-navigation" class="main-navigation" aria-label="Primary Navigation">
            <?php
            wp_nav_menu( [
                'theme_location' => 'primary',
                'menu_id'        => 'primary-menu',
                'container'      => false,
                'fallback_cb'    => false,
                'depth'          => 3,
            ] );
            ?>
        </nav>

    </div>
</header>

<?php astra_header_after(); ?>

<div style="border-bottom:1px solid var(--wp--preset--color--border);"></div>

<div id="content" class="site-content">
<div class="ast-container">
