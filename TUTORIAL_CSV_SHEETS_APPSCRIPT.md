# Complete Guide: CSV + Google Sheets + Apps Script
**Why Understanding This Matters For You**

---

## Table of Contents
1. **What is CSV? Why does it matter?**
2. **How Google Sheets reads and stores data**
3. **What is Google Apps Script? (It's just JavaScript)**
4. **How they work together — the complete pipeline**
5. **Real example: Publishing WordPress posts on a schedule**
6. **Why this is therapeutic for mental health automation**

---

## Part 1: What is CSV?

### The Problem CSV Solves
You have data. A lot of it. Maybe you're tracking:
- Blog post topics
- Publishing schedule
- Tasks to do
- Medication reminders
- Morning routine checklist

**Where do you store it?**

Option A: Keep it in your head.
- Problem: Bipolar and depression make memory hard. Brain fog. Fatigue.
- Result: You forget. Posts don't get published. Routine breaks.

Option B: Use Excel/Sheets manually.
- Problem: Boring, repetitive, error-prone. Requires willpower.
- Result: You stop after 2 weeks.

Option C: Use **CSV** + automation.
- Benefit: Data is stored simply, can be read by any program, can be automated.
- Result: You write ONCE. The computer does the boring part forever.

### What CSV Actually Is

**CSV = Comma-Separated Values**

It's the simplest data format in the world:

```
Title,Author,Status,Date
Day 1 Post,Sourov,READY,2026-06-10
Day 2 Post,Sourov,DRAFT,2026-06-11
Blog Post,Sourov,SCHEDULE,2026-06-15
```

That's it.
- First row = column headers (what the data is)
- Each row below = one record (one blog post, one task, one reminder)
- Commas separate the values

**Why is this useful?**

1. **Simple format** — Any program can read it (Excel, Google Sheets, Python, JavaScript, etc.)
2. **Universal** — Works across tools, no lock-in
3. **Version-controllable** — Can track changes in Git
4. **Automatable** — Computers can process it without human intervention

### CSV for Your Mental Health Workflow

Example: **Morning Routine Checklist**

```csv
Task,Frequency,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday,Notes
Wake up at 7am,Daily,✓,✓,✓,✓,✓,✓,✓,Set phone alarm
Medication,Daily,✓,✓,✓,✓,✓,✓,✓,Take with water
Breakfast,Daily,✓,✓,✓,✓,✓,✓,✓,Minimum 30 min
Journal,Daily,✓,✓,✓,✓,✓,✓,✓,Write 5 minutes
Exercise,3x/week,,✓,,✓,,✓,,"20 min walk or stretch"
```

**The benefit:**
- You can see at a glance what you did this week
- Computer can send reminders automatically
- No need to remember — it's written down
- Reduces anxiety ("Did I take my meds?" — just look at the CSV)

---

## Part 2: How Google Sheets Reads CSV

### Google Sheets IS a CSV Editor

When you open Google Sheets and type data, you're creating a CSV.

```
Google Sheets interface:
┌─────────────────────────┐
│ Title   │ Content │ Status │
├─────────────────────────┤
│ Day 1   │ Grammar │ READY  │
│ Day 2   │ Speaking│ DRAFT  │
└─────────────────────────┘

Underneath = CSV:
Title,Content,Status
Day 1,Grammar,READY
Day 2,Speaking,DRAFT
```

Google Sheets is just a **pretty interface** over CSV data.

### Reading Data From Google Sheets

When you use **Google Apps Script** (which we'll explain next), it reads from your Sheets like this:

```javascript
// Open the Google Sheet
const sheet = SpreadsheetApp.getActiveSheet();

// Get all data (like reading a CSV)
const data = sheet.getDataRange().getValues();

// Loop through rows
for (let i = 1; i < data.length; i++) {
  const row = data[i];
  const title = row[0];      // First column (Title)
  const content = row[1];    // Second column (Content)
  const status = row[2];     // Third column (Status)

  // Do something with it
  console.log(`Row ${i}: ${title} is ${status}`);
}
```

**What's happening:**
1. `.getDataRange()` reads the entire sheet as a 2D array (table)
2. `data[i]` is one row (like one CSV line)
3. `row[0]`, `row[1]`, `row[2]` are the individual cells (like comma-separated values)

---

## Part 3: What is Google Apps Script?

### It's Just JavaScript

**You're not learning a new language.** Apps Script = JavaScript + Google APIs.

JavaScript is the same language that runs in web browsers. Apps Script just adds Google-specific powers:
- Read/write to Google Sheets
- Send emails
- Make HTTP requests to external APIs (like WordPress)
- Run on a schedule automatically

### Simple Example: Read a Google Sheet

```javascript
function helloWorld() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const data = sheet.getDataRange().getValues();

  Logger.log("Data from the sheet:");
  for (let i = 0; i < data.length; i++) {
    Logger.log(data[i]); // Print each row
  }
}
```

**What this does:**
1. Opens the active Google Sheet
2. Gets all data
3. Prints it to the log (you can see output in Google Apps Script editor)

### Why This Matters For Your Mental Health

**Automation = reducing cognitive load.**

When you're bipolar or depressed:
- Decision fatigue is real
- You can't manage 10 different apps
- You need ONE source of truth

**Google Sheets + Apps Script = that one source:**
- Write data in Sheets (simple, visual, understandable)
- Apps Script reads it and does the boring work
- Everything else happens automatically

---

## Part 4: How They Work Together — The Complete Pipeline

Let's trace a real example: **WordPress Publishing Automation**

### The Setup
You have a Google Sheet with blog posts:

```
Title                      | Content              | Category      | Status   | Date
Day 16: Grammar           | <p>Grammar...</p>    | ELT Masterclass | READY   | 
Day 17: Speaking          | <p>Speaking...</p>   | ELT Masterclass | SCHEDULE | 2026-06-15T09:00
```

### What Happens Automatically (via Apps Script)

**Step 1: Apps Script reads the Sheet (CSV)**
```javascript
const data = sheet.getDataRange().getValues();
const post = data[1]; // Row 1 (first blog post)
const title = post[0];
const content = post[1];
const status = post[3];
```

**Step 2: Apps Script sends to WordPress API**
```javascript
const response = UrlFetchApp.fetch('https://sourovdeb.com/wp-json/sourov/v1/ai-post', {
  method: 'POST',
  headers: { 'X-Sourov-Key': API_KEY },
  payload: JSON.stringify({
    title: title,
    content: content,
    category: 'ELT Masterclass',
    status: status
  })
});
```

**Step 3: WordPress publishes the post (or schedules it)**
- If `status = 'publish'` → goes live immediately
- If `status = 'schedule'` → waits until the date

**Step 4: Apps Script marks it as done**
```javascript
sheet.getRange(2, 4).setValue('DONE');  // Mark row 2, column 4 as DONE
sheet.getRange(2, 5).setValue(responseData.link); // Add the URL
```

### The Magic: It All Happens On A Schedule

You set up ONE **trigger** in Apps Script:

```javascript
// Run this every hour
function createTrigger() {
  ScriptApp.newTrigger('publishPosts')
    .timeBased()
    .everyHours(1)
    .create();
}

// This function runs every hour automatically
function publishPosts() {
  // Read Sheet
  // Send to WordPress
  // Mark as done
  // Email you a report
}
```

**You write data in Sheets ONE TIME.**
**The automation handles publishing forever.**

### Complete Data Flow Diagram

```
┌─────────────────────────────┐
│   You (Human)               │
│  Write blog posts in        │
│  Google Sheets              │
│  Set Status = READY         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│   Google Sheets (CSV)       │
│  Stores: Title, Content,    │
│  Category, Status, Date     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Google Apps Script         │
│  (JavaScript running)       │
│  Every hour:                │
│  - Read Sheet               │
│  - Check Status column      │
│  - Find READY or SCHEDULE   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  WordPress API              │
│  POST /wp-json/sourov/      │
│  v1/ai-post                 │
│  Creates/schedules post     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  WordPress Website          │
│  Post published or          │
│  scheduled for future date  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  You (Human)                │
│  See post live on your      │
│  blog. No manual work.      │
└─────────────────────────────┘
```

---

## Part 5: Real Example — WordPress Publisher

This is exactly what we built for you. Let me show you how it works:

### Your Google Sheet
```
Title                    | Content                | Status   | Schedule Date    | Published URL | Notes
────────────────────────────────────────────────────────────────────────────────────────────────────────
Day 16: Grammar Teaching | <p>Grammar emerges ... | READY    |                  |               | Publish now
Day 17: Speaking Tips    | <p>When teaching ... | SCHEDULE | 2026-06-15 09:00 |               | Schedule for next week
Day 18: Listening        | <p>Authentic inputs...| DRAFT    |                  |               | Save for review
```

### The Apps Script Code

Located at: `tools/sheets-publisher.js`

```javascript
// Configuration
const WP_ENDPOINT = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const WP_API_KEY  = '0767044896thevenet_';

// Main function (runs every hour via trigger)
function runPublisher() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const data   = sheet.getDataRange().getValues();  // Read Sheet as CSV array

  for (let i = 1; i < data.length; i++) {
    const [title, content, category, status, schedDate] = data[i];  // Destructure row

    if (!title || status !== 'READY') continue;  // Skip empty or non-READY rows

    // Prepare post data
    const body = {
      title: String(title),
      content: String(content),
      category: String(category),
      status: 'publish'
    };

    // Send to WordPress
    const response = UrlFetchApp.fetch(WP_ENDPOINT, {
      method: 'post',
      headers: { 'X-Sourov-Key': WP_API_KEY },
      payload: JSON.stringify(body)
    });

    const result = JSON.parse(response.getContentText());

    // Mark row as done
    sheet.getRange(i + 1, 4).setValue('DONE');
    sheet.getRange(i + 1, 5).setValue(result.link);  // Add published URL
  }
}
```

**Line-by-line explanation:**

| Line | What it does | Why |
|------|---|---|
| `const sheet = SpreadsheetApp.getActiveSheet()` | Open the sheet | Need to read the data |
| `const data = sheet.getDataRange().getValues()` | Get all cells as CSV array | This is the "read CSV" step |
| `for (let i = 1; i < data.length; i++)` | Loop through rows | Process each blog post |
| `const [title, content, ...] = data[i]` | Extract columns | Unpack the CSV row |
| `if (!title \|\| status !== 'READY') continue` | Skip unless ready | Don't publish incomplete posts |
| `const response = UrlFetchApp.fetch(...)` | Send HTTP request to WordPress | This calls your WordPress API |
| `sheet.getRange(...).setValue('DONE')` | Mark the row as done | Update the CSV to show it's published |

### Why This Design Matters For You

**Reduces cognitive load:**
- You don't manage 5 different tools
- You have ONE Sheet with all your posts
- Script handles the boring part (formatting, API calls, scheduling)
- You can see at a glance what's published, what's scheduled, what's draft

**Forgiving for bad days:**
- Write posts during good days
- Set them to READY
- Bad day comes? Script still publishes them on schedule
- No need to remember, no willpower required

**Therapeutic:**
- Writing is creative (good for mental health)
- Automation is handled (reduces anxiety)
- You see consistent output (builds confidence)

---

## Part 6: Why This Architecture Helps With Mental Health

### The Problem We're Solving

When you're bipolar or depressed:

1. **Motivation fluctuates** — some days you can write 5 posts, some days you can't write 1 word
2. **Memory is unreliable** — "Did I publish today? When was the last post?"
3. **Perfectionism paralyzes** — "What if I make a mistake? I need it to be perfect."
4. **Hyperfocus vs. paralysis** — You either hyperfocus for 12 hours or can't start at all
5. **Decision fatigue** — "Should I publish now or schedule it? What category goes here?"

### How CSV + Sheets + Apps Script Solves This

| Problem | Solution | How |
|---------|----------|-----|
| Motivation fluctuates | Buffer posts ahead | Write 5 posts in one good day, schedule them spread out |
| Memory unreliable | Single source of truth | Everything in one Sheet. No "Did I post?" anxiety |
| Perfectionism | Drafts before publishing | Set Status=DRAFT, review later, no rush to publish |
| Hyperfocus vs. paralysis | Clear minimum viable action | Just: write title, set Status=READY. Script handles rest |
| Decision fatigue | Automate decisions | Script decides category, tags, SEO. You just write. |

### Real Workflow For You

**Good Day (Hyperfocus):**
```
9am-1pm: You write 5 blog posts in Google Sheets
        Set their Status = SCHEDULE for next 5 days
        Grab lunch, do other stuff, feel accomplished

Automatic (Apps Script):
        Every day at 9am, one post publishes
        Readers see consistent content
        You don't have to do anything
```

**Bad Day (Depression/Fatigue):**
```
You can't write. You can't think. Just opening a text editor feels hard.

But: Last week's scheduled posts still publish on time.
     Your audience doesn't know you're struggling.
     You don't have guilt about "missing a day."
     The system kept working without you.
```

**How this is therapeutic:**
- Removes shame about bad days
- Builds trust in yourself ("I wrote ahead, I'm not lazy")
- Visibility (can see all your posts in one place)
- Reduces decision-making on hard days

---

## Part 7: Step-by-Step Setup (For You)

### 1. Create a Google Sheet

- Go to https://sheets.google.com
- Click "New" → "Spreadsheet"
- Name it: "WordPress Publishing"
- Create columns:
  ```
  A: Title
  B: Content
  C: Category
  D: Status (dropdown: READY, SCHEDULE, DRAFT, DONE, ERROR)
  E: Schedule Date
  F: Published URL
  ```

### 2. Get into Google Apps Script

- In your Sheets, click: **Extensions → Apps Script**
- Delete the template code
- Paste the code from `tools/sheets-publisher.js`
- Edit the first two lines with YOUR credentials:
  ```javascript
  const WP_ENDPOINT = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
  const WP_API_KEY  = '0767044896thevenet_';  // ← Use YOUR key
  ```

### 3. Set Credentials (First Time Only)

- Run: `setupCredentials()` (it's in the script)
- Delete that function after running (so key isn't in the code)

### 4. Create the Hourly Trigger

- Run: `createHourlyTrigger()` (one time)
- Check the triggers (clock icon on left) to verify it exists

### 5. Test

- Add a test post to your Sheet with Status = READY
- Run: `runPublisher()` manually
- Check WordPress — did it publish?
- If yes: you're done. The hourly automation starts now.

### 6. Use It

Every day:
1. Write posts in your Google Sheet
2. Set Status = READY or SCHEDULE
3. Forget about it
4. Check back weekly to see published URLs

---

## Part 8: Extending This For Your Mental Health

You can use the **same CSV + Sheets + Apps Script pattern** for:

### 1. Medication Reminder
```
CSV:  Medication, Time, Frequency, Taken?
Script: Sends email reminder at Time. Marks Taken? = Yes automatically after you click.
```

### 2. Morning Routine Checklist
```
CSV: Task, 7am, 8am, 9am, Time to Complete
Script: Sends Slack/email with today's tasks at 7am
```

### 3. Mood Tracking
```
CSV: Date, Mood (1-10), Sleep, Medication Taken, Notes
Script: Weekly summary emailed to you
```

### 4. Expense Tracking (for freelancers)
```
CSV: Date, Expense, Category, Amount, Reimbursable?
Script: Weekly summary, alerts when over budget
```

### 5. Content Calendar
```
CSV: Topic, Deadline, Status, Priority, Assigned To
Script: Slack reminders for team members
```

**The pattern is always the same:**
1. CSV in Google Sheets
2. Google Apps Script reads it
3. Apps Script automates the boring part
4. No manual work after initial setup

---

## Summary

| Concept | What It Is | Why It Matters |
|---------|-----------|---|
| **CSV** | Simple text format for data | Universal, any tool can read it |
| **Google Sheets** | Spreadsheet = CSV with a UI | Easy to see and edit your data |
| **Apps Script** | JavaScript that reads Sheets | Automates the boring work |
| **Together** | Data + Automation = System | You write once, computer does forever |
| **For Mental Health** | Reduces decisions, removes shame | Therapeutic. Consistent output even on bad days. |

---

## Resources

- **Google Apps Script docs:** https://developers.google.com/apps-script
- **Google Sheets API:** https://developers.google.com/sheets/api
- **Your working script:** `tools/sheets-publisher.js`
- **Setup guide:** `README.md` (Method B — Google Sheets)

You've got this. Start small. Write 3 test posts. Run the script. See it work. Then expand.

