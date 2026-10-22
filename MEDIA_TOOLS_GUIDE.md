# Complete Guide: Free Audio, Video, and Banner Tools
**Everything you need to create professional media content without paying**

---

## Overview: What Tools You Need For Each Media Type

| Type | Use Case | Best Free Tool | Setup Time | OS |
|---|---|---|---|---|
| **Audio Recording** | Podcast, voice memo, narration | Audacity | 5 min | Mac/Win/Linux |
| **Audio Editing** | Cut, trim, effect, normalize | Audacity | 5 min | All |
| **Audio Creation** | Generate music, sounds | LMMS, MuseScore | 15 min | All |
| **Video Recording** | Screen capture, webcam | OBS Studio | 10 min | All |
| **Video Editing** | Cut, effects, transitions | DaVinci Resolve | 30 min | All |
| **Video Effects** | Motion graphics, overlays | Blender (overkill) or Shotcut | 20 min | All |
| **Banner Design** | Social media, blog header | Gimp, Inkscape, Canva | 10 min | All |
| **Logo Design** | Professional logo | Inkscape | 30 min | All |
| **Thumbnail Creation** | YouTube, course preview | Canva (free), Gimp | 10 min | All |

---

## PART 1: AUDIO TOOLS

### 1. Audacity (Best Audio Editor)

**What:** Professional audio recording and editing
**Cost:** Free, open-source
**Size:** ~200MB
**Learn time:** 1 hour

#### Download
```bash
# Mac
brew install audacity

# Windows / Linux
Download from: https://www.audacityteam.org/download/

# Or compile from source:
git clone https://github.com/audacity/audacity.git
cd audacity
mkdir build && cd build
cmake ..
make && sudo make install
```

#### Common Tasks

**Record your voice (for narration)**
```
1. Plug in microphone
2. Select microphone in Device Toolbar
3. Click red Record button
4. Speak clearly
5. Click pause when done
6. Edit → Select All → Effect → Normalize
7. File → Export → MP3
```

**Edit podcast (cut silence, add music)**
```
1. File → Open → podcast.mp3
2. Select → All
3. Effect → Noise Reduction (to remove background hum)
4. Effect → Normalize (make volume consistent)
5. Click at unwanted part → Select → Delete
6. Add music: File → Import → your-background-music.mp3
7. Adjust volumes (Effect → Fade In/Out)
8. Export as MP3
```

**Create intro music (simple tone)**
```
1. Generate → Silence (5 seconds)
2. Generate → Tone (frequency: 440Hz, duration: 3 sec)
3. Effect → Reverb (makes it echo)
4. File → Export → MP3
```

#### Use Cases
- ✓ Podcast recording and editing
- ✓ Voice narration for videos
- ✓ Remove background noise
- ✓ Trim silence, combine clips
- ✓ Add music layers

#### Pros
- Professional quality
- Batch processing
- Plugins for effects
- Works offline

#### Cons
- Steep learning curve initially
- Not intuitive for beginners
- No video (only audio)

---

### 2. LMMS (Make Background Music)

**What:** Create electronic music/loops
**Cost:** Free, open-source
**Size:** ~300MB
**Learn time:** 2 hours

#### Download
```bash
brew install lmms
# Or: https://lmms.io/download
```

#### Quick Start: Make Royalty-Free Background Music

```
1. Open LMMS
2. Click: Project → New
3. In Song Editor (bottom), choose tempo (120 BPM standard)
4. Click Beat/Baseline tab
5. Click empty grid cell → select drum sample
6. Fill pattern for 4 bars
7. Piano Roll tab → create melody
8. Add multiple tracks (different instruments)
9. File → Export as WAV/MP3
```

#### Use Cases
- ✓ Background music for videos
- ✓ Podcast intro/outro
- ✓ Educational video BGM
- ✓ Podcast transitions

#### Pros
- Very flexible
- Royalty-free music (you own it)
- Lots of built-in samples

#### Cons
- Learning curve
- Takes time to compose
- Quality depends on skills

**Shortcut:** Download royalty-free beats from:
- Free Music Archive: https://freemusicarchive.org
- YouTube Audio Library (if you have YouTube channel)
- Zophar's Music Archive

---

### 3. MuseScore (Compose Music/Notation)

**What:** Write sheet music, compose
**Cost:** Free (or $5.99/mo for advanced)
**Size:** ~400MB
**Learn time:** 1-2 hours

#### Download
```bash
brew install musescore
# Or: https://musescore.org/download
```

#### Use Cases
- ✓ Compose backing tracks
- ✓ Transcribe songs
- ✓ Create karaoke versions
- ✓ Educational music content

#### Quick Example: Create Simple Backing Track

```
1. Open MuseScore
2. File → New
3. Select instrument (Piano, Guitar, etc.)
4. Click staff → drag to draw notes
5. Play → Play to preview
6. File → Export → WAV or MP3
```

