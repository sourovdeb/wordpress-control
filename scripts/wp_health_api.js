'use strict';
/**
 * wp_health_api.js
 * WordPress health check module for the VS Code extension.
 *
 * Usage:
 *   const { checkHealth } = require('./wp_health_api');
 *   const result = await checkHealth(baseUrl, apiKey);
 *
 * Returns a plain object with:
 *   { ok: boolean, score: string, checks: Array<{name, status, detail}> }
 */

const https = require('https');
const http  = require('http');
const { URL } = require('url');

const TIMEOUT_MS = 10_000;

/**
 * Perform a single HTTP GET and resolve with { statusCode, body }.
 * @param {string} rawUrl
 * @param {Record<string, string>} [headers={}]
 * @returns {Promise<{statusCode: number, body: string}>}
 */
function httpGet(rawUrl, headers = {}) {
  return new Promise((resolve, reject) => {
    const parsed  = new URL(rawUrl);
    const adapter = parsed.protocol === 'https:' ? https : http;
    const options = {
      hostname: parsed.hostname,
      port:     parsed.port || (parsed.protocol === 'https:' ? 443 : 80),
      path:     parsed.pathname + parsed.search,
      method:   'GET',
      headers:  { 'User-Agent': 'WP-Control-Extension/1.0', ...headers },
      timeout:  TIMEOUT_MS,
    };
    const req = adapter.request(options, res => {
      let body = '';
      res.setEncoding('utf8');
      res.on('data', chunk => { body += chunk; });
      res.on('end',  ()    => resolve({ statusCode: res.statusCode, body }));
    });
    req.on('timeout', () => { req.destroy(new Error('Request timed out')); });
    req.on('error',   reject);
    req.end();
  });
}

// ─── Individual checks ──────────────────────────────────────────────────────

async function checkRestApi(base) {
  const { statusCode, body } = await httpGet(`${base}/wp-json/`);
  if (statusCode !== 200) throw new Error(`HTTP ${statusCode}`);
  const data = JSON.parse(body);
  return { name: data.name, wpUrl: data.url };
}

async function checkCustomEndpoint(base, apiKey) {
  if (!apiKey) return 'skipped (no API key)';
  const { statusCode, body } = await httpGet(
    `${base}/wp-json/sourov/v1/health`,
    { 'X-Sourov-Key': apiKey },
  );
  if (statusCode === 404) return 'endpoint not found';
  if (statusCode !== 200) throw new Error(`HTTP ${statusCode}`);
  return JSON.parse(body);
}

async function checkHomePage(base) {
  const { statusCode, body } = await httpGet(base);
  if (statusCode !== 200 && statusCode !== 301 && statusCode !== 302) {
    throw new Error(`HTTP ${statusCode}`);
  }
  return { http: statusCode, hasWpContent: body.includes('wp-content') };
}

async function checkSsl(base) {
  if (!base.startsWith('https://')) throw new Error('Not using HTTPS');
  const { statusCode } = await httpGet(base);
  return { sslValid: true, http: statusCode };
}

async function checkRobots(base) {
  const { statusCode, body } = await httpGet(`${base}/robots.txt`);
  return { http: statusCode, hasDisallow: body.includes('Disallow') };
}

async function checkSitemap(base) {
  for (const path of ['/sitemap.xml', '/sitemap_index.xml', '/wp-sitemap.xml']) {
    try {
      const { statusCode } = await httpGet(base + path);
      if (statusCode === 200) return { foundAt: path };
    } catch { /* try next */ }
  }
  throw new Error('No sitemap found');
}

// ─── Orchestrator ────────────────────────────────────────────────────────────

/**
 * Run all health checks against a WordPress site.
 * @param {string} baseUrl  e.g. 'https://yourdomain.com'
 * @param {string} [apiKey] X-Sourov-Key value
 * @returns {Promise<{ok: boolean, score: string, timestamp: string, checks: object[]}>}
 */
async function checkHealth(baseUrl, apiKey = '') {
  const base = baseUrl.replace(/\/$/, '');
  const CHECKS = [
    ['WP REST API',            () => checkRestApi(base)],
    ['Custom /health endpoint',() => checkCustomEndpoint(base, apiKey)],
    ['Home page',              () => checkHomePage(base)],
    ['SSL certificate',        () => checkSsl(base)],
    ['robots.txt',             () => checkRobots(base)],
    ['Sitemap',                () => checkSitemap(base)],
  ];

  const checks = await Promise.all(
    CHECKS.map(async ([name, fn]) => {
      const start = Date.now();
      try {
        const detail = await fn();
        return { name, status: 'pass', ms: Date.now() - start, detail };
      } catch (err) {
        return { name, status: 'fail', ms: Date.now() - start, detail: err.message };
      }
    })
  );

  const passed = checks.filter(c => c.status === 'pass').length;
  return {
    ok:        passed === checks.length,
    score:     `${Math.round(passed / checks.length * 100)}% (${passed}/${checks.length})`,
    timestamp: new Date().toISOString(),
    checks,
  };
}

module.exports = { checkHealth };
