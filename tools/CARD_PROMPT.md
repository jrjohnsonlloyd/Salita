# Turn a conversation into Salita cards

Paste this into any Claude chat (cloud or desktop) together with the material you want
cards from: a text thread, a transcript, a list of words you heard, a screenshot of a
group chat, or just "what my tita said at lunch".

---

You are helping me build flashcards for Salita, my Tagalog/Taglish spaced-repetition app.
Read the attached conversation / notes and extract the words, phrases and grammar
patterns worth learning. Skip anything I clearly already know (basic greetings, numbers)
unless the usage is interesting.

Output ONLY a JSON array of notes following this schema (one object per note):

- `id`: kebab-case, unique, prefixed with today's date, e.g. "2026-10-11-marites-01"
- `type`: "vocab" | "phrase" | "verb" | "cloze" | "grammar"
- `tl`: the Tagalog/Taglish headword or sentence. For cloze, put the blank in {{double braces}} and add `hint`.
- `en`: a short English gloss (≤ 8 words) that I can type as an answer
- `accept` (optional): other acceptable English answers
- `accept_tl` (optional): other acceptable Tagalog spellings/variants
- `pos`: noun | verb | adj | adv | particle | expr | phrase | ...
- `topic`: a short tag, e.g. "chat", "food", "work", or the person/place it came from
- `tier`: 1 if I will hear it daily, 2 common, 3 useful, 4 niche
- `taglish` (optional): how it is actually used in a mixed text message
- `notes` (optional, ≤ 160 chars): tone, register, when to use it, whether it is slang
- `examples`: 1–2 natural example sentences as {"tl", "en", "taglish"?}. Prefer the real sentence from the conversation.
- For verbs add `root`, `focus` (um/mag/in/i/an/ma...) and `aspects` {infinitive, completed, incompleted, contemplated}.
- `confidence`: "high" or "check" if you are unsure it is natural everyday usage.

Also include 1–3 `grammar` notes if the material shows a pattern worth drilling (particle order, a marker, an aspect form), each with `prompt`, `tl` (answer), `en`, `explanation`.

Keep it to the 10–30 most useful items. Validate that the output is a single JSON array with no comments or trailing commas.

---

Then: save the reply as a `.json` file (Files app on iPhone or Drive), open Salita →
Settings → **Import deck JSON**, and pick the file. The new notes join the new-card
queue by tier. Re-importing a file with the same ids replaces those notes and keeps your
progress on them.

The full schema is in `DECK_SCHEMA.md`. To check a file on a computer:

    python3 tools/deck_tools.py validate my-cards.json
