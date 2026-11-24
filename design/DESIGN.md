# ACE Design Handoff

The one reference for everything the ACE team makes: website, video, slides, report graphics.
If two pieces disagree, this doc wins. If this doc is silent, ask before inventing.

Last updated: Nov 23, 2026 · Owner: Rami (design/UX)

---

## 1. The idea in one line

**Five systems. One morning brief.**

ACE turns the scattered pieces of a Kent State student's day into three clear priorities, inside FlashLine and KSUMobile. Every design choice should feel *calm, clear and official*: Kent State, not a startup.

**Look and feel, in three references**

| Reference | What we take from it |
|---|---|
| Coco portfolio (Journey case study) | Story structure: dark hero with a device mockup, then clean editorial sections, small uppercase labels, thin rules, big bold headlines, text that fades in as you scroll, full-width photo pairs |
| Punchcut services page | Surface: deep navy full-bleed photo hero, two-weight headlines, icon row with top rules, translucent cards floating over parallax photos |
| Kent State brand | Kent blue and gold, Kent's approved typeface, real campus photography |

---

## 2. Color

### Core palette

| Token | Hex | Use |
|---|---|---|
| `kent-blue` | `#003976` | Primary brand color. Headlines on light, buttons, chart highlight on light |
| `kent-gold` | `#EFAB00` | Accent only: the one thing you want noticed. Highlights, active states, key number |
| `navy-900` | `#001F45` | Dark section backgrounds, hero overlay |
| `ink` | `#0B1220` | Darkest background (prototype app, video base) |
| `paper` | `#F6F4EE` | Light editorial sections (warm off-white, not pure white) |
| `white` | `#FFFFFF` | Text on dark, cards on paper |
| `slate-500` | `#5B6475` | Secondary text on light |
| `mist-300` | `#C7D2E4` | Secondary text on dark |
| `gold-700` | `#8A6100` | Gold-family **text** on light backgrounds (links, labels) |
| `rule-light` | `#E2DFD6` | Hairlines on paper |
| `rule-dark` | `rgba(255,255,255,.14)` | Hairlines on navy |

Kent State primary colors are blue (PMS 281, `#003976`) and gold (PMS 124, `#EFAB00`) from the university swatch page.

### Contrast (checked, WCAG 2.1)

| Text | On | Ratio | OK for |
|---|---|---|---|
| white | kent-blue | 11.4 : 1 | all text |
| white | navy-900 | 16.4 : 1 | all text |
| kent-gold | navy-900 | 8.2 : 1 | all text |
| kent-gold | kent-blue | 5.7 : 1 | all text |
| kent-blue | paper | 10.3 : 1 | all text |
| slate-500 | paper | 5.4 : 1 | body text |
| gold-700 | paper | 5.0 : 1 | body text |
| mist-300 | navy-900 | 10.7 : 1 | body text |
| **kent-gold** | **white / paper** | **2.0 : 1** | **never text.** Shapes, bars, underlines only |

### Rules

1. **Gold is the highlighter, not the paint.** At most one gold element per screen or frame should compete for attention.
2. Gold never carries text on light backgrounds. Use `gold-700` for gold-family text on paper.
3. Dark sections use `navy-900`; the prototype and video base use `ink`.
4. Never use red/green to carry meaning (colorblind). Status in the prototype uses color **plus** a word.
5. No gradients except the photo overlay (section 6) and the subtle navy-to-ink fade behind the hero.

---

## 3. Typography

### Typefaces

| Role | Face | Source |
|---|---|---|
| Everything (headlines, body, UI) | **Tablet Gothic** (Kent approved) | Adobe Fonts, Rami's Creative Cloud |
| Hero display | **Tablet Gothic Wide** | Adobe Fonts |
| Pull quotes, big stats (optional) | **Museo Slab** (Kent approved) | Adobe Fonts |
| Small labels, data, code | **JetBrains Mono** | Google Fonts (free) |
| Fallback if Adobe Fonts fails to load | Archivo | Google Fonts |

Adobe Fonts licenses Tablet Gothic for website publishing and for video, so the same font works on the site, in DaVinci and in slides.

