# LLM Process and Automation Playbook

## Objective
Build and operate an automated WordPress publishing system inspired by the PostFlow control panel UX, with reliable scheduling, AI enrichment, and safe execution workflow.

## Non-Negotiable Operating Rules
1. Think before execute.
2. Keep responses token-efficient and outcome-focused.
3. Use surgical scripts instead of manual command chains.
4. Verify each step and fine-tune only where needed.
5. Commit and push small, traceable increments.

## Standard Delivery Loop
1. Intake and Read-Only Audit
- Confirm repository state, branch, and baseline files.
- Read docs and API references before implementation.

2. Minimal Plan
- Define smallest end-to-end slice to implement.
- List exact files and expected outputs before edits.

3. Scripted Execution
- Create one strict script per objective.
- Keep side effects narrow and explicit.

4. Verification
- Check generated artifacts, runtime checks, and command exit codes.
- Capture evidence (key output, changed files, and commit hash).

5. Fine-Tune
- If verification fails, patch only affected parts.
- Rerun only the relevant script/checks.

6. Publish
- Commit with clear message.
- Push branch and open PR when ready.

## Reference Architecture
1. VS Code Extension Layer
- UI and orchestration (dashboard, posts, calendar, automation, settings).

2. Automation Engine Layer
- Queue ingestion (CSV/JSON/Sheets).
- AI SEO enrichment.
- Smart scheduling and conflict avoidance.
- WordPress REST posting and rollback.

3. WordPress Integration Layer
- Application Password authentication.
- /wp-json/wp/v2 endpoints for posts, tags, categories, media.
- Optional SEO plugin metadata mapping.

## Build Phases
1. Foundation
- Stabilize extension structure, commands, and settings persistence.

2. WordPress Core Integration
- Connection test, posts list, draft/future publish, delete.

3. AI + SEO Pipeline
- Provider abstraction (Claude, DeepSeek, Ollama).
- Structured SEO field generation and validation.

4. Scheduler and Queue
- Deterministic slot assignment and conflict prevention.
- Dry-run mode and rollback behavior.

5. PostFlow UX Alignment
- Dashboard metrics, calendar rescheduling, automation cards, settings parity.

6. Hardening
- Error handling, logging, retries, and smoke checks.

## Definition of Done
- Connection test succeeds.
- Generate -> review -> schedule/publish flow works.
- Queue pipeline handles multiple posts without collisions.
- At least one dry-run and one real run verified.
- Branch contains docs, scripts, and reproducible setup notes.
