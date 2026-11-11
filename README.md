# Salita — language trainer

A small installable app for daily language study. Two full decks: Tagalog / Taglish and
Latin American Spanish. Five travel decks for getting by as a visitor: Japanese, Thai,
Dutch, Czech and German. Switch with the language menu at the top; each language keeps
its own progress, streak and settings. Spaced repetition (FSRS-4.5), typed
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
- **Type the answer** and tap Check. Punctuation and "po" are ignored. In Tagalog accents
  are ignored too; in Spanish and German the right word with a wrong accent is graded
  Close (German also takes ae / oe / ue / ss); Dutch and Czech ignore accents unless you
  turn on Settings → Count accents. Japanese and Thai answers can be typed in the
  romanization shown on the card or in the script itself; long vowels, tone marks and
  spacing are not held against you. A near miss counts as Close and suggests Hard. Enter accepts the highlighted grade; 1–4 grade
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

The app uses the phone's built-in text-to-speech. Spanish, Japanese, Thai, Dutch, Czech
and German voices are standard on iPhone.
iOS does not ship a Filipino voice on every device; check Settings › Accessibility ›
Spoken Content › Voices and download one if it is offered. Until a voice for the
language exists (for Tagalog, an Indonesian voice is accepted as an approximation), the
speaker buttons are hidden and the Listen card type stays off.

## The decks

`decks/tagalog.json` and `decks/spanish.json` are the starter decks, built from the topic
files in `decks-src/`. Note formats: `DECK_SCHEMA.md` (Tagalog) and `DECK_SCHEMA_ES.md`
(Spanish). The Tagalog deck is everyday Manila Tagalog and Taglish; the Spanish deck is
Latin American, Mexican-leaning, with `ustedes` and no `vosotros`. Both are organized by
topic and frequency tier. Notes marked `confidence: "check"` are flagged in-app as
unverified; treat them as "ask a native speaker".

The travel decks (`decks/japanese.json`, `thai.json`, `dutch.json`, `czech.json`,
`german.json`; format in `DECK_SCHEMA_TRAVEL.md`) are much smaller, about 465 notes each,
and built around a trip: basics, numbers and time, transport, directions, hotel, food,
shopping, sights, help and health, small talk, signs, hiking and running, and a few
sentence patterns. Polite register throughout. Japanese and Thai notes are written in
the script with a romanization underneath (Settings → Show rōmaji / romanization on the
question, to hide it until you answer). German, Dutch and Czech nouns show their gender
and article. There are no conjugation drills in the travel decks.

Rebuild a deck from its source files:

    python3 tools/deck_tools.py build decks-src/tagalog -o decks/tagalog.json --name "Salita Tagalog starter deck"
    python3 tools/deck_tools.py build decks-src/spanish -o decks/spanish.json --name "Salita Spanish starter deck"
    python3 tools/deck_tools.py build --lang ja decks-src/japanese -o decks/japanese.json --name "Salita Japanese travel deck"
    python3 tools/deck_tools.py build --lang th decks-src/thai -o decks/thai.json --name "Salita Thai travel deck"
    python3 tools/deck_tools.py build --lang nl decks-src/dutch -o decks/dutch.json --name "Salita Dutch travel deck"
    python3 tools/deck_tools.py build --lang cs decks-src/czech -o decks/czech.json --name "Salita Czech travel deck"
    python3 tools/deck_tools.py build --lang de decks-src/german -o decks/german.json --name "Salita German travel deck"
    python3 tools/deck_tools.py stats decks/spanish.json

To add another language: write its topic files, build its deck, add one entry to `LANGS`
near the top of the script in `index.html`, and add the deck file to `SHELL` in `sw.js`
(and bump `CACHE` there so installed copies refresh).

### Growing the deck from real conversations

The app does not generate content; Claude does. `tools/CARD_PROMPT.md` is a prompt you
paste into any Claude chat along with a text thread or notes; it returns a JSON array of
notes for either language. Import that file in Settings → **Import deck JSON** while
that language is selected. Imported notes live alongside the starter deck, can be exported again (Settings → Export my cards) and are
included in backups. You can also add single cards by hand from Browse → **+ Add**.

## Files

- `index.html` — the whole app
- `decks/` — starter decks; `decks-src/` — their per-topic source files
- `sw.js`, `manifest.webmanifest`, `icons/` — offline support and home-screen install
- `tools/deck_tools.py` — validate / build / stats for deck files
- `tools/CARD_PROMPT.md` — prompt for turning conversations into cards
- `DECK_SCHEMA.md`, `DECK_SCHEMA_ES.md`, `DECK_SCHEMA_TRAVEL.md` — note formats
- `.github/workflows/pages.yml` — deploys to GitHub Pages on every push to main
