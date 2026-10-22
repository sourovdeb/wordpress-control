# Complete Guide to Free AI Tools You Can Use Right Now
**Work with Claude, ChatGPT, Mistral, and Ollama without paying**

---

## Overview: What You Have Access To

| Tool | Free Tier | How to Use | Best For |
|---|---|---|---|
| **Claude (This session)** | Via Anthropic API in code | Already available in repos | Writing, analysis, code |
| **ChatGPT Free** | web.openai.com | Browser, no login required | Questions, brainstorming |
| **Claude.ai** | 3-20 messages/day | Browser | Same as ChatGPT but with better memory |
| **Mistral Free** | mistral-small via API | Free tier API | Fast, lightweight, coding |
| **Ollama** | Fully free, runs locally | Download + run locally | Private, offline, no API cost |
| **Gemini Free** | google.com/gemini | Browser | Google integration, free tier |

---

## 1. Claude (The One You're Using Now)

### What This Is
This session you're in? **You're already using Claude for free via your current GitHub session.**

Every message you write is processed by Claude (Haiku model — the fastest, most efficient).

### How It Costs $0 Right Now
- Your session is paid for through this automated environment
- You're not spending your own API credits
- This is an unlimited session while it lasts

### How to Use Claude When This Session Ends
**Option A: Claude.ai (Web)**
```
Visit: https://claude.ai
Create free account
Get 3-20 messages per day free
(Upgrade to Claude+ for unlimited)
```

**Option B: Via API (Programmatically)**
If you want to use Claude in your scripts (like we did in the WordPress tools):

```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-...")  # Your free trial API key
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a blog post about teaching grammar"}
    ],
)
print(message.content[0].text)
```

**Cost:** Free trial includes ~$5 in credits. Then ~$0.005 per 1000 tokens (cheap).

