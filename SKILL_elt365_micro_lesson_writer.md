# SKILL: ELT365 Micro-Lesson Writer
**Version:** 1.0 · 2026-06-11 · Author context: Sourov Deb / sourovdeb.com
**Purpose:** Generate, extend, and upgrade the ELT365 series — a free 365-day teacher-training micro-course (one 5-minute lesson/day, CELTA-syllabus-level content). Reusable by any AI session. Load this file + ELT365_00_MASTER_PLAN.md before generating.

---

## 1. HARD CONSTRAINTS (legal — never violate)

1. **CELTA wording.** Author may ONLY be described as: "Cambridge CELTA course completed — 120 supervised teaching-practice hours, 4 written assignments passed at the required standard." NEVER "CELTA certified / qualified / awarded / holder." Reason: qualification under appeal (Ofqual ref SJ3XP35D); misstatement has legal consequences.
2. **Trademark.** "CELTA" is a Cambridge trademark. Series name must not contain it. Series name: **ELT365**. Body text may reference "the Cambridge CELTA syllabus (public document)" factually.
3. **Disclaimer** on every file and every published post footer:
   > *Independent project; not affiliated with, endorsed by, or accredited by Cambridge University Press & Assessment. Confers no qualification.*
4. **Zero fabrication.** Research claims hedged and attributed ("Nation's research suggests…", "often described as…"). No invented statistics, quotes, or citations.

## 2. SOURCE CANON (ground all content here)

Cambridge CELTA public syllabus (5 topic areas) · Scrivener *Learning Teaching* · Harmer *The Practice of ELT* · Thornbury *How to Teach Grammar / About Language* · Ur *A Course in Language Teaching* · Nation *Learning Vocabulary in Another Language* · Underhill *Sound Foundations* · Swan *Learner English*. If a claim cannot be traced to mainstream ELT methodology, cut it.

## 3. LESSON FORMAT (fixed — 55–80 words each)

```
### DNNN · Title
**Idea —** Core concept, ≤2 sentences.
**Example —** One concrete illustration.
**Try —** A task doable in ≤2 minutes.
```
- Day numbers zero-padded to 3 digits (D152).
- Last day of each month = review quiz referencing prior day numbers + one-line preview of next month.
- Tone: direct, practical, slightly wry. No filler. No "in this lesson we will…"

## 4. CURRICULUM MAP (source of truth: ELT365_00_MASTER_PLAN.md)

| Month | Days | Topic | Status |
|---|---|---|---|
| 1 | 001–031 | Foundations: learners & learning | ✅ written |
| 2 | 032–059 | Grammar core | ✅ written |
| 3 | 060–090 | Grammar advanced | ✅ written |
| 4 | 091–120 | Vocabulary / lexis | ✅ written |
| 5 | 121–151 | Phonology / pronunciation | ✅ written |
| 6 | 152–181 | Receptive skills (listening, reading) | ⬜ |
| 7 | 182–212 | Productive skills (speaking, writing) | ⬜ |
| 8 | 213–243 | Classroom management | ⬜ |
| 9 | 244–273 | Lesson planning | ⬜ |
| 10 | 274–304 | Error correction, feedback, assessment | ⬜ |
| 11 | 305–334 | Materials & technology | ⬜ |
| 12 | 335–365 | Professionalism & specialisms (D347 = English for hospitality) | ⬜ |

Per-day titles for ALL 365 days exist in the master plan — follow them; do not invent new sequencing.

## 5. GENERATION WORKFLOW (one month per session)

1. Load this skill + master plan. Read the target month's day-title list.
2. Draft all lessons for the month in one file: `ELT365_M{NN}_{TOPIC}_D{start}-{end}.md` with the standard header + disclaimer (copy from any ✅ file).
3. **Review pass (mandatory):** check each lesson for (a) word budget 55–80, (b) factual accuracy vs source canon, (c) no certification claims, (d) format compliance, (e) Try-task ≤2 min.
4. Update the Status column above (mark ✅).
5. Output file to /mnt/user-data/outputs/ and present to user.

## 6. PUBLISHING PIPELINE

- **Endpoint:** `POST https://www.sourovdeb.com/wp-json/sourov/v1/ai-post`
- **Auth:** header `X-Sourov-Key` (value stored as GAS Script Property `SOUROV_KEY` — never hardcode in files destined for GitHub).
- **Payload:** `{title, content (HTML), status, category, tags, meta_description, seo_title, date (ISO)}`
- **Conventions:** title `ELT365 · Day NNN — {Title}` · category `English Teaching` · tags `ELT365, teacher training, ELT` + one topic tag · status `publish` (via daily trigger) · schedule 09:00 Réunion (UTC+4).
- **Publisher script:** ELT365_DAILY_PUBLISHER.gs (GAS, no Sheets, PropertiesService day counter, Rhino-safe `var`-only syntax, `followRedirects:false`, domain must be `www.sourovdeb.com`).
- Distinct from the existing "60-Day ELT Masterclass" series on the site — never reuse its titles.

## 7. UPGRADE / EXTENSION PATHS (future use)

- **YouTube Shorts:** each lesson ≈ 45-sec script. Conversion rule: Idea = hook + body, Example = visual/on-screen text, Try = call-to-action. Batch-generate scripts month by month after channel name confirmed.
- **Email course:** same content, one lesson/day via GmailApp drip (reuse publisher's parser; swap UrlFetchApp for GmailApp.sendEmail).
- **PDF compilations:** monthly e-books (12 lead magnets) — generate from MD via pdf skill; add cover + disclaimer page.
- **Translations:** French edition (ELT365-FR) viable given author's C1; keep English terminology for ELT jargon.
- **Year 2 sequel:** advanced track (Delta-syllabus-inspired) — same trademark rule applies to "Delta."
- **License:** decision pending — CC BY 4.0 (max spread) vs CC BY-NC 4.0 (blocks commercial reuse). Flag to user before mass publication.

## 8. QUALITY GATES (refuse to ship if any fail)

- [ ] No "certified/qualified/awarded" anywhere
- [ ] Disclaimer present in file header
- [ ] Every claim traceable to source canon
- [ ] All day numbers match master plan
- [ ] Word budget respected
- [ ] File saved with exact naming convention