---

## PART 2: VIDEO TOOLS

### 1. OBS Studio (Best Screen Recording)

**What:** Record screen, webcam, mix audio/video
**Cost:** Free, open-source
**Size:** ~200MB
**Learn time:** 30 minutes

#### Download
```bash
brew install obs
# Or: https://obsproject.com/download
```

#### Use Case: Screen Recording For Teaching English

**Example: Record lesson screen**

```
1. Open OBS
2. Scene Collection → + New Scene → Name "Lesson"
3. Sources → + Add → Display Capture
4. Audio Mixer → Select microphone
5. Click Start Recording
6. Teach your lesson (speak clearly)
7. Click Stop Recording
8. Video saved to: ~/Documents/Videos/obs_recording.mkv
```

#### Common Settings

```
Settings → Output → Recording:
  Format: MP4 or MKV
  Encoder: H.264 (balanced quality/speed)
  Bitrate: 5000-8000 kbps (good quality)

Settings → Audio:
  Microphone: Select your USB mic or built-in
  Speaker: Audio Playback Device (to hear yourself)

Resolution:
  1920x1080 at 30fps (HD, reasonable file size)
```

#### Use Cases
- ✓ Screen recording for tutorials
- ✓ Zoom call recording (if allowed)
- ✓ Language lesson recordings
- ✓ Gaming (if you stream)
- ✓ Podcast with video

#### Pros
- Professional quality
- Multiple sources (screen + camera + audio)
- Streaming capabilities (Twitch, YouTube)
- Cross-platform

#### Cons
- Large file sizes
- Needs powerful computer for high quality
- Steep learning curve for advanced features

---

### 2. DaVinci Resolve (Best Video Editing)

**What:** Professional video editor, color grading, effects
**Cost:** Free (Studio version $295, but free is great)
**Size:** ~2.5GB
**Learn time:** 2-3 hours

#### Download
```bash
# Mac: https://www.blackmagicdesign.com/products/davinciresolve/
# Windows/Linux: Same link
# Or:
brew install davinci-resolve  # May not work, use website
```

#### Quick Workflow: Edit Your OBS Recording

```
1. Open DaVinci Resolve
2. File → New Project → Name "Lesson 1"
3. Media Pool → Import your .mp4
4. Double-click clip → add to timeline
5. View → Timeline
6. Drag clip into timeline area
7. Click clip → trim edges by dragging
8. Double-click clip → add text overlay
9. Color Correction tab → adjust brightness if needed
10. File → Export → H.264 MP4
11. Done
```

#### Basic Editing Tasks

**Trim silence at start/end**
```
1. Click on the clip in timeline
2. Move playhead to where to cut
3. Press Ctrl+X (cut)
4. Adjust timing
```

**Add text (for captions)**
```
1. Edit tab → Text → drag to timeline
2. Double-click → edit text
3. Adjust color/font/size right panel
```

**Speed up/slow down**
```
1. Right-click clip → Change Clip Speed
2. Set speed (1.0x = normal, 0.5x = half speed)
```

**Add background music**
```
1. File → Import another .mp3 file
2. Drag to timeline below video
3. Adjust volume in inspector
```

#### Use Cases
- ✓ Cut and trim video clips
- ✓ Add text overlays and captions
- ✓ Color correction
- ✓ Add music and sound effects
- ✓ Create professional-looking content

#### Pros
- Hollywood-grade tool
- Free version is surprisingly powerful
- Good for learning video production
- Available on all platforms

#### Cons
- Steep learning curve
- Large file sizes
- GPU acceleration helpful but not required

---

### 3. Shotcut (Alternative Video Editor)

**What:** Simpler video editor, good for beginners
**Cost:** Free, open-source
**Size:** ~200MB
**Learn time:** 1 hour

#### Download
```bash
brew install shotcut
# Or: https://shotcut.org/download/
```

#### When to Use Shotcut vs DaVinci
- **Use Shotcut if:** You want something simpler, less overwhelming
- **Use DaVinci if:** You want professional features and don't mind learning curve

#### Basic Workflow

```
1. File → Open file (your .mp4)
2. Drag clip to timeline
3. Trim by dragging edges
4. Right-click → Filters → Add color correction
5. File → Export → MP4
```

---

## PART 3: BANNER & GRAPHIC DESIGN TOOLS

### 1. Canva Free (Easiest for Beginners)

**What:** Drag-and-drop graphic designer
**Cost:** Free (or Canva Pro $13/mo)
**Learn time:** 5 minutes
**No install:** Browser-based

#### Access
```
1. Visit: https://www.canva.com
2. Sign up with Google
3. Click "+ Create a design"
4. Choose: Social Media Post, Banner, Poster, etc.
```

