# Deck note schema — SPANISH (one JSON array per file)

Audience: an American English speaker (US veteran living abroad) learning everyday
LATIN AMERICAN Spanish, Mexican-leaning neutral: the Spanish he will hear from Mexicans,
Central Americans and Colombians and in US Latino communities. Use `ustedes` (no vosotros),
`tú` as the default informal form, `usted` where politeness matters. Mention Spain-only
forms in `notes` only when a learner will meet them. Register: casual-polite spoken Spanish,
with the colloquial forms people actually use ("¿Qué onda?", "ahorita", "la neta") marked as
such in `notes`.

SPELLING: Spanish words in `tl` MUST carry their correct accents and ñ (está, país, mañana,
¿Qué?). Include ¿ ¡ on questions/exclamations. There is no `stress` field for Spanish.

Every item is a NOTE. The app turns notes into study cards. Fields:

{
  "id": "food-comer-01",           // kebab-case ascii, globally unique: "<file-prefix>-<word>-<nn>" (no accents in ids)
  "type": "vocab" | "phrase" | "verb" | "grammar" | "cloze",
  "tl": "comer",                   // the Spanish headword / phrase / sentence (correct accents!)
  "en": "to eat",                  // concise English meaning (one short gloss, ≤ 8 words)
  "accept": ["eat"],               // OPTIONAL other acceptable English answers (short)
  "accept_tl": ["comer algo"],     // OPTIONAL other acceptable Spanish answers (regional synonyms, variants)
  "pos": "verb",                   // noun|verb|adj|adv|pron|article|prep|conj|interj|expr|num|phrase
  "gender": "m" | "f",             // nouns only, REQUIRED for nouns ("el/la")
  "topic": "food",                 // one lowercase tag: the file's topic
  "tier": 1,                       // 1 = top-500 frequency/essential, 2 = common, 3 = useful, 4 = niche
  "casual": "¿Comemos?",           // OPTIONAL: how it is really said colloquially / in texting, if it differs
  "notes": "Regular -er verb. 'Comida' = food/meal.", // OPTIONAL ≤ 160 chars of usage/culture/grammar/regional info
  "examples": [                    // 1–2 natural example sentences, REQUIRED for vocab/verb/phrase
    {"tl": "¿Ya comiste?", "en": "Did you eat already?", "casual": "¿Ya comiste o qué?"}
  ],
  "confidence": "high" | "check"   // "check" = native-speaker review recommended
}

Type-specific extras:

verb (REQUIRED for type "verb"):
  "root": "com-",                  // stem, or the infinitive class note e.g. "-er regular", "stem-changing o>ue"
  "focus": "regular-er" | "regular-ar" | "regular-ir" | "stem-change" | "irregular" | "reflexive",
  "forms": {
    "infinitive": "comer",
    "pres_yo": "como", "pres_tu": "comes", "pres_el": "come", "pres_nos": "comemos", "pres_ellos": "comen",
    "pret_yo": "comí", "pret_tu": "comiste", "pret_el": "comió", "pret_nos": "comimos", "pret_ellos": "comieron",
    "gerund": "comiendo", "participle": "comido"
  }
  - tl = the infinitive. pres_el covers él/ella/usted; pres_ellos covers ellos/ellas/ustedes. ALL 13 keys required and correct.
  - For reflexive verbs give the pronoun in the form: "me levanto", "te levantas", "se levanta", "nos levantamos", "se levantan".

cloze (type "cloze"): tl is a full sentence with the blanked word in double braces:
  "tl": "Mañana {{voy}} al mercado.", "en": "Tomorrow I'm going to the market.",
  "hint": "ir, present, yo",       // REQUIRED short hint shown to the learner
  "accept_tl": optional alternative fillers. No "examples" needed.

grammar (type "grammar"): a drill with an explicit prompt.
  "prompt": "ser or estar: Ella ___ cansada. (she is tired)",
  "tl": "está",                    // the answer
  "en": "is (temporary state)",
  "explanation": "estar for temporary states/feelings and location; ser for identity, origin, time.", // REQUIRED ≤ 200 chars
  "topic": "grammar"

phrase (type "phrase"): tl is a set phrase/sentence; "en" its meaning; include one example of it in context.

Rules
- Output ONLY a valid JSON array (UTF-8, no comments, no trailing commas). Validate with python3 -c "import json,sys; json.load(open(sys.argv[1]))" before finishing.
- Do not invent words. If unsure a word is in real everyday Latin American use, mark confidence "check" or drop it.
- Vary example sentences; make them about real life (markets, Uber, WhatsApp, apartments, street food, banks, immigration offices, family gatherings).
- Tiers: roughly 40% tier 1, 35% tier 2, 25% tier 3-4 within each topic file.
- Keep English glosses short so they can be graded as typed answers.
