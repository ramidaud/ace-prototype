# ACE Prototype

ACE (Academic & Career Executive assistant) is a class prototype for EMAT 60010 at Kent State University, by Sam Garcia, Allan Sanchez, Abisola Mohammed and Rami Daud. **All student data is synthetic.** It is not an official Kent State product.

**Project site (hub):** https://ramidaud.github.io/ace-prototype/
**Prototype:** https://ramidaud.github.io/ace-prototype/prototype/
**Tester link (test mode only):** https://ramidaud.github.io/ace-prototype/prototype/#test (the old root `#test` link forwards here)
**Design system:** https://ramidaud.github.io/ace-prototype/design/

## What's here

- `index.html` is the project hub site. `prototype/index.html` is the whole prototype in one file. It reads a Supabase database (read-only, synthetic data) and gets the daily brief from Google Gemini through a Supabase Edge Function.
- `tools/seed_personas.py` generated the five demo students.

## Views

1. **Dashboard**: the Slide 6 FlashLine/ACE screen, driven by the database. Includes 3 AI-ranked priorities, a graduation ring, a weekly workload chart, a registration countdown, a career milestone, a "coming up" list, degree requirement bars, and hold and instructor-alert banners.
2. **Phone**: the same brief in a phone frame, with the 6:30 am email shown as a push notification. On a real phone the dashboard reflows to one column.
3. **Kent email nudge**: a mock Kent Mail reminder.
4. **How ACE handles data**: read-only sources, which fields go to the AI and which are withheld, and HECVAT / VPAT / FERPA status (from the Tom Mahan meeting).

Use the **Demo student** picker (bottom left) to switch personas.

## Personas (demo "today" = Thu Nov 19, 2026)

| Persona | Scenario ACE should catch |
|---|---|
| Jordan Rivera, first-gen sophomore | Paper due tonight, 40/50 stats quiz, 1 humanities course left, 2 Spring sections fit |
| Maya Chen, College Credit Plus | CCP intent form missing (blocks Spring), CCP withdraw deadline Sunday |
| Marcus Bell, graduating senior | Hasn't applied to graduate (due Nov 27), experiential requirement missing, job deadlines |
| Priya Nair, transfer junior | Advising hold, registration opens Monday, 9 transfer credits not posted |
| Tyler Brooks, freshman at Stark | Instructor early alert in math, 2 missing assignments, bursar hold |

There are also 40 background students. They make the database look real, but they don't appear in the picker.

## Database (Supabase project "ACE Prototype", `gcwuhdofhlebpgaqaran`)

The tables are grouped by the system ACE would read in production:

- **FlashLine / Banner**: `students`, `terms`, `courses`, `registration_windows`, `holds`, `key_dates`
- **Canvas**: `enrollments`, `canvas_assignments`
- **GPS audit**: `gps_requirements`
- **Schedule Builder**: `schedule_sections`
- **Navigate360**: `navigate_services`, `navigate_appointments`, `navigate_alerts`
- **Handshake**: `handshake_events`, `handshake_jobs`, `handshake_applications`
- **ACE**: `ace_briefs` (stored fallback briefs), `ace_notifications` (email nudges), `ace_sync_log`, `demo_clock`

`ace_student_snapshot(student_id)` returns everything for one student in a single call. The AI gets a trimmed copy with no IDs, emails, last name or GPA.

`demo_clock.anchor_date` is the demo's "today". All countdowns are measured from it, so the demo won't go stale before Dec 7.

Access is read-only: row-level security is on and the anon key can only SELECT.

## Live AI brief

The page tries three ways to get the brief, in this order:

1. **Gemini**, through the Supabase Edge Function `ace-brief`, which picks a current Flash model and skips busy ones. This is the proposal's stack.
2. **Claude**, when the same page is viewed as an artifact inside claude.ai.
3. **Stored brief** from `ace_briefs`. It shows instantly and stays if the AI is unavailable, so a demo never shows a blank screen.

The pill next to the headline shows which one is active.

## Known gaps / next passes

- "Open in Canvas" and similar buttons show an explanation dialog. They don't deep-link anywhere.
- The course codes look like Kent's but are illustrative.
- No formal WCAG audit yet. Keyboard, focus, skip link and labeled charts are in.

## User testing

Open the tester link, choose the facilitator and method, then hand over the device. Each session runs two counterbalanced rounds ("current way" across six mock portals vs. ACE) with three timed questions each, an accuracy check on ACE's picks, a five-item Likert survey and optional demographics. Results are anonymous and visible only in the **Results** tab with the team passcode.

## Advisor view

Advisors see only their own advisees, sorted by who needs attention, with a rule-based prep sheet for each appointment.
