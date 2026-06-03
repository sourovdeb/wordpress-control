#!/usr/bin/env python3
"""
WP Auto-Publisher Desktop — sourovdeb.com
Tkinter GUI: write a topic OR paste your content → AI auto-fills SEO → publish/schedule

Requirements: pip install requests
Run: python wp-desktop.py
Config stored at: ~/.wp-studio/config.json
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json, os, threading, webbrowser
from datetime import datetime

try:
    import requests
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# ── Config ────────────────────────────────────────────────────────────────────
CONFIG_DIR  = os.path.expanduser("~/.wp-studio")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULTS = {
    "wp_url":       "https://sourovdeb.com",
    "plugin_key":   "",
    "ai_provider":  "claude",
    "claude_key":   "",
    "deepseek_key": "",
    "categories":   ["ELT Masterclass","ELT","CELTA","Job Hunting","AI Tools","Teaching Resources","Personal"],
}

def load_cfg():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return {**DEFAULTS, **json.load(f)}
    return DEFAULTS.copy()

def save_cfg(c):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(c, f, indent=2)

# ── WordPress API ─────────────────────────────────────────────────────────────
def wp_api(cfg, path, method="GET", body=None):
    url = cfg["wp_url"].rstrip("/") + "/wp-json/sourov/v1" + path
    headers = {
        "X-Sourov-Key":  cfg["plugin_key"],
        "Content-Type":  "application/json",
    }
    r = requests.request(method, url, headers=headers, json=body, timeout=30)
    r.raise_for_status()
    return r.json()

# ── AI ────────────────────────────────────────────────────────────────────────
def _call_ai(cfg, system, prompt, max_tokens=3000):
    provider = cfg.get("ai_provider", "claude")
    if provider == "claude":
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key":           cfg["claude_key"],
                "anthropic-version":   "2023-06-01",
                "content-type":        "application/json",
            },
            json={
                "model":      "claude-haiku-4-5-20251001",
                "max_tokens": max_tokens,
                "system":     system,
                "messages":   [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
        r.raise_for_status()
        raw = r.json()["content"][0]["text"]
    elif provider == "deepseek":
        r = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {cfg['deepseek_key']}",
                "Content-Type":  "application/json",
            },
            json={
                "model":    "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": prompt},
                ],
            },
            timeout=60,
        )
        r.raise_for_status()
        raw = r.json()["choices"][0]["message"]["content"]
    else:
        raise ValueError(f"Unknown AI provider: {provider}")

    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(raw)


def ai_generate_post(cfg, topic, tone="educational", words=800):
    system = "You are a WordPress content writer for an ELT educator's blog. Respond ONLY with valid JSON, no markdown fences."
    prompt = f"""Write a complete blog post about: "{topic}"
Tone: {tone}. Target: {words} words.
Return exactly this JSON:
{{
  "title": "engaging title",
  "content": "full HTML with <h2>, <p>, <ul>, <strong> tags",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "category": "most fitting from: ELT Masterclass, ELT, CELTA, Job Hunting, AI Tools, Teaching Resources",
  "meta_description": "SEO description 120-155 chars",
  "seo_title": "SEO title max 60 chars",
  "excerpt": "2-sentence summary"
}}"""
    return _call_ai(cfg, system, prompt)


def ai_autofill_seo(cfg, title, content):
    system = "You are an SEO expert. Respond ONLY with valid JSON, no markdown fences."
    prompt = f"""Blog post title: {title}
Content preview: {content[:1000]}

