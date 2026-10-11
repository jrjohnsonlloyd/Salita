# Turn a conversation into Salita cards

Paste this into any Claude chat (cloud or desktop) together with the material you want
cards from: a text thread, a transcript, a list of words you heard, a screenshot of a
group chat, or just "what my tita said at lunch".

---

You are helping me build flashcards for Salita, my spaced-repetition app. The language is
[TAGALOG or SPANISH — say which]. For Spanish, keep every accent and ñ in the Spanish text,
add `"gender": "m"|"f"` on nouns, use Latin American forms (ustedes, no vosotros), and
start the file with {"lang": "es", "notes": [ ... ]}; for Tagalog use {"lang": "tl", "notes": [...]}.
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
- `casual` (optional): how it is actually said colloquially or in a text message (Taglish for Tagalog)
- `notes` (optional, ≤ 160 chars): tone, register, when to use it, whether it is slang
- `examples`: 1–2 natural example sentences as {"tl", "en", "casual"?}. Prefer the real sentence from the conversation.
- For Tagalog verbs add `root`, `focus` (um/mag/in/i/an/ma...) and `aspects` {infinitive, completed, incompleted, contemplated}.
- For Spanish verbs add `root`, `focus` (regular-ar/-er/-ir, stem-change, irregular, reflexive) and `forms` {infinitive, pres_yo, pres_tu, pres_el, pres_nos, pres_ellos, pret_yo, pret_tu, pret_el, pret_nos, pret_ellos, gerund, participle}.
- `confidence`: "high" or "check" if you are unsure it is natural everyday usage.

Also include 1–3 `grammar` notes if the material shows a pattern worth drilling (particle order, a marker, an aspect form), each with `prompt`, `tl` (answer), `en`, `explanation`.

Keep it to the 10–30 most useful items. Validate that the output is valid JSON with no comments or trailing commas.

---

Then: save the reply as a `.json` file (Files app on iPhone or Drive), open Salita, make
sure the matching language is selected, go to Settings → **Import deck JSON**, and pick
the file. The new notes join the new-card
queue by tier. Re-importing a file with the same ids replaces those notes and keeps your
progress on them.

The full schemas are in `DECK_SCHEMA.md` (Tagalog) and `DECK_SCHEMA_ES.md` (Spanish). To check a file on a computer:

    python3 tools/deck_tools.py validate my-cards.json
