# SKILL_orwell_lesson_essay
**Version:** 1.0 · **Date:** 2026-06-13 · **Inherits:** SKILL_COMMON_CORE (§2 language, §3 evidence, §4 sources, §5 style, §7 privacy, §8 safety) · **Registry #:** 43
**Purpose:** Turn any project resource into one of two outputs — (A) an **essay/memoir in George Orwell's plain style**, or (B) a **CELTA-style English lesson**. Topics: ELT/CELTA teaching, memoir, or anything in the corpus. Supersedes nothing; extends `SKILL_portfolio_to_essays_v1` with an explicit Orwell voice-spec and a full lesson-builder. Any agent can run it against the uploaded project and produce teaching material or publishable prose.

## When to use
- "Write me an essay / blog / memoir piece on X" → **Mode A**.
- "Make me a lesson / teaching material / worksheet on X" → **Mode B**.
- "Turn this paper/biography/case into a post / a class" → A or B per request.
## When not to use
- Legal letters, complaint emails, applications → use the regulatory/career skills (registry #17–24, #1–9).
- Research-paper drafting → #25. Pure proofread/edit of supplied text → `writing.md`.

## Inputs (resolve before writing; ask **one** consolidated question only if ≥2 unknown)
Mode (A/B) · topic · source files (default: let SOURCE MAP pick) · audience · length · language (EN default; FR on request) · for Mode B also: learner level (CEFR A1–C2) and lesson focus (grammar / lexis / a skill).

## SOURCE MAP (write from these — never invention; §4)
| Topic | Pull from | Default mode |
|---|---|---|
| ELT / teaching craft | CELTA evidence + practice notes, JEFL_Paper, Disclosure_and_Adjustment_Autoethnography | B (lesson) or A (craft essay) |
| Memoir / life | BIOGRAPHY_SOUROV_DEB, BIOPIC_PART_TWO, TRANSCRIPT_LIFE_STORY, 07_ABOUT_ME, my_dysfunctional_family, myboss | A |
| System critique (CELTA/disclosure) | SOUROV_MASTER_LEGAL_FILE, When_the_Certificate_Fails_You, appeal docs — **documented facts only** | A |
| Method / "how I work" | naming-convention, organizer, GMAIL_EMAIL_ARCHAEOLOGY, campaign/bounce analysis | A |
| Languages / craft | DCL/C1 notes, code-switching material | A or B |
| Routine / pattern | STABILITY_PROGRAM (published-safe framing only; §8) | A — no clinical content |
If a concrete scene or sensory detail is missing, elicit it (SKILL_memory_elicitation_interview) — do not fabricate (§3, §4).

---

## PART A — ORWELL VOICE SPEC (apply to Mode A; recommended for Mode B rubric/handout prose)
Source: George Orwell, *Politics and the English Language* (1946). Operationalised:

**The six rules, as edit passes (run in order):**
1. **Kill stale figures.** Cut any metaphor/simile you have seen in print. Either make a fresh, exact image or state it plainly.
2. **Short word beats long.** "use" not "utilize", "help" not "facilitate", "now" not "at this point in time".
3. **Cut every word you can.** If the sentence survives the cut, the word was dead weight.
4. **Active over passive.** "The centre altered the record", not "the record was altered".
5. **No jargon, foreign tag, or scientific word where an everyday English one exists.** If a term must stay, define it once in plain words.
6. **Break any rule before writing something barbarous.** Clarity and truth outrank the list.

**Five deeper principles (the part that makes it Orwell, not just clean copy):**
- **Concrete over abstract.** Replace "values", "issues", "experience" with the specific thing seen, dated, named. A casino floor at 3 a.m., not "the hospitality sector".
- **Prose like a windowpane.** The reader should see the thing, not your style. No throat-clearing, no decoration.
- **Implicate yourself.** Orwell indicts the narrator, not only others. Memoir earns trust by admitting the writer's own failure or doubt.
- **The particular carries the general.** One exact scene proves the argument better than a paragraph of claims.
- **Refuse euphemism.** Name the act. This is also why §3 matters: in case-related pieces, the plain documented fact, never a softened or motive-loaded version.

**Anti-patterns (auto-reject):** AI-giveaway phrases (delve, navigate the landscape, moreover, in today's world, it's important to note); abstraction stacks; passive evasion; adjectives doing the work a fact should do; a "remembered" detail the owner never supplied.

---

## PART B — CELTA LESSON SPEC (apply to Mode B)
**Pick a framework by lesson type:**
- **PPP** (Presentation → Practice → Production) — discrete grammar/lexis at lower levels.
- **TTT** (Test → Teach → Test) — when learners may already half-know the item; diagnose first.
- **TBL** (Task-Based) — communicative outcome drives the lesson; language emerges from the task.
- **ESA** (Engage → Study → Activate, Harmer) — flexible alternative.
- **Receptive skills** (reading/listening): lead-in → set context → pre-teach blocking vocab → **gist task** (one question, whole text) → **detailed task** (specific info) → response/freer productive follow-up.
- **Productive skills** (speaking/writing): lead-in → model + analyse → prepare → **task** → content + language feedback.

**Lesson-plan skeleton (fill every field; this is the deliverable for Mode B):**
- **Main aim** (one, learner-facing: "by the end, learners can …").
- **Subsidiary aims** (skills/sub-skills practised).
- **Personal aim** (one thing the teacher works on).
- **Target language analysis — MFPA:** Meaning (concept + a CCQ or two), Form (structure on the board), Pronunciation (stress, weak forms, connected speech), Appropriacy (register/when used).
- **Anticipated problems & solutions** — split: (i) with the language (meaning/form/pron), (ii) with learners/tasks (logistics, level spread) — each with a concrete solution.
- **Procedure table:** Stage | Stage aim | Procedure | Interaction (T-S / S-S / S-T) | Time. Keep **STT > TTT** (student talking time over teacher talking time).
- **Materials** + answer key.

**Technique checklist (must appear where relevant):**
CCQs (check meaning, not "do you understand?") · ICQs (check instructions before a task) · eliciting before telling · drilling (choral then individual) for new pron · grade your language to level · stage instructions one step at a time · error correction (on-the-spot vs delayed; reformulation vs prompting) · clear context before form.

---

## PROCEDURE — Mode A (essay / memoir)
1. Pick topic; pull ONLY mapped files; **re-read them**.
2. Tag every concrete claim `DOCUMENTED` / `RECOLLECTION` (§3).
3. Boundary pass (§7, blocking): anonymise living private individuals; child via parenthood only; proceedings → documented facts, no motive.
4. CELTA language guard (§2) on any certificate mention.
5. Draft to shape: **hook = one lived, dated scene (80–120 w)** → one idea → one piece of evidence/scene → practical takeaway → one-line close. One idea per essay; surplus ideas seed the next.
6. Run the six rules (Part A) as ordered edit passes, then the five principles, then anti-pattern reject.
7. Output: markdown + SEO title + meta description ≤155 chars. To WordPress only as `draft` (§1); owner publishes.

## PROCEDURE — Mode B (lesson)
1. Resolve level + focus; pull mapped source for the content/text.
2. Choose framework (Part B) and state why in one line.
3. Build the lesson-plan skeleton — every field filled, MFPA done, CCQs/ICQs written out, anticipated problems paired with solutions.
4. Produce learner-facing materials + answer key. If a reading/listening text is needed and none is on file, write an original level-graded text (don't reproduce copyrighted material).
5. CELTA language guard (§2) anywhere the qualification is referenced in rubric/bio.
6. Output: ready-to-teach lesson plan + materials (markdown; optional PDF via `wiki/tools.md` Python). Optionally feed into a "teaching craft" essay (Mode A) for the blog.

---

## TOPIC BANK (ready, mapped)
**Essays (Mode A):**
1. What a casino floor taught me about teaching English under pressure. [memoir+craft]
2. The certificate is not the competence — 120 supervised hours, what they built. [§2 guard mandatory]
3. Disclosure without demand — 900-word public version of the autoethnography. [research→public]
4. Email archaeology: rebuilding a career from fifteen years of sent mail. [method]
5. Verified beats clever — what a bounced email campaign proved. [method+data]
6. Learning French to C1 as an adult. [memoir]
7. Four languages in one head. [memoir]
8. From Sydney to Saint-Pierre — one relocation scene. [memoir, anonymised]
9. Paperwork as evidence — the habit, not the case. [facts only]

**Lessons (Mode B):**
10. A1 lexis — "jobs and workplaces" (PPP), text drawn from the hospitality material.
11. B1 reading — a graded text on relocation; gist + detail tasks (receptive framework).
12. B2 functional language — disagreeing politely (TBL); roleplay outcome.
13. C1 writing — the personal essay; model + analyse + draft (productive framework), Orwell rules as the editing rubric. [bridges A and B]
14. Teacher-training micro-lesson — writing effective CCQs, with worked examples.

---

## SELF-CHECK (before delivering)
- [ ] Mode matched the request (essay vs lesson).
- [ ] Every concrete claim is DOCUMENTED or labelled RECOLLECTION; nothing invented (§3).
- [ ] Boundary pass done; no named private individual, child referenced only via parenthood (§7).
- [ ] CELTA language guard passed — no "certified/awarded/obtained/certifié" (§2).
- [ ] Mode A: opens on one dated scene; six rules + five principles applied; no anti-pattern phrases.
- [ ] Mode B: every skeleton field filled; MFPA complete; CCQs/ICQs written; problems paired with solutions; STT>TTT.
- [ ] Output cited, in owner style (§5), filed not left in chat (§4).

## FAILURE MODES
- Memoir drifting into accusation: any sentence about a named party in proceedings must trace to a document, or cut it.
- Over-summary: a Mode A draft with no single dated scene fails Rule 5 of the elicitation skill — go elicit the scene first.
- Fabricated sensory/"remembered" detail: never add detail the owner did not supply.
- Lesson with vague aims or "do you understand?" checking: rewrite aim learner-facing; replace with CCQs.
- Reproducing a copyrighted text as lesson material: write an original graded text instead.
