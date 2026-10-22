# SKILL: Memory-Elicitation Biographical Interview
**Version:** 1.0 | **Created:** 7 June 2026 | **Scope:** Eliciting accurate, detailed, episodic life-story material from a person, for biography / research papers / blog / video.

---

## OVERVIEW

Use this skill to build a question set that pulls **specific, sensory, single-event memories** out of a person — instead of the vague summaries people default to. It is engineered on autobiographical-memory science, not intuition, and includes safeguards against the confabulation that leading interviews (and AI interviewers especially) cause. Produces two outputs: **fact-anchored questions** (drill into a known record) and a **Self-Authoring / Life-Story epoch scaffold** (free generation).

---

## TRIGGER CONDITIONS

Activate when the user wants to:
- Write or extend a biography, memoir, autoethnography, or "about me" narrative.
- Interview themselves or another person for life-story content (papers, blog, YouTube).
- Fill gaps in an existing life-record that reads thin, generic, or all-summary.
- Especially when the subject has **depression, PTSD/C-PTSD, or childhood-abuse history** (these cause Overgeneral Memory — see Rule 2).

---

## MODULE 1 — PRE-WORK (before writing any question)

```
1. Read all existing biographical material on file.
2. Build a KNOWN vs MISSING table: for each life-domain, what is documented vs blank.
   Domains: childhood texture/joy; each major relocation; addiction/recovery;
   work/craft; partner (meeting, courtship, key day); children; belonging/identity;
   family-of-origin now; a neglected craft/hobby; religion/spirituality;
   worldview/values; the most recent defining conflict.
3. Mark every fact as DOCUMENT-fixed or RECOLLECTION-only. Never collapse the two.
4. The MISSING column = the question targets. Do not re-ask what is already known.
```

---

## MODULE 2 — THE SIX DESIGN RULES (each changes phrasing)

```
RULE 1 — CUE-DRIVEN (Conway, Self-Memory System).
  Lead every question with a concrete anchor: a smell, sound, object, weather,
  or who was in the room. Never lead with a theme. Anchors trigger fast direct
  retrieval; themes force slow generative search and yield summaries.

RULE 2 — DEFEAT OVERGENERAL MEMORY (Williams; CaR-FA-X).
  Depression + PTSD + abuse history make people recall CATEGORIES, not episodes,
  and it is WORST for positive memories. So:
    - demand ONE event, ONE place, ONE day, lasting under a day;
    - over-sample POSITIVE single episodes (hardest + usually missing).
  Phrase: "pick one time you can still see," not "what was it like."

RULE 3 — TARGET THE BUMP (reminiscence bump; immigrant second bump).
  Weight questions to ages ~10–30, to FIRST-TIMES, and to TRANSITIONS
  (each migration, each role change). These hold the self-defining scenes.

RULE 4 — NON-LEADING / ANTI-CONFABULATION (Loftus; arXiv 2408.04681:
  AI interviewers amplify false memories).
    - Open what/where/who/how. Never "did you feel X?" or "was it Y?"
    - Never supply a detail the subject didn't say.
    - "I don't remember" and "I'm not sure that's real" are VALID answers.
    - Include 2–3 prompts that surface invented/borrowed memory directly
      (family-told stories; memories that changed across tellings).

RULE 5 — COGNITIVE-INTERVIEW ENGINE (Fisher & Geiselman) for stuck memories.
    (a) Context reinstatement: return to scene — weather, body-state, who was near.
    (b) Report everything, trivial included; explicit "do not guess."
    (c) Change order: recall backwards or from a midpoint.
    (d) Change perspective: describe as another person present saw it.
  Highest yield: (a)+(b). The "do not guess" instruction is the confabulation brake.

RULE 6 — EVENT BEFORE MEANING (McAdams LSI; Self-Authoring).
  Capture the raw episode first. Ask what it meant only AFTER.
  Interpretation contaminates episodic detail if asked first.
```

---

## MODULE 3 — OUTPUT STRUCTURE (always produce both)

```
SET 1 — FACT-ANCHORED
  For each MISSING gap, write 3–5 questions, each using a KNOWN fact as the cue,
  drilling into the missing interior. Organise by gap. No invented content.

SET 2 — EPOCH SCAFFOLD (Self-Authoring + McAdams)
  - Propose 5–7 epochs derived from the subject's own documented chronology
    (personalised scaffold, not a generic template).
  - Per epoch: >=4 experiences via four cue-types, >=1 positive:
       A. a single day  B. a first time  C. an object/smell  D. a forced positive.
  - Per experience, three layers: [event only] / [effect on world & people] /
       [effect on trust, hope, self-worth, personality].
  - Cross-epoch key scenes (answer once): high point, low point, turning point,
       positive + negative childhood memory, vivid adult memory, wisdom event,
       spiritual/mystical.
  - Future script: next chapter, 5-year scene, the one-sentence life project.
  - Reconstruction prompts (last): a borrowed family story; a memory that changed;
       one event you're unsure really happened.
```

---

## MODULE 4 — INTERVIEW CONDUCT & CAPTURE

```
CONDUCT
  - One cue per question. Wait. Never stack questions.
  - If stalled: reinstate context (Rule 5a) — never offer a guess to confirm.
  - Capture the event verbatim before asking meaning.
  - Date every session.

CAPTURE FORMAT (reusable for papers/blog/video)
  EPOCH · TITLE · DATE-OF-TELLING · [event verbatim] / [effect] / [uncertainty flag]
  If a later telling differs, LOG BOTH — the change is data, not error.

PACING & SAFETY
  - One epoch per sitting; sleep between sessions (aids consolidation).
  - For trauma/bipolar/insomnia profiles: keep rhythm rules; schedule heavy scenes
    near professional support, not late at night. Stop if flooded.
  - Frame (McAdams): "the story is selective; there are no right or wrong answers;
    this is not a diagnosis." Reduces defensiveness and demand characteristics.
```

---

## SOURCES
Conway & Pleydell-Pearce (2000); Conway (2005) — Self-Memory System.
Williams & Broadbent (1986); Williams et al. (2007) — Overgeneral Memory / CaR-FA-X.
Munawar, Kuhn & Haque (2018), PLOS ONE — reminiscence bump review.
Loftus (1974–2005) — misinformation effect; arXiv 2408.04681 (2024) — AI false-memory amplification.
Fisher & Geiselman (1992) — Cognitive Interview.
McAdams (2007) — Life Story Interview-II.