**Web project:** `<link rel="stylesheet" href="https://use.typekit.net/huk6nbo.css">` (Rami's Adobe Fonts project). Family names: `tablet-gothic`, `tablet-gothic-wide`, `tablet-gothic-narrow`, `tablet-gothic-condensed`, `museo-slab`. For DaVinci and slides, click "Activate" on each family in Adobe Fonts so the desktop fonts sync.

**Weights in the web project right now: 400 and 700 only.** Until Light (300) is added, the signature headline uses Regular 400 for the first line.

CSS stack:

```css
--font-sans: "tablet-gothic", "Archivo", system-ui, sans-serif;
--font-wide: "tablet-gothic-wide", "tablet-gothic", "Archivo", sans-serif;
--font-slab: "museo-slab", Georgia, serif;
--font-mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
```

### The signature headline

Two weights on two lines, the Punchcut move. Light first line sets up, bold second line lands.

> Five systems.
> **One morning brief.**

Light = 300, Bold = 700. Never more than two lines on the web, never more than 8 words total.

### Section label

Every section opens with a mono label, numbered, uppercase, letter-spaced, with a thin rule under it:

```
01 · THE PROBLEM
──────────────────────────
```

JetBrains Mono 12px / 0.14em tracking / uppercase. Gold on dark, `gold-700` on paper.

### Web type scale

| Token | Size | Weight | Line height | Use |
|---|---|---|---|---|
| `display` | clamp(44px, 7vw, 104px) | 300 + 700 | 1.0 | Hero only |
| `h1` | clamp(36px, 4.5vw, 64px) | 700 | 1.05 | Section headlines |
| `h2` | clamp(26px, 3vw, 40px) | 600 | 1.15 | Sub-sections, card titles in features |
| `h3` | 20px | 600 | 1.3 | Card titles |
| `lead` | clamp(19px, 1.6vw, 24px) | 400 | 1.45 | Intro paragraphs, scroll-reveal text |
| `body` | 17px | 400 | 1.6 | Paragraphs (max 68 characters wide) |
| `small` | 14px | 400 | 1.5 | Captions, sources |
| `label` | 12px mono | 500 | 1.4 | Section labels, tags, data |
| `stat` | clamp(64px, 9vw, 140px) | 700 (or Museo Slab 700) | 0.9 | Big numbers |

Headings use sentence case. Uppercase is for mono labels only. Emphasis is **bold**, never underline or italic-for-emphasis (Dr. Tang: avoid outline and underline).

---

## 4. Layout and spacing

- **Grid:** 12 columns, max content width 1200px, 24px gutters, 32px side margin (20px on phones).
- **Spacing scale (px):** 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 160. Sections are separated by 128–160px on desktop, 80px on phones.
- **Radius:** 8px small (tags, buttons), 16px cards, 28px device frames. Never fully round except avatars and the orb.
- **Rules:** 1px hairlines between label and content, and between list rows. They do the work that boxes usually do.
- **White space is a feature.** If a section feels empty, cut words before adding things.

### Section rhythm on the website

Dark and light alternate so the scroll has a pulse:

```
HERO (dark, photo)  →  PROBLEM (paper)  →  STUDENT STORY (dark, photo cards)
→  HOW IT WORKS (paper)  →  TRY IT (ink, live prototype)  →  VIDEO (dark)
→  APPROVAL PATH (paper)  →  TESTING (paper)  →  ROADMAP (dark)  →  TEAM (paper)  →  DOWNLOADS (dark footer)
```

---

## 5. Components

| Component | Recipe |
|---|---|
| **Hero** | Full-bleed campus photo or loop video, navy overlay (section 6), two-weight display headline bottom-left, mono label above it, orb bottom-right, "Scroll" cue with a thin line |
| **Overview row** | Two columns: left = mono label + short italic objective in `slate-500`; right = `lead` paragraph |
| **Stat block** | Huge `stat` number, one-line meaning under it, mono source line. One gold number per row, the rest white/blue |
| **Glass card** (over photos) | `rgba(0,31,69,.62)` + `backdrop-filter: blur(14px)`, 1px `rule-dark` border, 16px radius, 28px padding. Title `h3`, body `mist-300` |
| **Icon row** | 4–5 columns, each with a 1px top rule, 28px line icon, two-line bold title, 2–3 line description |
| **Integration card** | System name (h3), "what ACE reads" list, mono tag `READ-ONLY`, small logo-free icon. No vendor logos (trademark) |
| **Pull quote** | Museo Slab or Tablet Gothic 600, 32–40px, gold opening mark, mono attribution |
| **Device mockup** | Real prototype screenshot inside a laptop or phone frame, soft shadow, sits half over the section edge |
| **Button** | Primary: kent-gold fill, ink text, 8px radius, 14px/600. Secondary: 1px white or blue outline. Arrow `→` after the label |
| **Download row** | File name, type + size in mono, arrow button. Hairline between rows |

---

## 6. Imagery

- **Real Kent campus photography and footage only** (Rami's library plus John's best-of folder). No stock people.
- Subjects: students between classes, on phones and laptops, in the library, at the Student Center. Natural light, candid, not posed.
- **Overlay for text on photos:** `linear-gradient(180deg, rgba(0,31,69,.35) 0%, rgba(0,31,69,.85) 100%)`. Text always sits in the darker part.
- **Device shots:** prototype screenshots placed in laptop and phone frames, ideally composited into real campus photos (the Coco move).
- Photo credit and release: only use images UCM already has releases for.

---

## 7. Motion (website)

| Effect | Spec |
|---|---|
| Scroll reveal | Fade up 24px, 600ms, `cubic-bezier(.2,.7,.2,1)`, staggered 80ms per item |
| Word-by-word reveal | Lead paragraphs: words go from 20% to 100% opacity as they scroll through the middle of the screen (Coco) |
| Parallax | Background photos move at 0.25× scroll speed. Never on text |
| Stat count-up | Numbers count from 0 over 1.2s when they enter view |
| Card hover | Lift 4px, border brightens. 200ms |

**Always respect `prefers-reduced-motion`:** turn off parallax and count-ups and show everything at full opacity.

---

## 8. The ACE orb

The orb is ACE's face: a blue planet-like circle with gold eyes and an orbiting gold moon, from the proposal deck. Files live in `assets/`.

| File | Mood | Use it when |
|---|---|---|
| `ace-hello.gif` | Neutral, greeting | Intros, the site hero, "Meet ACE" |
| `ace-thinking.gif` | Moon orbiting, eyes up | Loading, "checking your systems", back-end explanations |
| `ace-happy.gif` | Smiling eyes | Brief ready, success, solution moments |
| `ace-alert.gif` | Ping rings | Problems, deadlines, holds, warnings |
| `ace-wink.gif` | Wink | Friendly asides, tips, invitations |
| `ace-done.gif` | Check mark | Completion, roadmap milestones, "thank you" |

Rules: keep the orb's colors as they are; never stretch it; minimum 48px tall; give it room (at least half its width clear on every side). The orb speaks in **short** bubbles (under 6 words) in white with ink text. It is a guide, not a mascot: at most one orb on screen at a time.

---

## 9. Data visualization

From Dr. Tang's storytelling lectures, applied:

1. **One message per chart.** The title states the takeaway ("Nearly half of students missed a deadline they didn't know about"), not the topic.
2. **Blue and gray, one gold highlight.** The bar or number that makes the point is gold (on dark) or kent-blue (on light); everything else is gray.
3. Bars start at zero. Bars wider than the gaps between them.
4. **No pies, donuts, area charts or 3D.**
5. Round numbers in text ("about 600 students per advisor"). Exact numbers live in the source line.
6. Every chart has a mono source line: `Source: Pathify (2025)`.
7. For 1–3 numbers, use big text (stat block), not a chart.

---

## 10. Words

- Plain, short sentences. Second person for students ("your day"), third person for decision-makers.
- Lead with the student, then the institution: retention, DFW rates and advising efficiency are what decision-makers care about.
- Round numbers, then cite.
- **Names, spelled exactly:** ACE (Academic & Career Executive assistant), FlashLine, KSUMobile, Canvas, Banner, Visual Schedule Builder, Navigate360 (Kent calls it KSU Navigate), Handshake, Microsoft Copilot, Microsoft Entra ID, HECVAT, VPAT, FERPA.
- **Retired terms** (since the Nov 23 meeting): ~~GPS audit~~ as a data source, ~~Gemini/Vertex~~ in final materials. The prototype runs a Gemini demo model; say "the prototype uses a demo model; production uses Microsoft Copilot."

---

## 11. Video spec (about 3 minutes)

| Item | Spec |
|---|---|
| Format | 1920×1080, 24 fps, H.264 (master in ProRes or DNxHR from DaVinci) |
| Style | Vox-style explainer: motion graphics + voiceover + sound design, mixed with Kent campus footage and still diagram frames |
| Base | `ink` / `navy-900` frames, kent-gold highlights, white type |
| Type | Tablet Gothic. Titles 72–96px bold; body callouts 40–48px; labels 24px JetBrains Mono uppercase |
| Safe area | Keep text inside 90% title-safe (96px from left/right edges, 54px from top/bottom) |
| Lower thirds | Mono label (gold) over name (white, 40px), on a 70% navy bar, slides in 12 frames |
| Captions | Burned-in version for the Taylor Hall screen: Tablet Gothic 44px, white on 60% ink box, bottom center, max 2 lines |
| Voiceover | About 150 words/minute, so a 3-minute cut is about 420–450 words |
| Orb | Narrator's "face" for transitions and the back-end walkthrough |
| Music | Light, steady, instrumental, ducked −18 dB under voice |
| End card | ACE orb + "Five systems. One morning brief." + site URL + team names, 5 seconds |

**Story arc** (team, Nov 23): problem → stakeholders (student first) → ACE as the solution through one student's day → front-end walkthrough → annotated front-to-back flowchart with compliance touchpoints → "what's next" call to action.

---

## 12. Slides and report graphics

Same palette, fonts and chart rules. Slides: navy-900 title slides, paper content slides, mono section labels matching the website numbering. Report figures: export charts at 2× from the site styles so the report and site match.

---

## 13. Where things live

| What | Where |
|---|---|
| This doc | `design/DESIGN.md` in the GitHub repo `ramidaud/ace-prototype`, plus the team folder |
| Visual preview of this doc | `https://ramidaud.github.io/ace-prototype/design/` |
| Orb files | `assets/` in the repo |
| Live prototype | the GitHub Pages site (moving to `/prototype/` when the hub site launches) |

---

## 14. Before anything ships, check

- [ ] Only blue, gold, navy, ink, paper, white and the listed grays
- [ ] At most one gold "look here" per screen or frame
- [ ] Tablet Gothic (or the Archivo fallback) for everything except mono labels
- [ ] Section labels numbered and matching across site, video and slides
- [ ] Charts follow section 9 and have a source line
- [ ] No GPS audit or Gemini in final copy
- [ ] Real Kent photos with releases
- [ ] Works with keyboard only, and with reduced motion turned on

## Update, Nov 23: prototype follows FlashLine, not the marketing system

- The prototype now mirrors FlashLine's real dark UI: system sans, charcoal greys, the purple Course Registration header, "Student Dashboard" title with underline tabs. ACE appears as a card on the Dashboard tab and as its own "ACE" tab. Kent navy and gold stay on the hub site, the video and the report.
- Demo controls (persona switcher, Phone, Email, Data, Advisor, Test, Results) live in a striped gold "ACE PROTOTYPE · SYNTHETIC DATA" bar above FlashLine, so nobody mistakes them for FlashLine features.
- Hub photos: Kent State UCM photography in assets/photos (campus at dusk, students walking, VR, drones, plus a five-photo band before the team section), always under a navy overlay at 85% or more so text stays at AA contrast.
- Screenshots in assets/shots are 2x captures of the prototype with Jordan's real demo data and the prototype bar hidden.
