# SKILL — AI Teach & Create (ELT content → sourovdeb.com)

**Use when:** an AI agent should (a) **teach** — generate ELT lessons/explainers
grounded in standard frameworks — and (b) **create** — publish them to
sourovdeb.com in the right pillar, compliant by construction. Pairs with
SKILL_wordpress_site_management and GUIDELINE_site_content_management.

---

## 1. TEACH — generate the material

Work only from established ELT frameworks (name them; don't invent methods):

- **PPP** — Presentation → Practice → Production.
- **TBLT** — Task-Based: task first, language second (Willis).
- **TTT** — Test → Teach → Test (diagnose, then target the gap).
- **ESA** — Engage → Study → Activate (Harmer).
- **MFP** analysis — for any target language, state **Meaning, Form,
  Pronunciation**, plus **CCQs** (concept-checking questions).
- **Receptive skills** — gist / scanning / intensive sub-skills, top-down +
  bottom-up processing.
- **Communicative approach** — meaning-focused, learner talking time over teacher talking time.

**Lesson skeleton (trainer-facing):**
1. **Aim** — "By the end, learners will be better able to … (SWBAT)."
2. **Target language** + **MFP** + **anticipated problems & solutions**.
3. **Assumed knowledge.**
4. **Stages** — name · purpose · interaction (T-S / S-S / individual) · timing.
5. **CCQs**, instructions (ICQs), board plan.
6. **Materials / sources** (cite real ones).

**Learner-facing post** = same content, jargon stripped: a short explanation, 2–3
worked examples, a mini practice set with an answer key, one takeaway.

## 2. Compliance (build it in, don't bolt it on)

- **CELTA wording (hard):** if the qualification is mentioned anywhere, use only:
  "Cambridge CELTA course completed — 120 supervised teaching hours and four
  written assignments validated to the required standard." Never "obtained /
  certified / awarded." (Ofqual SJ3XP35D.)
- **Zero fabrication:** no invented citations, rules, or statistics. If unsure of
  a rule, state it plainly and cite a grammar reference (e.g. Swan, *Practical
  English Usage*) rather than guessing.
- Affiliate disclosure (Resources) and the mental-health notice are
  **auto-injected by the theme** — don't duplicate them in the body.
- Internal "Related reading" backlinks, meta, JSON-LD, and IndexNow are
  **automatic on publish** — write good content; the theme does SEO.

## 3. CREATE — choose pillar + format

| Content | Pillar (`category`) | Format |
|---|---|---|
| Lesson / method / IELTS / "X of 60" | `English Teaching` | learner-facing or trainer-facing post |
| Essay on meaning / disclosure / coping | `Philosophy & Mental Health` | reflective essay |
| Tool / book / service recommendation | `Resources` | review + honest notes (affiliate links ok) |

Post fields: `title`, `content` (HTML), `status` (`publish|future|draft`),
`category`, `tags`, `meta_description` (≤155), `seo_title`.

## 4. PUBLISH — Google Apps Script (no Sheet)

Paste into script.google.com → run `publishLesson()`. Pure JS, no Sheet, no
dependency. Same endpoint as everything else.

```javascript
/** WordPress publisher for sourovdeb.com — Apps Script, no Sheet. */
var WP_ENDPOINT = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
var WP_KEY      = '0767044896thevenet_';

function wpPost(post) {
  var res = UrlFetchApp.fetch(WP_ENDPOINT, {
    method: 'post',
    headers: { 'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json' },
    payload: JSON.stringify(post),
    muteHttpExceptions: true
  });
  return 'HTTP ' + res.getResponseCode() + ': ' + res.getContentText();
}

/** Publish one ELT post to the English Teaching pillar. */
function publishLesson() {
  var post = {
    title:   'Present Perfect vs Past Simple — when each one is true',
    content: [
      '<p>Use the <b>past simple</b> for a finished time; the <b>present perfect</b> when the time is unfinished or the result matters now.</p>',
      '<h2>Examples</h2>',
      '<ul><li>I <i>saw</i> her yesterday. (finished time)</li>',
      '<li>I <i>have seen</i> that film. (when isn’t the point)</li></ul>',
      '<h2>Practice</h2>',
      '<ol><li>I ___ (live) here since 2019.</li><li>We ___ (go) to Paris last May.</li></ol>',
      '<p><b>Answers:</b> have lived · went.</p>',
      '<p><b>Takeaway:</b> ask “is the time finished?” first.</p>'
    ].join(''),
    status:  'publish',                 // 'publish' | 'future' | 'draft'
    category: 'English Teaching',       // pillar: drives menu, archive, backlinks
    tags:    'grammar, tense, present perfect, past simple',
    meta_description: 'A simple rule for choosing present perfect or past simple, with examples and practice.',
    seo_title: 'Present Perfect vs Past Simple | Sourov Deb'
    // date: '2026-06-20T09:00:00'       // add when status='future'
  };
  Logger.log(wpPost(post));
}

/** Optional: queue several, spaced out. */
function publishBatch() {
  var posts = [ /* {title, content, status, category, tags, meta_description, seo_title}, ... */ ];
  for (var i = 0; i < posts.length; i++) {
    Logger.log((i + 1) + ': ' + wpPost(posts[i]));
    Utilities.sleep(1500);
  }
}
```
Rhino-safe (var, standard for-loop, no const/let/arrow) per the project's GAS constraint.

**curl equivalent** (any agent): see SKILL_wordpress_site_management §8.

## 5. End-to-end loop

1. Generate lesson (§1) → strip to learner-facing post (§1).
2. Run compliance pass (§2): CELTA phrasing, no fabrication, no method names for self-harm.
3. Set pillar + fields (§3).
4. Publish via GAS or curl (§4). Theme handles disclosure, backlinks, SEO, IndexNow.
5. Confirm: `GET …/wp-json/wp/v2/posts?per_page=1&_fields=id,link` returns the new post.

---
*Frameworks: standard CELTA syllabus (PPP, TBLT, TTT, ESA, MFP/CCQ, communicative
approach). Grammar reference of record: Swan, Practical English Usage. Compliance:
Ofqual SJ3XP35D. Publishing: sourov/v1 REST API.*
