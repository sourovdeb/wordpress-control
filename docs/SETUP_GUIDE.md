# WordPress Control — Setup Guide

This VS Code extension provides a sidebar panel to manage your WordPress site
without leaving the editor.

---

## Requirements

- VS Code 1.74+
- Node.js 18+
- A WordPress site with the `sourov-ai-controller.php` plugin active
- Your API key (set in WordPress plugin settings)

---

## Installation (Development Mode)

```bash
git clone https://github.com/sourovdeb/wordpress-control
cd wordpress-control
npm install

# Open in VS Code
code .

# Press F5 to launch Extension Development Host
```

---

## Configuration

Set these in VS Code settings (`Ctrl+,`) or `settings.json`:

```json
{
  "wpControl.siteUrl": "https://yourdomain.com",
  "wpControl.apiKey":  ""
}
```

**Never commit your API key.** Use VS Code settings or environment variables.

---

## Features

### Sidebar Panel
Open via the WordPress icon in the Activity Bar.

| Button | Action |
|--------|--------|
| Health Check | Runs all health checks; shows pass/fail |
| New Draft | Opens a form to create a WordPress draft |
| View Posts | Lists recent posts from your site |
| Publish | Changes a draft to published |

### Health Check API

The extension calls `GET /wp-json/sourov/v1/health` (requires plugin + API key).

Checks performed:
- WP REST API reachable
- Custom endpoint responding
- Home page returning 200
- SSL certificate valid
- robots.txt and sitemap present

### REST Client (scripts/wp_rest_client.js)

```javascript
const { WPRestClient } = require('./scripts/wp_rest_client');

const wp = new WPRestClient('https://yourdomain.com', 'your-api-key');

// Create a draft
const result = await wp.createDraft('My Post Title', '<p>Body content.</p>', ['ELT']);
console.log('Created post ID:', result.post_id);

// Health check
const health = await wp.getHealth();
console.log('DB OK:', health.database_ok);
```

---

## WordPress Plugin (Required)

The extension communicates with your site via a custom REST endpoint.
Install the health monitor plugin:

1. Copy `../my_professional_documents/plugins/wp_health_monitor.php`
   to `/wp-content/plugins/sourov-health-monitor/wp_health_monitor.php`
2. Activate in WordPress admin > Plugins
3. Add to `wp-config.php`:
   ```php
   define( 'SOUROV_API_KEY', 'your-key-here' );
   ```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Health check returns 401 | Wrong API key in settings |
| Health check returns 404 | Plugin not active on WordPress |
| "Cannot connect" | Check `wpControl.siteUrl` is correct |
| Extension not loading | Run `npm install`, press F5 again |
| CORS error in webview | Expected — extension uses Node.js HTTP, not fetch |
