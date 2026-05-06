# PostFlow Automation Checklist

## Environment
- Configure WordPress URL, username, and application password.
- Configure AI provider credentials (DeepSeek/Claude/Ollama).
- Confirm WordPress REST endpoint availability.

## Core Features
- Site status check from extension.
- List posts with status filters.
- Generate post JSON with AI.
- Review generated content before publishing.
- Publish now, save draft, and schedule future posts.

## Automation Features
- Queue import from CSV/JSON (Sheets optional).
- SEO enrichment and tag generation.
- Schedule assignment with conflict avoidance.
- Duplicate detection before posting.
- Rollback on partial failure.

## Verification Gates
- Dry-run pipeline succeeds with no API writes.
- Real run creates scheduled posts correctly.
- SEO fields are written for configured plugin.
- Logs capture success/failure clearly.

## Git Workflow
1. Update local base branch.
2. Create feature/docs branch.
3. Commit focused changes.
4. Push branch.
5. Open PR with validation evidence.