### Best Use Cases
- Writing blog posts (we're using this for your automation)
- Content editing and improvement
- Code generation and debugging
- Strategic planning
- Long-form analysis

### Why Use Claude Over ChatGPT?
- Better at following instructions precisely
- Longer context window (can handle bigger documents)
- More honest when it doesn't know something
- Better at code and structured output (JSON, markdown)

---

## 2. ChatGPT Free (web.openai.com)

### No Account Needed? 
Sort of. You can ask questions without signup, but limited responses. Full features need free OpenAI account.

### Free Tier Details
- Unlimited conversations (no daily limit)
- Access to GPT-4 (sometimes) and GPT-3.5
- No plugins, no memory between conversations
- Can download chat history

### How to Use
```
1. Visit: https://chat.openai.com
2. Click "Sign up with Google" (faster)
3. Start chatting
```

### Best Use Cases
- Quick questions
- Brainstorming (very good at this)
- Explaining concepts
- General assistance
- When you need fast response

### Cost
Free tier:
- Unlimited conversations
- Full access to GPT-4 (during free tier periods)
- No payment needed

Paid ($20/mo):
- Faster responses
- Priority access
- More usage

---

## 3. Claude.ai (Browser)

### What It Is
The official Claude interface in your web browser.

### Free Tier
- 3-20 messages per day
- Can ask complex questions
- Memory of conversations in one chat
- But limited usage per day

### How to Use
```
1. Visit: https://claude.ai
2. Sign up with Google or email
3. Start typing
4. Hit 3-20 messages → wait for reset (24h)
```

### Cost Comparison
| Feature | Free | Claude+ ($20/mo) |
|---|---|---|
| Messages per day | 3-20 | Unlimited |
| Model access | Latest Claude | Latest + older |
| File uploads | 5 files | Unlimited |
| Projects | 1 | Unlimited |
| Long context | Partial | Full (200k tokens) |

### Best Use Cases
- When you have complex questions (better than ChatGPT)
- When you need to upload files and ask about them
- Serious work where quality matters

**Our Recommendation:**
If you use Claude once a day, free tier is fine.
If you use it multiple times daily, Claude+ ($20/mo) is worth it.

---

## 4. Mistral Free (Lightweight, Fast)

### What It Is
A French AI company that gives away free API access to their models.

### Free Tier
- 5,000 messages/month (very generous)
- Fast responses
- Good for code
- Via API (programmatically)

### How to Use (Programmatically)

```python
import requests

url = "https://api.mistral.ai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {MISTRAL_FREE_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "mistral-small",
    "messages": [
        {"role": "user", "content": "Write a poem about coding"}
    ]
}

response = requests.post(url, json=data, headers=headers)
print(response.json()['choices'][0]['message']['content'])
```

### Free Tier Limits
- 5,000 messages/month = ~165 messages/day
- That's more than enough for most use cases
- Rate-limited to 10 requests/second
- No video/images, just text

### Cost After Free Tier
- Pay-as-you-go: ~$0.10 per 1M input tokens
- Much cheaper than Claude or ChatGPT

### Best Use Cases
- Integrating AI into scripts (like our WordPress tools)
- When you need a reliable API that's free
- Coding assistance
- Quick text generation
- Content calendar automation (what we built)

### Sign Up
```
1. Visit: https://console.mistral.ai
2. Create free account
3. Get API key
4. Use in code
```

---

## 5. Ollama (Private, Offline, Truly Free)

### What It Is
Download AI models to run locally on your computer.
No internet needed after setup.
No company watching you.
No API cost.

### How It Works
```
1. Download Ollama: https://ollama.ai
2. Install (Mac/Linux/Windows)
3. Run a model locally:
   ollama run llama2
4. Chat with it in terminal or web UI
5. Use it in your code
```

### Free Models Available
- **llama2** (Meta) — 7B parameters, good general purpose
- **mistral** (Mistral) — fast, good for coding
- **neural-chat** — conversation focused
- **dolphin-mixtral** — more intelligent, bigger
- **codellama** — specialized for code

### System Requirements
- **Minimum:** 8GB RAM, 10GB disk
- **Better:** 16GB RAM, 20GB disk
- Works on Mac, Linux, Windows, WSL

### Cost
- Free (one-time download)
- Uses your computer's power (electricity cost negligible)
- Private — nothing leaves your computer
- Offline — works without internet

### Example: Using Ollama in Code

```python
import requests

# Ollama runs locally on port 11434
url = "http://localhost:11434/api/generate"

response = requests.post(url, json={
    "model": "mistral",
    "prompt": "Write a blog post about teaching English",
    "stream": False
})

print(response.json()['response'])
```

### Best Use Cases
- **Sensitive content** (medical, mental health) — stays on your computer
- **Offline work** — no internet dependency
- **Cost optimization** — free after setup
- **Learning** — understand how LLMs work
- **Privacy-first projects** — GDPR compliant

### Our WordPress Integration (Using Ollama)
In `extension.js`, we support Ollama:

```javascript
if (provider === 'ollama') {
  const res = await fetch('http://localhost:11434/api/generate', {
    method: 'POST',
    body: JSON.stringify({
      model: 'mistral',
      prompt: userPrompt,
      stream: false
    })
  });
  return res.json().response;
}
```

---

## 6. Google Gemini Free (Integrated with Google)

### What It Is
Google's AI, integrated into Gmail, Docs, and Google account.

### Free Tier
- Unlimited basic questions
- Limited advanced features
- Integration with Google Workspace
- Free with Google account

### How to Use
```
1. Visit: https://gemini.google.com
2. Use your Google account (auto-login)
3. Ask questions
```

### Cost
- Free basic tier
- Gemini Advanced ($20/mo with Google One)

### Best Use Cases
- If you already live in Google Workspace
- Gmail writing assistance
- Google Docs collaboration
- Integrated with your calendar/docs

### Why Choose It?
- Seamless Google integration
- Already have the account
- Good for quick questions
- Mobile app available

---

## 7. Combining Free AI Tools (The Smart Way)

### Strategy: Never Pay, Always Have Options

```
Monday: Use Claude free tier (3 messages)
        → Ask strategic questions

Tuesday: Use ChatGPT free (unlimited)
         → Brainstorm, get ideas

Wednesday: Use Mistral API (free 5000/month)
           → Generate content automatically

Thursday: Use Ollama locally (truly free)
          → Code generation, private work

Friday-Sunday: Use leftover from the week
```

### Real Workflow For Your Blogging

```
Monday-Tuesday:
  - You: Write outline in Google Docs
  - ChatGPT: Brainstorm 10 post titles
  - Claude: Pick best title, expand to outline

Wednesday:
  - Mistral API (automatic): Generate first draft
  - You: Edit and improve
  - Ollama (local): Generate SEO keywords

Thursday:
  - You: Final review
  - ChatGPT: Proofread for grammar
  - Schedule via Google Sheets

Friday:
  - Blog auto-publishes (via our system)
  - You: Relax, no more work
```

---

## 8. Setting Up Your Free AI Toolkit

### Quick Start (15 minutes)

1. **Create ChatGPT Free account**
   ```
   https://chat.openai.com
   Sign up with Google
   Bookmark it
   ```

2. **Create Claude.ai Free account**
   ```
   https://claude.ai
   Sign up with Google
   Bookmark it
   ```

3. **Get Mistral Free API key**
   ```
   https://console.mistral.ai
   Create account
   Create API key
   Save it to: ~/.mistral_key
   ```

4. **Install Ollama (optional, advanced)**
   ```
   https://ollama.ai/download
   Download and install
   Run: ollama pull mistral
   Bookmark: http://localhost:11434
   ```

### Total Cost: $0
### Total Setup Time: 15 minutes
### Monthly Access: All models, unlimited questions

---

## 9. Using Free AI in Your Automation

### Example: Wordpress Publisher + Free AI

We built your tools to work with **any** free AI:

```python
# tools/wp-desktop.py already supports:
- Claude (free tier)
- DeepSeek (free tier)
- Ollama (truly free, local)

# You can choose which to use:
config.json:
  "ai_provider": "claude"   # Uses Claude's free API
  # OR
  "ai_provider": "ollama"   # Uses local Ollama (no API key needed)
```

### Example: Sheets Publisher + Free AI

In your Google Sheets automation:

```javascript
// Mistral FREE API call
function autoFillSEO(title, content) {
  const payload = {
    model: "mistral-small",
    messages: [{
      role: "user",
      content: `Title: "${title}"\nGenerate SEO tags and description`
    }]
  };

  const response = UrlFetchApp.fetch(
    'https://api.mistral.ai/v1/chat/completions',
    {
      headers: {
        'Authorization': 'Bearer ' + MISTRAL_FREE_KEY,
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify(payload)
    }
  );

  return JSON.parse(response.getContentText());
}
```

**This uses Mistral's free tier (5000 messages/month).**
**Cost: $0**

---

## 10. Comparison Chart: Which to Use When

| Need | Tool | Why | Cost |
|---|---|---|---|
| Quick question | ChatGPT | Fast, accurate, free tier good | Free |
| Complex analysis | Claude | Better understanding | Free (limited) |
| Automation/API | Mistral | Good free tier, fast API | Free (5k/mo) |
| Private/Offline | Ollama | Runs locally, truly free | Free |
| Google integration | Gemini | Already in Gmail/Docs | Free |
| Content generation | All of above | Mix and match | Free |
| Long documents | Claude+ | 200k context window | $20/mo (optional) |
| Daily heavy use | ChatGPT+ or Claude+ | Unlimited | $20/mo each |

---

## 11. Real-World Scenario For You

### Your Weekly Content Workflow (All Free)

**Monday (30 min):**
- You: Write blog post outline
- ChatGPT Free: Suggest 5 titles
- Cost: $0

**Tuesday (30 min):**
- You: Draft full blog post
- Claude.ai Free: Review structure (use 1 message)
- Cost: $0

**Wednesday (20 min):**
- Mistral API (automatic): Generate SEO keywords and tags (use 1 API call)
- You: Review and approve
- Cost: $0

**Thursday (10 min):**
- You: Add to Google Sheets with Status=READY
- Cost: $0

**Friday (1 sec):**
- Ollama (local): Checks Sheets, generates final metadata
- WordPress: Auto-publishes
- You: Do nothing
- Cost: $0

### Weekly Cost: $0
### Weekly Time Spent: 1.5 hours (you writing)
### Posts Published: 4-5
### Content Quality: Professional (AI-assisted, human-reviewed)

---

## Money-Saving Tips

1. **Use free tiers first** — All APIs offer free tier. Exploit it.
2. **Use Ollama for testing** — Free locally, use cloud API only for production
3. **Batch operations** — Generate 5 articles at once = cheaper per article
4. **Cache results** — Ask Claude once, use answer many times
5. **Use cheaper models** — Mistral-small = fast + cheap vs Claude-opus

---

## The Best Setup For You

### If you have minimal budget ($0)
Use:
- ChatGPT Free (unlimited conversations)
- Claude.ai Free (3-20/day for complex work)
- Mistral Free API (5000 messages/month)
- Ollama local (truly free)

**Monthly cost: $0**
**Limitation: Daily message limits, but enough for most**

### If you can spend $10/month
Add:
- Mistral Paid API (~$5)
- Extra buffer

**Monthly cost: $10**
**Benefit: No daily limits on Mistral**

### If you can spend $20/month
Choose ONE:
- Claude+ ($20) — Best for analysis + writing
- ChatGPT+ ($20) — Most versatile
- Mistral Paid ($5) + OpenAI Pay-as-you-go

**Monthly cost: $20**
**Benefit: Unlimited access to one top-tier model**

### If you can spend $40/month (Ultimate)
Get:
- Claude+ ($20)
- ChatGPT+ ($20)

**Monthly cost: $40**
**Benefit: Best of both. Use Claude for writing, ChatGPT for questions.**

---

## Quick Links

- **ChatGPT Free:** https://chat.openai.com
- **Claude.ai Free:** https://claude.ai
- **Mistral Free API:** https://console.mistral.ai
- **Ollama:** https://ollama.ai
- **Google Gemini:** https://gemini.google.com

---

## Summary

You have **unlimited access to world-class AI** for $0-20/month.

The only limit is your creativity in using it.

Start with free tiers.
Combine multiple tools.
Never pay for something you haven't tried first.

You've got this.