#### Quick Example: Create Blog Header Banner

```
1. Click "+ Create a design"
2. Choose: Blog Design → Blog Header
3. Click Template to start from template
4. Edit text: "Day 16: Grammar Teaching"
5. Change colors: Click element → Color palette
6. Add image: Drag your photo into the design
7. Download: Export → Download as PNG or PDF
```

#### Use Cases (Best for)
- ✓ Social media posts (Twitter, Instagram, Facebook)
- ✓ Blog headers
- ✓ YouTube thumbnails
- ✓ Email graphics
- ✓ Simple infographics

#### Pros
- **Extremely easy** — drag and drop
- **No design skills needed**
- **Thousands of templates**
- **Free tier is good**
- **Mobile app available**

#### Cons
- Limited customization vs. real design tools
- Free tier has watermark (barely noticeable)
- Requires internet (browser-based)

#### Free Tier Features
- ✓ Access to 250,000+ templates
- ✓ Resize designs
- ✓ Basic fonts
- ✓ Basic shapes
- ✓ Download as PNG (2-3 per month free)
- **Limitation:** Only 5 GB storage, can't save more than a few designs

---

### 2. GIMP (Free Photoshop Alternative)

**What:** Full-featured image editor
**Cost:** Free, open-source
**Size:** ~500MB
**Learn time:** 2-3 hours

#### Download
```bash
brew install gimp
# Or: https://www.gimp.org/downloads/
```

#### When to Use GIMP
- When you need to **edit existing images**
- When you need **pixel-perfect control**
- When you need **advanced effects**
- When you have a PSD file to edit

#### Quick Task: Edit a Banner

```
1. File → Open → select image.jpg
2. Image → Scale Image → resize to 1920x1080 (banner size)
3. Filters → Light and Shadow → Shadows-Highlights (fix lighting)
4. Tools → Text → add text to banner
5. Colors → Hue-Saturation → adjust color
6. File → Export As → save as PNG
```

#### Common Tasks

**Remove background from image**
```
1. File → Open image
2. Tools → Select → Fuzzy Select (magic wand)
3. Click background
4. Edit → Clear
5. Save as PNG (keeps transparency)
```

**Resize image without distortion**
```
1. Image → Scale Image → set width/height
2. Make sure chain link is connected (maintains aspect ratio)
3. Click Scale
```

**Add watermark to image**
```
1. Open image
2. Tools → Text → click image → type watermark
3. Adjust size and position
4. Export as PNG
```

#### Pros
- Powerful and flexible
- Works offline
- No limitations (free tier)
- Good learning tool

#### Cons
- Steep learning curve
- Interface is complex
- Slower than commercial tools

---

### 3. Inkscape (Vector Graphics / Logo Design)

**What:** Create scalable vector graphics (logos, icons)
**Cost:** Free, open-source
**Size:** ~300MB
**Learn time:** 3-4 hours

#### Download
```bash
brew install inkscape
# Or: https://inkscape.org/download/
```

#### When to Use Inkscape
- Creating **logos** (they stay crisp at any size)
- Creating **icons**
- Drawing **diagrams**
- Creating **scalable graphics**

#### Quick Example: Design a Simple Logo

```
1. File → New
2. Tools → Circle → drag to draw circle
3. Tools → Bezier → draw a line (your company name)
4. Tools → Text → add text
5. Select → Arrange → group elements together
6. File → Save As → save as SVG
7. File → Save As → save as PNG for web
```

#### Pros
- Creates **scalable** graphics (can resize infinitely)
- Professional logo tool
- Works offline
- No file size limitations

#### Cons
- Biggest learning curve of all
- Takes time to create good designs
- Not for photo editing

#### Keyboard Shortcuts (Time-Saving)
```
S = Selection
C = Circle/Ellipse
R = Rectangle
Z = Zoom
T = Text
B = Bezier (pen tool)
G = Gradient
Ctrl+D = Duplicate
Ctrl+G = Group
Ctrl+Shift+G = Ungroup
```

---

## QUICK REFERENCE: Which Tool For What?

| Task | Tool | Time | Difficulty |
|---|---|---|---|
| Record lesson | OBS | 10 min | Easy |
| Edit video | DaVinci Resolve | 30 min | Medium |
| Add voiceover | Audacity | 5 min | Easy |
| Create banner | Canva | 5 min | Very Easy |
| Edit photo | GIMP | 20 min | Medium |
| Design logo | Inkscape | 60 min | Hard |
| Make music | LMMS | 45 min | Medium |
| Record podcast | Audacity | 10 min | Easy |

---

## COMPLETE MEDIA PRODUCTION WORKFLOW

### Scenario: Create an Educational Video Lesson

**Step 1: Record (10 minutes)**
```
Use: OBS Studio
→ Record yourself teaching on screen
→ Clear audio from USB microphone
→ Save as video.mkv
```

