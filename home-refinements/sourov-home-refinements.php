<?php
/**
 * Plugin Name: Sourov Home Refinements
 * Description: Homepage refinements: white background, smoother cube movement, and replaces the "Motion field / pixel birds" grid with a "This may interest you" section showing random posts that change every 30 minutes. Front end only, homepage only. Deactivate to remove everything.
 * Version: 1.0.0
 * Author: Sourov Deb
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'wp_enqueue_scripts', function () {
	if ( ! is_front_page() ) {
		return;
	}

	$css = <<<'CSS'
/* ---- White background ---- */
body,
.site,
.site-content,
.site-main,
#page,
#content,
#primary,
main {
	background: #ffffff !important;
}

/* ---- Smoother cube movement ---- */
.sourov-smooth-cube,
.sourov-smooth-cube * {
	transition: transform 0.16s cubic-bezier(0.22, 0.61, 0.36, 1);
	will-change: transform;
}

/* ---- "This may interest you" section ---- */
.sourov-mi {
	padding: 2rem 1.25rem;
	background: #ffffff;
}

.sourov-mi-title {
	font-size: 1.4rem;
	margin: 0 0 1.25rem;
	letter-spacing: 0.02em;
}

.sourov-mi-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
	gap: 1.25rem;
}

.sourov-mi-card {
	display: block;
	text-decoration: none;
	color: inherit;
	background: #ffffff;
	border: 1px solid #e6e6e6;
	border-radius: 8px;
	overflow: hidden;
	transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.sourov-mi-card:hover,
.sourov-mi-card:focus-visible {
	box-shadow: 0 6px 22px rgba(0, 0, 0, 0.09);
	transform: translateY(-2px);
}

.sourov-mi-card img {
	width: 100%;
	height: 150px;
	object-fit: cover;
	display: block;
	background: #f0f0f0;
}

.sourov-mi-card-body {
	padding: 0.85rem 1rem 1rem;
}

.sourov-mi-card h3 {
	font-size: 1rem;
	line-height: 1.35;
	margin: 0 0 0.4rem;
}

.sourov-mi-card p {
	font-size: 0.85rem;
	line-height: 1.5;
	opacity: 0.75;
	margin: 0;
}

.sourov-mi-note {
	margin-top: 1rem;
	font-size: 0.75rem;
	opacity: 0.55;
}
CSS;

	wp_register_style( 'sourov-home-refinements', false );
	wp_enqueue_style( 'sourov-home-refinements' );
	wp_add_inline_style( 'sourov-home-refinements', $css );

	$js = <<<'JS'
(function () {
	'use strict';

	var WINDOW_MS = 30 * 60 * 1000; // 30 minutes

	/* ---------- 1. Smoother cube ---------- */
	function smoothCube() {
		var caption = null;
		var nodes = document.querySelectorAll('body *');
		for (var i = 0; i < nodes.length; i++) {
			var t = (nodes[i].textContent || '');
			if (t.indexOf('Drag to spin') !== -1 && t.length < 200 && !caption) {
				caption = nodes[i];
				break;
			}
		}
		if (!caption) return;
		var el = caption.previousElementSibling;
		var hops = 0;
		while (el && hops < 4) {
			var r = el.getBoundingClientRect();
			if (r.width > 80 && r.height > 80) {
				el.classList.add('sourov-smooth-cube');
				return;
			}
			el = el.previousElementSibling;
			hops++;
		}
	}

	/* ---------- 2. "This may interest you" ---------- */
	function smallestElementContaining(texts) {
		var best = null;
		var bestLen = Infinity;
		var nodes = document.querySelectorAll('body *');
		for (var i = 0; i < nodes.length; i++) {
			var el = nodes[i];
			if (el.children.length > 2) continue;
			var t = (el.textContent || '');
			var ok = true;
			for (var j = 0; j < texts.length; j++) {
				if (t.indexOf(texts[j]) === -1) { ok = false; break; }
			}
			if (ok && t.length < bestLen) {
				best = el;
				bestLen = t.length;
			}
		}
		return best;
	}

	function gridHost() {
		var label = smallestElementContaining(['Motion field', 'pixel birds']);
		if (!label) return null;
		var host = label;
		var hops = 0;
		while (host && host.parentElement && host.parentElement !== document.body && hops < 6) {
			var r = host.getBoundingClientRect();
			if (r.height >= 120 && r.width >= 240) break;
			host = host.parentElement;
			hops++;
		}
		return host;
	}

	function mulberry32(a) {
		return function () {
			a |= 0; a = (a + 0x6D2B79F5) | 0;
			var t = Math.imul(a ^ (a >>> 15), 1 | a);
			t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
			return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
		};
	}

	function pickSeeded(arr, n, seed) {
		var rnd = mulberry32(seed);
		var copy = arr.slice();
		for (var i = copy.length - 1; i > 0; i--) {
			var j = Math.floor(rnd() * (i + 1));
			var tmp = copy[i]; copy[i] = copy[j]; copy[j] = tmp;
		}
		return copy.slice(0, n);
	}

	function strip(html) {
		var d = document.createElement('div');
		d.innerHTML = html;
		return (d.textContent || '').trim();
	}

	function cardHTML(p) {
		var img = '';
		try {
			var media = p._embedded && p._embedded['wp:featuredmedia'] && p._embedded['wp:featuredmedia'][0];
			if (media) {
				var src = (media.media_details && media.media_details.sizes && media.media_details.sizes.medium && media.media_details.sizes.medium.source_url) || media.source_url;
				var alt = media.alt_text || strip(p.title.rendered);
				img = '<img src="' + src + '" alt="' + alt.replace(/"/g, '&quot;') + '" loading="lazy">';
			}
		} catch (e) {}
		var excerpt = strip(p.excerpt.rendered || '');
		if (excerpt.length > 140) excerpt = excerpt.slice(0, 140).replace(/\s+\S*$/, '') + '…';
		return '<a class="sourov-mi-card" href="' + p.link + '">' + img +
			'<div class="sourov-mi-card-body"><h3>' + strip(p.title.rendered) + '</h3><p>' + excerpt + '</p></div></a>';
	}

	var host = null;
	var allPosts = null;

	function renderWindow() {
		if (!host) return;
		var seed = Math.floor(Date.now() / WINDOW_MS);
		var picks = pickSeeded(allPosts, 4, seed);
		host.innerHTML =
			'<div class="sourov-mi">' +
			'<h2 class="sourov-mi-title">This may interest you</h2>' +
			'<div class="sourov-mi-grid">' + picks.map(cardHTML).join('') + '</div>' +
			'<p class="sourov-mi-note">A random selection of posts \u2014 refreshed every 30 minutes.</p>' +
			'</div>';
	}

	function scheduleNext() {
		var now = Date.now();
		setTimeout(function () {
			renderWindow();
			scheduleNext();
		}, WINDOW_MS - (now % WINDOW_MS) + 1500);
	}

	function replaceGrid() {
		host = gridHost();
		if (!host) return;
		host.classList.add('sourov-mi-host');
		host.setAttribute('data-sourov-mi', '1');
		fetch('/wp-json/wp/v2/posts?per_page=30&_embed=wp:featuredmedia', { credentials: 'same-origin' })
			.then(function (r) { return r.json(); })
			.then(function (posts) {
				if (!posts || !posts.length) return;
				allPosts = posts;
				renderWindow();
				scheduleNext();
			})
			.catch(function () {});
	}

	function init() {
		smoothCube();
		replaceGrid();
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
})();
JS;

	wp_register_script( 'sourov-home-refinements', false, array(), '1.0.0', true );
	wp_enqueue_script( 'sourov-home-refinements' );
	wp_add_inline_script( 'sourov-home-refinements', $js );
} );
