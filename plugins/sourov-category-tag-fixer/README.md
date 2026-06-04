# Sourov Category & Tag Auto-Fixer

A WordPress plugin that automatically fixes missing or incorrect categories and tags on all posts.

## What it fixes

- Posts stuck in "Uncategorized" → assigns the best matching category based on content keywords
- Posts with no tags → automatically generates tags from content keywords
- Creates categories that don't yet exist in WordPress

## Installation

1. Upload the `sourov-category-tag-fixer/` folder to `wp-content/plugins/`
2. Activate in WordPress admin under Plugins
3. Go to Settings → Sourov Fixer
4. Set your API key (must match the `X-Sourov-Key` you use in your scripts)

## REST API Endpoints

All endpoints require the `X-Sourov-Key` header.

| Method | Endpoint | Action |
|--------|----------|--------|
| `GET` | `/wp-json/sourov/v1/preview-fixes` | Dry run — shows what would be changed |
| `POST` | `/wp-json/sourov/v1/fix-posts` | Bulk fix all posts |
| `POST` | `/wp-json/sourov/v1/fix-post/{id}` | Fix one post by ID |

## Category Rules

The plugin auto-assigns categories based on keyword counts:

| Category | Keywords |
|----------|----------|
| Grammar | grammar, tense, verb, noun, modal |
| Listening & Phonology | listening, pronunciation, phonology |
| Speaking & Fluency | speaking, fluency, conversation |
| Vocabulary | vocabulary, lexis, collocation |
| CELTA | celta, lesson plan, teaching practice |
| ELT Masterclass | default fallback |

## Quick Fix (Python)

```python
import requests

headers = {'X-Sourov-Key': 'YOUR_API_KEY'}
base = 'https://sourovdeb.com/wp-json/sourov/v1'

# Step 1: See what will change
print(requests.get(f'{base}/preview-fixes', headers=headers).json())

# Step 2: Apply fixes
result = requests.post(f'{base}/fix-posts', json={'limit': '200'}, headers=headers)
print(f"Fixed {result.json()['fixed_count']} posts")
```
