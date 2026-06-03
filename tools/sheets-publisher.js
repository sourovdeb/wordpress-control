/**
 * WP Auto-Publisher — Google Sheets Version
 * Author: Sourov DEB | 2026-06-03
 *
 * SHEET STRUCTURE (row 1 = headers):
 *   A: Title
 *   B: Content / Topic
 *   C: Category
 *   D: Status        ← READY | SCHEDULE | DRAFT | DONE | ERROR
 *   E: Schedule Date  (e.g. 2026-06-15 09:00, for SCHEDULE rows)
 *   F: Published URL  (filled automatically)
 *   G: Notes
 *
 * SETUP (run once):
 *   1. Open Google Sheets → Extensions → Apps Script
 *   2. Paste this file
 *   3. Run setupCredentials() once (edit values first, then delete the function)
 *   4. Run createHourlyTrigger() once
 *   5. Done — every hour it will check for READY/SCHEDULE rows and publish them
 *
 * USAGE:
 *   - Set Status = READY    → publishes immediately
 *   - Set Status = SCHEDULE → schedules for the date in column E
 *   - Set Status = DRAFT    → saves as draft (for review in WP admin)
 *   - After publishing, Status changes to DONE and URL is filled in column F
 */

// ── Credentials (stored in Script Properties, not here) ───────────────────────
function getWpKey()     { return PropertiesService.getScriptProperties().getProperty('WP_API_KEY');  }
function getClaudeKey() { return PropertiesService.getScriptProperties().getProperty('CLAUDE_KEY');  }

const WP_BASE     = 'https://sourovdeb.com';
const WP_ENDPOINT = WP_BASE + '/wp-json/sourov/v1/ai-post';
const SHEET_NAME  = 'Posts';

// ── Main function (runs on timer) ─────────────────────────────────────────────
function runPublisher() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SHEET_NAME) || ss.getActiveSheet();
  const data  = sheet.getDataRange().getValues();

  let processed = 0;

  for (let i = 1; i < data.length; i++) {
    const [title, content, category, status, schedDate] = data[i];
    const rowNum   = i + 1;
    const statusUp = String(status || '').trim().toUpperCase();

    if (!title || !['READY', 'SCHEDULE', 'DRAFT'].includes(statusUp)) continue;

    Logger.log(`Row ${rowNum}: "${title}" → ${statusUp}`);

    try {
      // Auto-fill SEO if we have a Claude key
      let seo = {};
      if (content && getClaudeKey()) {
        seo = autoFillSEO(String(title), String(content));
        Logger.log(`  SEO: tags=[${(seo.tags||[]).join(', ')}]`);
      }

      const wpStatus = statusUp === 'READY' ? 'publish'
                     : statusUp === 'DRAFT' ? 'draft'
                     : 'future';

      const body = {
        title:            String(title),
        content:          String(content),
        category:         String(category || seo.category || 'ELT'),
        tags:             (seo.tags || []).join(', '),
        meta_description: seo.meta_description || '',
        seo_title:        seo.seo_title || String(title),
        status:           wpStatus,
      };

      if (wpStatus === 'future' && schedDate) {
        const d = new Date(schedDate);
        body.date = Utilities.formatDate(d, 'UTC', "yyyy-MM-dd'T'HH:mm:ss");
      }

      const result = wpPost(body);
      const url    = result.link || result.url || '';

      // Mark row green, write URL, update status
      sheet.getRange(rowNum, 4).setValue('DONE').setBackground('#c3e6cb');
      sheet.getRange(rowNum, 6).setValue(url);
      Logger.log(`  ✓ Published ID:${result.id} — ${url}`);
      processed++;
      Utilities.sleep(1500); // Respect rate limits

    } catch (e) {
      sheet.getRange(rowNum, 4).setValue('ERROR: ' + e.message).setBackground('#f5c6cb');
      Logger.log(`  ✗ Error: ${e.message}`);
    }
  }

  Logger.log(`Done. Processed ${processed} row(s).`);
}

// ── Auto-fill SEO via Claude Haiku ────────────────────────────────────────────
function autoFillSEO(title, content) {
  const claudeKey = getClaudeKey();
  if (!claudeKey) return {};

  const payload = {
    model:      'claude-haiku-4-5-20251001',
    max_tokens: 500,
    system:     'You are an SEO expert for an ELT educator blog. Return ONLY valid JSON, no markdown.',
    messages: [{
      role:    'user',
      content: `Title: "${title}"\nContent preview: ${content.slice(0, 600)}\n\nReturn exactly: {"tags":["t1","t2","t3","t4","t5"],"category":"ELT Masterclass","meta_description":"120-155 char description","seo_title":"max 60 char title"}`
    }]
  };

  const r = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', {
    method:  'post',
    headers: {
      'x-api-key':           claudeKey,
      'anthropic-version':   '2023-06-01',
      'content-type':        'application/json',
    },
    payload:            JSON.stringify(payload),
    muteHttpExceptions: true,
  });

  const d   = JSON.parse(r.getContentText());
  let   raw = (d.content || [{}])[0].text || '{}';
  raw = raw.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
  try { return JSON.parse(raw); } catch(e) { return {}; }
}

// ── WordPress POST helper ─────────────────────────────────────────────────────
function wpPost(body) {
  const r = UrlFetchApp.fetch(WP_ENDPOINT, {
    method:  'post',
    headers: {
      'X-Sourov-Key': getWpKey(),
      'Content-Type': 'application/json',
    },
    payload:            JSON.stringify(body),
    muteHttpExceptions: true,
  });
  const code = r.getResponseCode();
  const text = r.getContentText();
  if (code < 200 || code > 299) throw new Error(`HTTP ${code}: ${text.slice(0, 200)}`);
  return JSON.parse(text);
}

// ── Site health check ─────────────────────────────────────────────────────────
function checkSiteStatus() {
  const r = UrlFetchApp.fetch(`${WP_BASE}/wp-json/sourov/v1/status`, { muteHttpExceptions: true });
  Logger.log(r.getContentText());
}

// ── Setup: run once to store credentials ─────────────────────────────────────
// IMPORTANT: Fill in your values, run this function once, then DELETE it from the script
function setupCredentials() {
  const props = PropertiesService.getScriptProperties();
  props.setProperty('WP_API_KEY',  'REPLACE_WITH_YOUR_PLUGIN_KEY');
  props.setProperty('CLAUDE_KEY',  'REPLACE_WITH_YOUR_CLAUDE_KEY');
  Logger.log('✓ Credentials stored. Now delete this function from the script.');
}

// ── Setup: create hourly trigger ──────────────────────────────────────────────
function createHourlyTrigger() {
  // Remove existing triggers first
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  // Create new hourly trigger
  ScriptApp.newTrigger('runPublisher')
    .timeBased()
    .everyHours(1)
    .create();
  Logger.log('✓ Hourly trigger created. runPublisher will fire every hour.');
}

// ── Sheet setup: create headers ───────────────────────────────────────────────
function createSheetHeaders() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  let   sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME);

  const headers = ['Title', 'Content / Topic', 'Category', 'Status', 'Schedule Date', 'Published URL', 'Notes'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers])
    .setBackground('#4a4a4a').setFontColor('#ffffff').setFontWeight('bold');

  // Status dropdown validation
  const rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['READY', 'SCHEDULE', 'DRAFT', 'DONE', 'ERROR'], true)
    .build();
  sheet.getRange('D2:D1000').setDataValidation(rule);

  // Freeze header row
  sheet.setFrozenRows(1);
  Logger.log('✓ Sheet headers created.');
}