Return exactly:
{{
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "category": "most fitting from: ELT Masterclass, ELT, CELTA, Job Hunting, AI Tools, Teaching Resources",
  "meta_description": "SEO description 120-155 chars",
  "seo_title": "SEO title max 60 chars"
}}"""
    return _call_ai(cfg, system, prompt, max_tokens=500)


# ── Main App ──────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.cfg          = load_cfg()
        self.current_post = {}

        self.title("WP Auto-Publisher — sourovdeb.com")
        self.geometry("860x680")
        self.configure(bg="#1e1e1e")
        self.resizable(True, True)

        self._apply_styles()
        self._build()
        self.after(600, self._ping_site)

    # ── Styles ────────────────────────────────────────────────────────────────
    def _apply_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure(".",               background="#1e1e1e", foreground="#d4d4d4", font=("Segoe UI", 10))
        s.configure("TNotebook",       background="#252526", borderwidth=0)
        s.configure("TNotebook.Tab",   background="#2d2d2d", foreground="#858585", padding=[14, 7])
        s.map("TNotebook.Tab",         background=[("selected","#1e1e1e")], foreground=[("selected","#d4d4d4")])
        s.configure("TFrame",          background="#1e1e1e")
        s.configure("TLabel",          background="#1e1e1e", foreground="#d4d4d4")
        s.configure("TButton",         background="#0e639c", foreground="white", padding=[9, 5], relief="flat", borderwidth=0)
        s.map("TButton",               background=[("active","#1177bb"),("disabled","#333")])
        s.configure("Green.TButton",   background="#2d7a4a", foreground="white", padding=[9, 5], relief="flat")
        s.map("Green.TButton",         background=[("active","#38975c")])
        s.configure("Purple.TButton",  background="#673de6", foreground="white", padding=[9, 5], relief="flat")
        s.map("Purple.TButton",        background=[("active","#7851f0")])
        s.configure("Danger.TButton",  background="#6e2020", foreground="#f44747", padding=[9, 5], relief="flat")
        s.configure("Ghost.TButton",   background="#2d2d2d", foreground="#d4d4d4", padding=[9, 5], relief="flat")
        s.map("Ghost.TButton",         background=[("active","#3a3a3a")])
        s.configure("TEntry",          fieldbackground="#2d2d2d", foreground="#d4d4d4", insertcolor="#d4d4d4", relief="flat")
        s.configure("TCombobox",       fieldbackground="#2d2d2d", foreground="#d4d4d4", relief="flat")
        s.configure("TLabelframe",     background="#1e1e1e", foreground="#dcdcaa", relief="flat")
        s.configure("TLabelframe.Label", background="#1e1e1e", foreground="#dcdcaa", font=("Segoe UI", 10, "bold"))
        s.configure("Treeview",        background="#252526", foreground="#d4d4d4", fieldbackground="#252526", rowheight=24)
        s.configure("Treeview.Heading", background="#2d2d2d", foreground="#858585", relief="flat")
        s.map("Treeview",              background=[("selected","#094771")])

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build(self):
        # Top bar
        top = tk.Frame(self, bg="#252526")
        top.pack(fill="x")
        tk.Label(top, text="⚡ WP Auto-Publisher",
                 bg="#252526", fg="#673de6", font=("Segoe UI", 12, "bold")).pack(side="left", padx=14, pady=7)
        self.status_lbl = tk.Label(top, text="connecting…",
                                    bg="#252526", fg="#858585", font=("Segoe UI", 9))
        self.status_lbl.pack(side="right", padx=14, pady=7)

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=(4, 8))

        self._tab_write    = ttk.Frame(nb)
        self._tab_posts    = ttk.Frame(nb)
        self._tab_settings = ttk.Frame(nb)

        nb.add(self._tab_write,    text="  ✍️  Write & Publish  ")
        nb.add(self._tab_posts,    text="  📋  Manage Posts    ")
        nb.add(self._tab_settings, text="  ⚙️  Settings        ")

        self._build_write()
        self._build_posts()
        self._build_settings()

        nb.bind("<<NotebookTabChanged>>", lambda e: self._on_tab(nb))

    # ── Write Tab ─────────────────────────────────────────────────────────────
    def _build_write(self):
        f = self._tab_write

        # Mode bar
        mode_bar = tk.Frame(f, bg="#252526", padx=14, pady=9)
        mode_bar.pack(fill="x")
        tk.Label(mode_bar, text="MODE:", bg="#252526", fg="#858585",
                 font=("Segoe UI", 9, "bold")).pack(side="left")
        self.mode = tk.StringVar(value="generate")
        for val, txt in [("generate","  AI writes everything — give me a topic"),
                          ("manual",  "  I wrote it — auto-fill SEO only")]:
            tk.Radiobutton(mode_bar, text=txt, variable=self.mode, value=val,
                           bg="#252526", fg="#d4d4d4", selectcolor="#1e1e1e",
                           activebackground="#252526", activeforeground="#d4d4d4",
                           command=self._toggle_mode).pack(side="left", padx=(16, 0))

        # Topic input (generate mode)
        self._topic_row = tk.Frame(f, bg="#1e1e1e", padx=14, pady=4)
        self._topic_row.pack(fill="x")
        tk.Label(self._topic_row, text="Topic:", bg="#1e1e1e", fg="#858585",
                 font=("Segoe UI", 9)).pack(side="left")
        self.topic_entry = ttk.Entry(self._topic_row, width=70, font=("Segoe UI", 11))
        self.topic_entry.pack(side="left", padx=(10, 0), fill="x", expand=True)
        self.topic_entry.bind("<Return>", lambda e: self._do_generate())

        opts = tk.Frame(f, bg="#1e1e1e", padx=14, pady=2)
        opts.pack(fill="x")
        for lbl, var_name, vals, default, w in [
            ("Tone:",  "tone_var",  ["educational","professional","conversational","friendly","persuasive"], "educational", 16),
            ("Words:", "words_var", ["400","600","800","1000","1200"], "800", 8),
        ]:
            tk.Label(opts, text=lbl, bg="#1e1e1e", fg="#858585", font=("Segoe UI", 9)).pack(side="left", padx=(0 if lbl=="Tone:" else 20, 0))
            cb = ttk.Combobox(opts, values=vals, width=w, state="readonly", font=("Segoe UI", 10))
            cb.set(default)
            setattr(self, var_name, cb)
            cb.pack(side="left", padx=(6, 0))

        # Manual input (hidden by default)
        self._manual_row = tk.Frame(f, bg="#1e1e1e", padx=14)
        tk.Label(self._manual_row, text="Title:", bg="#1e1e1e", fg="#858585",
                 font=("Segoe UI", 9)).pack(anchor="w")
        self.manual_title = ttk.Entry(self._manual_row, font=("Segoe UI", 11))
        self.manual_title.pack(fill="x", pady=(3, 8))
        tk.Label(self._manual_row, text="Content (HTML or plain text):", bg="#1e1e1e",
                 fg="#858585", font=("Segoe UI", 9)).pack(anchor="w")
        self.manual_content = scrolledtext.ScrolledText(
            self._manual_row, height=7, bg="#2d2d2d", fg="#d4d4d4",
            insertbackground="#d4d4d4", font=("Segoe UI", 10), relief="flat",
            padx=8, pady=6)
        self.manual_content.pack(fill="both", expand=True, pady=(3, 0))

        # Action buttons
        btn_row = tk.Frame(f, bg="#1e1e1e", padx=14, pady=8)
        btn_row.pack(fill="x")
        self.gen_btn = ttk.Button(btn_row, text="✨  Generate + Auto-SEO",
                                   style="Purple.TButton", command=self._do_generate)
        self.gen_btn.pack(side="left")
        self.seo_btn = ttk.Button(btn_row, text="🔍  Auto-Fill SEO",
                                   command=self._do_autofill)
        # seo_btn shown only in manual mode
        self.busy_lbl = tk.Label(btn_row, text="", bg="#1e1e1e", fg="#673de6",
                                  font=("Segoe UI", 9, "italic"))
        self.busy_lbl.pack(side="left", padx=(14, 0))

        # Preview card
        prev = ttk.LabelFrame(f, text=" Preview & Publish ", padding=12)
        prev.pack(fill="both", expand=True, padx=14, pady=(0, 8))

        self.prev_title = tk.Label(prev, text="(nothing generated yet — enter a topic above)",
                                    bg="#1e1e1e", fg="#dcdcaa",
                                    font=("Segoe UI", 11, "bold"), wraplength=780, justify="left")
        self.prev_title.pack(anchor="w")

        meta = tk.Frame(prev, bg="#1e1e1e")
        meta.pack(fill="x", pady=(6, 0))
        self.prev_seo  = tk.Label(meta, text="", bg="#1e1e1e", fg="#4ec9b0", font=("Segoe UI", 9))
        self.prev_seo.pack(anchor="w")
        self.prev_meta = tk.Label(meta, text="", bg="#1e1e1e", fg="#858585",
                                   font=("Segoe UI", 9), wraplength=780, justify="left")
        self.prev_meta.pack(anchor="w")
        self.prev_tags = tk.Label(meta, text="", bg="#1e1e1e", fg="#858585", font=("Segoe UI", 9))
        self.prev_tags.pack(anchor="w", pady=(2, 0))

        pub = tk.Frame(prev, bg="#1e1e1e")
        pub.pack(fill="x", pady=(10, 0))
        ttk.Button(pub, text="✓  Publish Now",  style="Green.TButton",
                   command=lambda: self._publish("publish")).pack(side="left")
        ttk.Button(pub, text="💾  Save Draft",   style="Ghost.TButton",
                   command=lambda: self._publish("draft")).pack(side="left",  padx=(8, 0))
        ttk.Button(pub, text="🕐  Schedule…",    style="Ghost.TButton",
                   command=self._toggle_scheduler).pack(side="left", padx=(8, 0))

        self.sched_row = tk.Frame(prev, bg="#1e1e1e")
        tk.Label(self.sched_row, text="Date/time (ISO):", bg="#1e1e1e",
                 fg="#858585", font=("Segoe UI", 9)).pack(side="left")
        self.sched_entry = ttk.Entry(self.sched_row, width=22)
        self.sched_entry.insert(0, datetime.now().strftime("%Y-%m-%dT09:00"))
        self.sched_entry.pack(side="left", padx=(8, 10))
        ttk.Button(self.sched_row, text="Schedule", style="Green.TButton",
                   command=lambda: self._publish("future")).pack(side="left")

    def _toggle_mode(self):
        if self.mode.get() == "generate":
            self._manual_row.pack_forget()
            self._topic_row.pack(fill="x")
            self.seo_btn.pack_forget()
            self.gen_btn.pack(side="left")
        else:
            self._topic_row.pack_forget()
            self._manual_row.pack(fill="both", expand=True, padx=14, pady=4)
            self.gen_btn.pack_forget()
            self.seo_btn.pack(side="left")

    def _toggle_scheduler(self):
        if self.sched_row.winfo_ismapped():
            self.sched_row.pack_forget()
        else:
            self.sched_row.pack(fill="x", pady=(8, 0))

    # ── Posts Tab ─────────────────────────────────────────────────────────────
    def _build_posts(self):
        f = self._tab_posts

        bar = tk.Frame(f, bg="#252526", padx=12, pady=7)
        bar.pack(fill="x")
        tk.Label(bar, text="Filter:", bg="#252526", fg="#858585").pack(side="left")
        self.post_filter = ttk.Combobox(
            bar, values=["All (draft + scheduled)","Scheduled only","Drafts only"],
            width=22, state="readonly")
        self.post_filter.set("All (draft + scheduled)")
        self.post_filter.pack(side="left", padx=(8, 10))
        ttk.Button(bar, text="↻  Refresh", command=self._load_posts).pack(side="left")

        tree_frame = tk.Frame(f, bg="#1e1e1e")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=8)

        cols = ("id","title","status","date","link")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=18)
        for col, heading, width, anchor in [
            ("id",     "ID",      50,  "center"),
            ("title",  "Title",   360, "w"),
            ("status", "Status",  80,  "center"),
            ("date",   "Date",    130, "center"),
            ("link",   "URL",     200, "w"),
        ]:
            self.tree.heading(col, text=heading, anchor=anchor)
            self.tree.column(col,  width=width,  anchor=anchor)

        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")

        acts = tk.Frame(f, bg="#1e1e1e", padx=12, pady=6)
        acts.pack(fill="x")
        ttk.Button(acts, text="🌐  Open in Browser", command=self._open_browser).pack(side="left")
        ttk.Button(acts, text="✕  Delete Selected", style="Danger.TButton",
                   command=self._delete_post).pack(side="left", padx=(10, 0))

    # ── Settings Tab ──────────────────────────────────────────────────────────
    def _build_settings(self):
        f = self._tab_settings

        canvas = tk.Canvas(f, bg="#1e1e1e", highlightthickness=0)
        scroll = ttk.Scrollbar(f, orient="vertical", command=canvas.yview)
        inner  = tk.Frame(canvas, bg="#1e1e1e", padx=24, pady=16)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        def lf(parent, title):
            lframe = ttk.LabelFrame(parent, text=f" {title} ", padding=12)
            lframe.pack(fill="x", pady=(0, 14))
            return lframe

        def row(parent, label, widget, entry_width=50):
            r = tk.Frame(parent, bg="#1e1e1e")
            r.pack(fill="x", pady=4)
            tk.Label(r, text=label, bg="#1e1e1e", fg="#858585",
                     font=("Segoe UI", 9), width=22, anchor="e").pack(side="left")
            widget_inst = widget(r, width=entry_width)
            widget_inst.pack(side="left", fill="x", expand=True, padx=(10, 0))
            return widget_inst

        wp = lf(inner, "WordPress")
        self.s_url = row(wp, "Site URL",          ttk.Entry)
        self.s_key = row(wp, "Plugin Secret Key", lambda p, **kw: ttk.Entry(p, show="*", **kw))
        self.s_url.insert(0, self.cfg.get("wp_url", ""))
        self.s_key.insert(0, self.cfg.get("plugin_key", ""))
        ttk.Button(wp, text="Ping Site", command=self._ping_site,
                   style="Ghost.TButton").pack(anchor="w", pady=(4, 0))

        ai = lf(inner, "AI Provider")
        pr = tk.Frame(ai, bg="#1e1e1e")
        pr.pack(fill="x", pady=4)
        tk.Label(pr, text="Provider", bg="#1e1e1e", fg="#858585",
                 font=("Segoe UI", 9), width=22, anchor="e").pack(side="left")
        self.s_provider = ttk.Combobox(pr, values=["claude","deepseek"], width=14, state="readonly")
        self.s_provider.set(self.cfg.get("ai_provider", "claude"))
        self.s_provider.pack(side="left", padx=(10, 0))

        self.s_claude   = row(ai, "Claude API Key",   lambda p, **kw: ttk.Entry(p, show="*", **kw))
        self.s_deepseek = row(ai, "DeepSeek API Key", lambda p, **kw: ttk.Entry(p, show="*", **kw))
        self.s_claude.insert(0,   self.cfg.get("claude_key", ""))
        self.s_deepseek.insert(0, self.cfg.get("deepseek_key", ""))

        ttk.Button(inner, text="💾  Save Settings", style="Purple.TButton",
                   command=self._save_settings).pack(anchor="w")
        self.save_msg = tk.Label(inner, text="", bg="#1e1e1e", fg="#4ec9b0", font=("Segoe UI", 9))
        self.save_msg.pack(anchor="w", pady=(6, 0))

    # ── Handlers ──────────────────────────────────────────────────────────────
    def _ping_site(self):
        def _run():
            try:
                d = wp_api(self.cfg, "/status")
                msg = f"✓ {d.get('site','connected')} | {d.get('total_posts',0)} posts | {d.get('scheduled_posts',0)} scheduled"
                self.after(0, lambda: self.status_lbl.config(text=msg, fg="#4ec9b0"))
            except Exception as e:
                self.after(0, lambda: self.status_lbl.config(text=f"✗ {e}", fg="#f44747"))
        threading.Thread(target=_run, daemon=True).start()

    def _set_busy(self, msg):
        self.busy_lbl.config(text=msg)
        state = "disabled" if msg else "normal"
        self.gen_btn.config(state=state)
        self.seo_btn.config(state=state)

    def _do_generate(self):
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("WP Publisher", "Please enter a topic.")
            return
        self._set_busy("Generating with AI…")
        def _run():
            try:
                post = ai_generate_post(self.cfg, topic,
                                         self.tone_var.get(), int(self.words_var.get()))
                self.current_post = post
                self.after(0, lambda: self._show_preview(post))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("AI Error", str(e)))
            finally:
                self.after(0, lambda: self._set_busy(""))
        threading.Thread(target=_run, daemon=True).start()

    def _do_autofill(self):
        title   = self.manual_title.get().strip()
        content = self.manual_content.get("1.0", "end").strip()
        if not title or not content:
            messagebox.showwarning("WP Publisher", "Enter both title and content.")
            return
        self._set_busy("Auto-filling SEO…")
        def _run():
            try:
                seo = ai_autofill_seo(self.cfg, title, content)
                post = {
                    "title":            title,
                    "content":          content,
                    "tags":             seo.get("tags", []),
                    "category":         seo.get("category", "ELT"),
                    "meta_description": seo.get("meta_description", ""),
                    "seo_title":        seo.get("seo_title", title),
                }
                self.current_post = post
                self.after(0, lambda: self._show_preview(post))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("AI Error", str(e)))
            finally:
                self.after(0, lambda: self._set_busy(""))
        threading.Thread(target=_run, daemon=True).start()

    def _show_preview(self, post):
        if not post:
            self.prev_title.config(text="(nothing generated yet)")
            self.prev_seo.config(text="")
            self.prev_meta.config(text="")
            self.prev_tags.config(text="")
            return
        tags = post.get("tags", [])
        tag_str = ", ".join(tags) if isinstance(tags, list) else str(tags)
        self.prev_title.config(text=post.get("title", ""))
        self.prev_seo.config(text=f"SEO Title: {post.get('seo_title','')}")
        self.prev_meta.config(text=f"Meta: {post.get('meta_description','')}")
        self.prev_tags.config(text=f"Tags: {tag_str}   |   Category: {post.get('category','')}")

    def _publish(self, status):
        if not self.current_post:
            messagebox.showwarning("WP Publisher", "Nothing to publish. Generate or auto-fill first.")
            return
        post = dict(self.current_post)
        post["status"] = status
        if status == "future":
            dt = self.sched_entry.get().strip()
            post["date"] = dt if "T" in dt else dt + "T09:00:00"
        if isinstance(post.get("tags"), list):
            post["tags"] = ", ".join(post["tags"])
        self._set_busy(f"Publishing ({status})…")
        def _run():
            try:
                result = wp_api(self.cfg, "/ai-post", "POST", post)
                pid  = result.get("id") or result.get("post_id")
                link = result.get("link", "")
                self.after(0, lambda: messagebox.showinfo("Published!", f"Post ID: {pid}\n{link}"))
                if link:
                    self.after(0, lambda: webbrowser.open(link))
                self.current_post = {}
                self.after(0, lambda: self._show_preview({}))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Publish Error", str(e)))
            finally:
                self.after(0, lambda: self._set_busy(""))
        threading.Thread(target=_run, daemon=True).start()

    def _load_posts(self):
        fmap = {
            "All (draft + scheduled)": "",
            "Scheduled only":          "future",
            "Drafts only":             "draft",
        }
        fval = fmap.get(self.post_filter.get(), "")
        path = f"/scheduled?post_status={fval}" if fval else "/scheduled"
        def _run():
            try:
                posts = wp_api(self.cfg, path)
                self.after(0, lambda: self._render_posts(posts))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", str(e)))
        threading.Thread(target=_run, daemon=True).start()

    def _render_posts(self, posts):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in (posts or []):
            self.tree.insert("", "end", values=(
                p.get("id",""),
                p.get("title",""),
                p.get("status",""),
                str(p.get("scheduled",""))[:16],
                p.get("link",""),
            ))

    def _open_browser(self):
        sel = self.tree.selection()
        if not sel: return
        link = self.tree.item(sel[0])["values"][4]
        if link: webbrowser.open(str(link))

    def _delete_post(self):
        sel = self.tree.selection()
        if not sel: return
        vals  = self.tree.item(sel[0])["values"]
        pid, title = vals[0], vals[1]
        if not messagebox.askyesno("Delete?", f"Permanently delete post ID {pid}?\n\"{title}\""):
            return
        def _run():
            try:
                wp_api(self.cfg, f"/post/{pid}", "DELETE")
                self.after(0, self._load_posts)
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", str(e)))
        threading.Thread(target=_run, daemon=True).start()

    def _save_settings(self):
        self.cfg.update({
            "wp_url":       self.s_url.get().strip().rstrip("/"),
            "plugin_key":   self.s_key.get().strip(),
            "ai_provider":  self.s_provider.get(),
            "claude_key":   self.s_claude.get().strip(),
            "deepseek_key": self.s_deepseek.get().strip(),
        })
        save_cfg(self.cfg)
        self.save_msg.config(text="✓ Saved!")
        self.after(2500, lambda: self.save_msg.config(text=""))
        self._ping_site()

    def _on_tab(self, nb):
        label = nb.tab(nb.select(), "text")
        if "Posts" in label:
            self._load_posts()


if __name__ == "__main__":
    App().mainloop()
