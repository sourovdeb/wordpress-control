# WP AI Studio — Changelog

## 2026-07-02

### Site Enhancer Plugin — v2.0.0 deployed to sourovdeb.com

The `sourov-site-enhancer` plugin was upgraded from v1.0.0 to v2.0.0 directly on the live server.

#### New REST API fields (available on all posts)

When querying posts via the WP REST API, two new fields are now returned:

| Field | Type | Description |
|---|---|---|
| `_ssd_yt` | string (URL) | YouTube video URL for this post. Set via post meta box. |
| `_ssd_pod` | string (URL) | Podcast episode URL for this post. MP3 files show a native player; other URLs show a link. |

#### New shortcodes

| Shortcode | Usage |
|---|---|
| `[sourov_youtube video_id="XXXXXXXXXXX"]` | Responsive 16:9 YouTube embed (no-cookie) |
| `[sourov_podcast src="URL" title="Episode Title"]` | Native audio player |

#### YouTube Channel CTA

Appears automatically at the bottom of all posts in the following categories (no video URL needed):
- English Teaching (category ID 9)
- Philosophy (category ID 581)
- Mental Health (category ID 582)

Channel: **Treasure Hunters Digital** — `https://www.youtube.com/channel/UC1rs5aY7YdFiADKkhOMPCvQ`

#### New sidebar widget

`SSD_YouTube_Widget` — add via WP Admin > Appearance > Widgets > "Sourov — YouTube Channel"

#### Using the extension to set YouTube video per post

In the WP AI Studio panel, when creating or updating a post, you can include the `_ssd_yt` field to set a YouTube URL:

```json
{
  "title": "ELT365 · Day 188 — Information-gap tasks",
  "content": "<p>Content here...</p>",
  "status": "publish",
  "_ssd_yt": "https://youtu.be/YOUR_VIDEO_ID"
}
```

Or via the custom AI controller API:

```bash
curl -X POST "https://sourovdeb.com/wp-json/sourov/v1/ai-post" \
  -H "X-Sourov-Key: 0767044896thevenet_" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "ELT365 · Day 189 — Drilling",
    "content": "<p>...</p>",
    "status": "publish",
    "category": "English Teaching",
    "_ssd_yt": "https://youtu.be/ABC123DEFGH"
  }'
```

Note: The `_ssd_yt` field is a post meta field — if the standard WP REST API rejects it, set it directly via the meta endpoint:

```bash
curl -X POST "https://sourovdeb.com/wp-json/wp/v2/posts/{POST_ID}/meta" \
  -u "USERNAME:APP_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"key": "_ssd_yt", "value": "https://youtu.be/VIDEO_ID"}'
```