**Step 2: Narration (5 minutes)**
```
Use: Audacity
→ Record intro voiceover separately
→ Edit out long pauses
→ Export as intro.mp3
```

**Step 3: Create Thumbnail (5 minutes)**
```
Use: Canva
→ Design YouTube thumbnail
→ Title: "Day 16: Grammar Teaching"
→ Download as PNG
```

**Step 4: Edit Video (30 minutes)**
```
Use: DaVinci Resolve
→ Import video.mkv
→ Import intro.mp3 on audio track
→ Add text overlay
→ Add background music (from LMMS or YouTube Audio Library)
→ Color correct lighting
→ Export final MP4
```

**Step 5: Upload**
```
→ YouTube
→ Set thumbnail (your Canva design)
→ Add description
→ Set playlist
→ Publish
```

**Total time: 1 hour for professional-looking video**
**Total cost: $0**

---

## File Size Guide

| Type | Typical Size | Format | Streaming Quality |
|---|---|---|---|
| 10 min audio (voice) | 5-10 MB | MP3 | Great |
| 30 min podcast | 30-50 MB | MP3 | Great |
| 10 min video HD | 200-400 MB | MP4 | Good |
| 60 min video HD | 2-4 GB | MP4 | Good |
| Banner image | 100-500 KB | PNG | Excellent |
| Logo vector | 10-100 KB | SVG | Excellent (scales up) |

**Tip:** Compress videos after editing using FFmpeg:
```bash
ffmpeg -i original_large.mp4 -crf 23 compressed.mp4
# -crf 23 = good quality, much smaller file
```

---

## Recommended Workflow FOR YOUR CONTENT

**Monday-Wednesday: Writing (no tools needed)**
- Write blog post in Google Docs
- Edit and refine
- Save as final draft

**Thursday: Audio (if making podcast)**
```
1. Record voiceover: Audacity (10 min)
2. Clean audio: Remove noise, normalize volume (5 min)
3. Export: MP3 format
```

**Friday: Video (optional, if making video course)**
```
1. Screen record lesson: OBS (15 min)
2. Edit video: DaVinci Resolve (20 min)
3. Add intro music: LMMS (or use YouTube Audio Library)
4. Export: MP4 format
```

**Friday: Banner/Social**
```
1. Design banner: Canva (5 min)
2. Export as PNG
3. Upload to social media with blog link
```

**Total production time: 1-2 hours per post**
**Quality: Professional**
**Cost: $0**

---

## Advanced Tips

### Make Your Videos Smaller (Save Storage)

```bash
# Basic compression
ffmpeg -i video.mp4 -crf 28 video_compressed.mp4

# Reduce resolution
ffmpeg -i video.mp4 -vf scale=1280:720 small_video.mp4

# For web (heavily compressed)
ffmpeg -i video.mp4 -crf 32 -vf scale=1280:720 web_video.mp4
```

### Batch Convert Multiple Files

```bash
# Convert all MP4s in folder to smaller size
for file in *.mp4; do
  ffmpeg -i "$file" -crf 28 "compressed_${file}"
done
```

### Add Subtitles to Video

```bash
# Install subtitle editor:
brew install subtitle-editor

# Or use FFmpeg:
ffmpeg -i video.mp4 -i subtitles.srt -c:v copy -c:a copy output.mp4
```

---

## Summary Table: All Tools

| Tool | Purpose | Free? | Install? | Difficulty |
|---|---|---|---|---|
| **Audacity** | Audio editing | ✓ | ✓ | Medium |
| **LMMS** | Make music | ✓ | ✓ | Medium |
| **MuseScore** | Compose music | ✓ | ✓ | Hard |
| **OBS** | Record screen | ✓ | ✓ | Easy |
| **DaVinci Resolve** | Edit video | ✓ | ✓ | Hard |
| **Shotcut** | Simple video edit | ✓ | ✓ | Easy |
| **Canva** | Design banners | ✓ | ✗ (web) | Very Easy |
| **GIMP** | Edit images | ✓ | ✓ | Medium |
| **Inkscape** | Design logos | ✓ | ✓ | Hard |

---

## Your Recommended Setup

### Start Simple (30 minutes total setup)
1. Install **Audacity** (recording)
2. Install **OBS Studio** (video)
3. Sign up for **Canva** (banners)

### Practice with Each Once
- Record a voice memo (Audacity)
- Record screen (OBS)
- Create a banner (Canva)

### Then Add As Needed
- DaVinci Resolve (when you need video editing)
- GIMP (when you need photo editing)
- Inkscape (when you need to design logos)

---

**Total setup time: 30 minutes**
**Total cost: $0**
**Professional output: Yes**

You have everything you need. Start simple. Practice. Add complexity as you need it.

