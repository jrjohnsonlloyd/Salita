# Deck note schema (one JSON array per file)

Audience: an American English speaker (US veteran living in Makati, Metro Manila) learning
everyday Manila Tagalog and natural Taglish as actually spoken/texted in 2026.
Register: casual-polite spoken Tagalog. Prefer the words Manileños actually use
(e.g. "kain tayo", "sige", "ingat") over purist/formal forms; mention the formal
form in `notes` only when a learner will meet it. Use standard spelling (ng/nang
correct, "mga", hyphenated reduplication like "araw-araw"). No diacritics on
Tagalog words EXCEPT the field `stress` (see below). Keep Taglish natural: mixed
sentences the way people text ("Na-late ako kasi traffic").

Every item is a NOTE. The app turns notes into study cards. Fields:

{
  "id": "food-kain-01",            // kebab-case, globally unique: "<file-prefix>-<word>-<nn>"
  "type": "vocab" | "phrase" | "verb" | "grammar" | "cloze",
  "tl": "kumain",                  // the Tagalog headword / phrase / sentence
  "en": "to eat",                  // concise English meaning (one short gloss, ≤ 8 words)
  "accept": ["eat"],               // OPTIONAL other acceptable English answers (short)
  "accept_tl": ["kain"],           // OPTIONAL other acceptable Tagalog answers (spelling variants, synonyms)
  "pos": "verb",                   // noun|verb|adj|adv|pron|particle|marker|conj|interj|expr|num|phrase
  "topic": "food",                 // one lowercase tag: the file's topic
  "tier": 1,                       // 1 = top-500 frequency/essential, 2 = common, 3 = useful, 4 = niche
  "stress": "kumáin",              // OPTIONAL headword with acute accent on stressed vowel, grave for final glottal (bató / batà). Omit if unsure.
  "taglish": "Kain tayo!",         // OPTIONAL: how this is naturally used in Taglish, if it differs or is idiomatic
  "notes": "Root kain. Also 'kain' alone as an invitation.", // OPTIONAL ≤ 160 chars of usage/culture/grammar
  "examples": [                    // 1–2 natural example sentences, REQUIRED for vocab/verb/phrase
    {"tl": "Kumain na ba kayo?", "en": "Have you (all) eaten yet?", "taglish": "Kumain na ba kayo? Order na tayo."}
  ],
  "confidence": "high" | "check"   // "check" = native-speaker review recommended (usage/naturalness unsure)
}

Type-specific extras:

verb (REQUIRED for type "verb"):
  "root": "kain",
  "focus": "um" | "mag" | "in" | "i" | "an" | "ma" | "maka" | "magpa" | "maki" ,
  "aspects": {"infinitive": "kumain", "completed": "kumain", "incompleted": "kumakain", "contemplated": "kakain"}
  - tl = the infinitive. Give both actor-focus and object-focus versions as SEPARATE notes
    only for the ~30 most common roots (e.g. kumain + kainin, bumili + bilhin).

cloze (type "cloze"): tl is a full sentence with the blanked word in double braces:
  "tl": "Pupunta {{ako}} sa mall bukas.", "en": "I will go to the mall tomorrow.",
  "hint": "pronoun: I",            // REQUIRED short hint shown to the learner
  "accept_tl": optional alternative fillers. No "examples" needed.

grammar (type "grammar"): a drill with an explicit prompt.
  "prompt": "Put in natural order: ka / na / ba  (→ 'are you ... already?')",
  "tl": "ka na ba",                // the answer
  "en": "are you ... already?",
  "explanation": "Enclitic order: monosyllabic pronouns (ka) → na/pa → ba.", // REQUIRED ≤ 200 chars
  "topic": "grammar"

phrase (type "phrase"): tl is a set phrase/expression; "en" its meaning; include one example of it in context.

Rules
- Output ONLY a valid JSON array (UTF-8, no comments, no trailing commas). Validate with python3 -c "import json,sys; json.load(open(sys.argv[1]))" before finishing.
- Do not invent words. If unsure a word is in real everyday use, mark confidence "check" or drop it.
- Vary example sentences; make them about real life in Metro Manila (jeep, Grab, GCash, condo, BGC, ulam, kasi, tapos...).
- Tiers: roughly 40% tier 1, 35% tier 2, 25% tier 3-4 within each topic file.
- Keep English glosses short so they can be graded as typed answers.
