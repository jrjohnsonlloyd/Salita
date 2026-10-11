# Salita — Tagalog / Taglish trainer

A small installable app for daily Tagalog study. Spaced repetition (FSRS-4.5), typed
answers with forgiving grading, verb aspect drills, fill-the-blank and grammar cards,
Taglish "how would a friend text this" cards, optional listening cards, streaks and
progress charts. Everything runs in one HTML file and works offline. Nothing leaves the
phone.

Live: https://jrjohnsonlloyd.github.io/salita/

## Install on iPhone

1. Open the link above in Safari.
2. Share → **Add to Home Screen**.
3. Open it from the home screen once while online so it caches itself for offline use.

Progress is stored in the app's own browser storage. Deleting the home-screen app
deletes the progress, so back up now and then (Settings → Share backup → save to Files
or Drive). Restore merges, so restoring an old backup never loses newer progress.

## How a session works

- **New words** appear once with meaning, example and notes ("Got it"), then come back as
  a test later in the same session.
- **Type the answer** and tap Check. Accents, punctuation and "po" are ignored; a near
  miss counts as Close and suggests Hard. Enter accepts the highlighted grade; 1–4 grade
  directly on a keyboard.
- **Grades**: Again = would not have produced it (card returns in a few minutes).
  Hard = got it, slowly. Good = fine. Easy = instant. The buttons show the next interval.
- **Card types** per note: Recognize (Tagalog → English), Produce (English → Tagalog),
  Listen (hear it, type it), Taglish (self-graded), Verb aspect (completed /
  incompleted / contemplated), Fill the blank, Grammar. Produce, Listen, Taglish and
  aspect cards unlock after the Recognize card has been passed once. Turn any type or
  topic off in Settings.
- **Daily load** defaults to 15 new cards a day plus whatever is due. "Learn 10 more"
  on the summary screen adds extra new cards when you want them.

### Listening cards and audio

The app uses the phone's built-in text-to-speech. iOS does not ship a Filipino voice on
every device; check Settings › Accessibility › Spoken Content › Voices and download one
if it is offered. Until a Filipino (or, approximately, Indonesian) voice exists, the
speaker buttons are hidden and the Listen card type stays off.

## The deck

`deck.json` is the starter deck (see `DECK_SCHEMA.md` for the note format). It was
written for everyday Manila Tagalog and Taglish, organized by topic and frequency tier.
Notes marked `confidence: "check"` are flagged in-app as unverified; treat them as "ask a
Filipino friend".

Build the deck from source files:

    python3 tools/deck_tools.py build deck-src/ -o deck.json --name "Salita starter deck"
    python3 tools/deck_tools.py stats deck.json

### Growing the deck from real conversations

The app does not generate content; Claude does. `tools/CARD_PROMPT.md` is a prompt you
paste into any Claude chat along with a text thread or notes; it returns a JSON array of
notes. Import that file in Settings → **Import deck JSON**. Imported notes live
alongside the starter deck, can be exported again (Settings → Export my cards) and are
included in backups. You can also add single cards by hand from Browse → **+ Add**.

## Files

- `index.html` — the whole app
- `deck.json` — starter deck
- `sw.js`, `manifest.webmanifest`, `icons/` — offline support and home-screen install
- `tools/deck_tools.py` — validate / build / stats for deck files
- `tools/CARD_PROMPT.md` — prompt for turning conversations into cards
- `DECK_SCHEMA.md` — note format
- `.github/workflows/pages.yml` — deploys to GitHub Pages on every push to main
