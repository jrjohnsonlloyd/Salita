# Deck note schema — TRAVEL decks (Japanese, Thai, Dutch, Czech, German)

Audience: an American English speaker in his twenties, based in Manila, who travels a lot
and wants to get by politely as a visitor: stations and airports, hotels, restaurants,
shops, asking the way, sights, small talk, emergencies. He also runs races and hikes, so
each deck has a small "active" topic. He is NOT trying to become fluent in these
languages. Every note must earn its place on a trip.

Register: polite, neutral, what a courteous adult visitor says to staff and strangers.
- Japanese (`ja`): polite です/ます forms. Normal Japanese writing (kanji + kana) in `tl`,
  modified Hepburn with macrons in `rom` (ō, ū; ん = n, n' before a vowel; は as particle = wa).
- Thai (`th`): Thai script in `tl`. He is male: polite particle ครับ (khráp), "I" = ผม (phǒm);
  give the female form (ค่ะ / คะ, ดิฉัน / ฉัน) in `notes` the first time and where it matters.
  `rom` uses one consistent phrasebook-style romanization with tone marks and long vowels
  doubled: mid = no mark, low = grave (à), falling = circumflex (â), high = acute (á),
  rising = caron (ǎ); aspirated kh / ph / th, unaspirated k / p / t, ng, j, ch;
  syllables of one word joined, words separated by spaces.
- Dutch (`nl`): Netherlands Dutch. `u` with staff and strangers, `je` in casual chat.
- Czech (`cs`): polite `vy` forms with staff and strangers. All diacritics correct.
- German (`de`): standard German as used in Germany, `Sie` with staff and strangers. Mention
  an Austrian or Swiss word in `notes` only where a visitor will meet it (Grüezi, Servus,
  Semmel). Nouns capitalized. ß and umlauts correct.

Every item is a NOTE. The app turns notes into study cards: Recognize (word shown, type
the English), Produce (English shown, type the word: for Japanese and Thai he may type the
romanization), Listen (text-to-speech reads `tl`), Fill the blank, Grammar.

```
{
  "id": "food-water-01",           // kebab-case ASCII, unique: "<file-prefix>-<english or romanized word>-<nn>"
  "type": "vocab" | "phrase" | "cloze" | "grammar",   // NO "verb" type in travel decks: a verb is "vocab" with pos "verb"
  "tl": "水",                      // the word / phrase / sentence in the language's own writing
  "rom": "mizu",                   // Japanese and Thai ONLY, and then REQUIRED on every note. Never on nl / cs / de.
  "en": "water",                   // short English meaning (one gloss, ≤ 8 words) that he can type as an answer
  "accept": ["drinking water"],    // OPTIONAL other acceptable English answers (short)
  "accept_tl": ["お水", "omizu"],  // OPTIONAL other acceptable answers in the language: variants and synonyms.
                                   //   For ja / th give BOTH the native-script form and its romanization.
  "pos": "noun",                   // noun|verb|adj|adv|pron|particle|prep|conj|interj|expr|num|phrase|counter
  "gender": "m",                   // nouns only. de and cs: "m" | "f" | "n". nl: "c" (de-word) | "n" (het-word). Never for ja / th.
  "topic": "food",                 // = the file's topic (see list below)
  "tier": 1,                       // 1 = needed on day one, 2 = common, 3 = useful, 4 = nice to have
  "casual": "...",                 // OPTIONAL and rare: the casual form, only when a visitor will actually hear it a lot
  "notes": "...",                  // OPTIONAL ≤ 160 chars: when to use it, etiquette, a trap, pronunciation tip, plural
  "examples": [                    // 1–2 natural sentences. REQUIRED for vocab and phrase.
    {"tl": "お水をください。", "rom": "Omizu o kudasai.", "en": "Water, please."}   // "rom" required for ja / th, forbidden otherwise
  ],
  "confidence": "high" | "check"   // "check" = you are not sure it is natural / correct: a native speaker should review
}
```

Headwords: no article in `tl` for nouns (German `Bahnhof` with gender "m", not `der Bahnhof`;
Dutch `station` with gender "n"). The app shows the article from `gender`. Verbs in the
dictionary form (Japanese: the ます form, e.g. 食べます, with the plain form in `notes` if useful).

Type-specific rules:

- `phrase`: `tl` is a set phrase or a whole useful sentence ("Where is the toilet?"); `en` its
  meaning; one example showing it in a short exchange or a variation.
- `cloze`: `tl` is a full sentence with exactly one blank in double braces:
  `"tl": "駅は{{どこ}}ですか。"`, `"en": "Where is the station?"`, `"hint": "question word: where"` (REQUIRED).
  For ja / th `rom` is the same sentence with the same blank: `"rom": "Eki wa {{doko}} desu ka."`.
  No `examples` needed. `accept_tl` for other correct fillers.
- `grammar`: a drill with an explicit prompt, for the handful of patterns that let a visitor build
  their own sentences (asking for things, where is X, can I X, I would like X, numbers + counters,
  negation, past/future basics, polite particles).
  `"prompt": "Ask for it politely: コーヒー ___ (coffee, please)"`, `"tl": "をください"`, `"rom": "o kudasai"`,
  `"en": "please (give me)"`, `"explanation": "Thing + をください is the all-purpose polite request."` (REQUIRED ≤ 200 chars),
  `"topic": "grammar"`. The prompt is written so he can read it without knowing the script
  (for ja / th put the romanization in the prompt in parentheses when you show native text).

## Files and sizes

One JSON array per file in `decks-src/<language>/`. File name = topic = id prefix.

| file | topic | about | notes |
|---|---|---|---|
| `basics.json` | basics | greetings, please / thank you / sorry, yes / no, I don't understand, do you speak English, essential little words | 45 |
| `time.json` | time | numbers, counting things and people, clock time, days, dates, today / tomorrow, how long | 40 |
| `travel.json` | travel | airport, trains, metro, buses, taxis, tickets, platforms, IC cards / passes, delays | 45 |
| `directions.json` | directions | where is, left / right / straight, near / far, map, landmarks, lost | 30 |
| `stay.json` | stay | hotel check-in / out, room problems, luggage, wifi, laundry | 30 |
| `food.json` | food | restaurants, ordering, the bill, dishes and drinks a visitor meets, allergies, "no meat", convenience stores / cafés / bars | 55 |
| `money.json` | money | shopping, prices, paying (cash / card), sizes, tax-free, ATMs, bargaining only where it is done | 35 |
| `sights.json` | sights | temples / churches / museums / castles, tickets, opening hours, photos, weather, nature | 30 |
| `help.json` | help | emergencies, pharmacy, doctor, body and symptoms, police, lost things, safety | 35 |
| `chat.json` | chat | small talk: where are you from, I'm from the US, I live in the Philippines, first time here, compliments, cheers, goodbyes | 35 |
| `signs.json` | signs | words READ on signs, buttons, menus and tickets: exit, entrance, push / pull, closed, no smoking, toilets, men / women, platform, sold out | 30 |
| `active.json` | active | hiking (trail, summit, hut, how long to the top, weather turning), running and races (start, finish, bib pickup, water station), gym, sore / tired | 25 |
| `grammar.json` | grammar | 15 `grammar` drills + 15 `cloze` sentences on the highest-yield patterns | 30 |

About 465 notes per language. Within each topic file: roughly 45% tier 1, 35% tier 2, 20% tier 3–4,
and roughly half single words (`vocab`), half `phrase`.

## Rules

- Output ONLY valid JSON arrays (UTF-8, no comments, no trailing commas).
- Do not invent words or phrases. If unsure something is correct and natural, mark `"confidence": "check"` or drop it.
- No duplicates across files: one note per word and meaning (the builder merges exact repeats, but do not rely on it).
- Keep English glosses short and typeable; put alternatives in `accept`.
- Examples are about real travel situations in that country (real station names, dishes, apps, places).
- Check with: `python tools/deck_tools.py validate --lang <ja|th|nl|cs|de> decks-src/<language>/*.json`
