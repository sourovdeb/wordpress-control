---
description: "Use when building, automating, debugging, or operating this repository. Enforce think-before-execute planning, token-efficient communication, script-first execution, and verification-driven fine-tuning."
name: "LLM Surgical Execution Protocol"
applyTo: "**"
---
# LLM Surgical Execution Protocol

- Think before execute: decide the smallest safe sequence before running commands.
- Be token efficient: use short progress updates and avoid repeating unchanged context.
- Prefer script-first execution for multi-step work; avoid ad-hoc command chains.
- Use strict shell scripts for operational tasks:
```bash
#!/usr/bin/env bash
set -euo pipefail
```
- Follow this structure in each script:
  1) Pre-checks
  2) Targeted change
  3) Verification
- Validate every run with explicit checks: exit code, expected files, and key state.
- If results are partial, fine-tune only the failing step and rerun minimally.
- For risky operations, include both pre-check and post-check in the same script.
- Keep scripts idempotent when possible.
- Prefer one focused script per objective.
