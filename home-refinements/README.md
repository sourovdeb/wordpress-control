# Homepage Refinements — Install Guide

One plugin delivers all three homepage changes requested on 2026-10-22:

1. **White background** — the light-grey homepage background becomes `#ffffff`.
2. **Smoother cube movement** — the hero cube gets eased, GPU-friendly transitions so dragging/swiping feels fluid instead of stepped.
3. **"This may interest you"** — the "Motion field / pixel birds" grid is replaced by a section showing 4 random posts, re-shuffled automatically every 30 minutes (seeded by the current 30-minute window, so every visitor sees the same pick per window).

Also already done live (via WordPress connector, no plugin needed): the **Header Nav menu was cleaned** to 9 flat top-level items — Home, About Me, English Teaching, Teacher Training, Career & Professional Development, Philosophy & Mental Health, Photography & Software, Resources, Blog. All 17 nested sub-items were removed.

## Install (Hostinger hPanel — ~2 minutes)

1. Download `sourov-home-refinements.php` from this folder.
2. In hPanel go to **Files → File Manager** → `public_html/wp-content/plugins/`.
3. Create folder `sourov-home-refinements`, and upload `sourov-home-refinements.php` into it.
4. In WordPress admin go to **Plugins** and activate **Sourov Home Refinements**.
5. Hard-refresh the homepage (Ctrl+F5). If a caching plugin or Hostinger cache is on, purge it once.

## How it works

- Loads only on the homepage front page, front end only.
- Finds the cube by the "Drag to spin…" caption and the grid by the "Motion field / pixel birds" label — no theme files are edited.
- Random picks come from `/wp-json/wp/v2/posts` (latest 30 posts), shuffled with a seeded PRNG keyed to the current 30-minute window; a timer re-renders exactly at each window boundary.
- Fully reversible: **deactivate the plugin to remove everything instantly.** Delete the folder to remove permanently.

## If a selector misses

The labels are taken from the live homepage HTML. If a future theme version renames "Motion field / pixel birds" or "Drag to spin", the corresponding feature silently no-ops — edit those strings in the plugin's JS section to match the new labels.
