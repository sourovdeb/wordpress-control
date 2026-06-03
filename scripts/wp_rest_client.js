'use strict';
/**
 * wp_rest_client.js
 * Thin REST client for the WordPress /sourov/v1 custom API.
 * Used by the VS Code extension to create, update, and list posts.
 *
 * All methods return parsed JSON on success, or throw an Error
 * with a human-readable message on failure.
 */

const https = require('https');
const http  = require('http');
const { URL } = require('url');

const TIMEOUT_MS = 15_000;

class WPRestClient {
  /**
   * @param {string} baseUrl   e.g. 'https://yourdomain.com'
   * @param {string} apiKey    X-Sourov-Key value
   */
  constructor(baseUrl, apiKey) {
    if (!baseUrl) throw new Error('baseUrl is required');
    if (!apiKey)  throw new Error('apiKey is required');
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.apiKey  = apiKey;
  }

  // ─── Post operations ──────────────────────────────────────────────────

  /**
   * Create a new post.
   * @param {{ title, content, status?, category?, tags?, meta_description?, seo_title?, date? }} post
   */
  createPost(post) {
    return this._request('POST', '/wp-json/sourov/v1/ai-post', post);
  }

  /**
   * Publish a post as draft (shorthand).
   * @param {string} title
   * @param {string} content
   * @param {string[]} [tags]
   */
  createDraft(title, content, tags = []) {
    return this.createPost({
      title,
      content,
      status: 'draft',
      tags:   tags.join(', '),
    });
  }

  /**
   * Get WordPress site health from the custom endpoint.
   */
  getHealth() {
    return this._request('GET', '/wp-json/sourov/v1/health');
  }

  /**
   * Get standard WP REST API info (no auth required).
   */
  getSiteInfo() {
    return this._request('GET', '/wp-json/', null, false);
  }

  // ─── HTTP layer ──────────────────────────────────────────────────────────

  /**
   * @param {'GET'|'POST'} method
   * @param {string} path
   * @param {object|null} [body]
   * @param {boolean} [auth=true]
   */
  _request(method, path, body = null, auth = true) {
    return new Promise((resolve, reject) => {
      const url     = new URL(this.baseUrl + path);
      const adapter = url.protocol === 'https:' ? https : http;
      const payload = body ? JSON.stringify(body) : null;

      const headers = {
        'User-Agent':   'WP-Control-Extension/1.0',
        'Accept':       'application/json',
      };
      if (auth)    headers['X-Sourov-Key']   = this.apiKey;
      if (payload) headers['Content-Type']   = 'application/json';
      if (payload) headers['Content-Length'] = Buffer.byteLength(payload);

      const options = {
        hostname: url.hostname,
        port:     url.port || (url.protocol === 'https:' ? 443 : 80),
        path:     url.pathname + url.search,
        method,
        headers,
        timeout: TIMEOUT_MS,
      };

      const req = adapter.request(options, res => {
        let data = '';
        res.setEncoding('utf8');
        res.on('data', c => { data += c; });
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            if (res.statusCode >= 400) {
              reject(new Error(
                `HTTP ${res.statusCode}: ${parsed.message || parsed.error || data.slice(0, 200)}`
              ));
            } else {
              resolve(parsed);
            }
          } catch {
            reject(new Error(`Non-JSON response (HTTP ${res.statusCode}): ${data.slice(0, 200)}`));
          }
        });
      });

      req.on('timeout', () => req.destroy(new Error('Request timed out')));
      req.on('error',   reject);
      if (payload) req.write(payload);
      req.end();
    });
  }
}

module.exports = { WPRestClient };
