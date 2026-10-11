#!/usr/bin/env python3
"""Salita deck tools: validate, merge and summarize note files.

  python3 tools/deck_tools.py validate FILE [FILE...]
  python3 tools/deck_tools.py build  -o decks/tagalog.json --name "Salita starter deck" decks-src/tagalog
  python3 tools/deck_tools.py stats  deck.json

Notes follow DECK_SCHEMA.md. `build` concatenates all input arrays, checks every note,
merges notes that share a headword and meaning across files, de-duplicates ids by appending a suffix,
and writes {"name", "version", "notes": [...]}.
"""
import json, sys, os, re, argparse, datetime

TYPES = {'vocab', 'phrase', 'verb', 'grammar', 'cloze'}
ASPECTS = ('infinitive', 'completed', 'incompleted', 'contemplated')
ES_FORMS = ('infinitive', 'pres_yo', 'pres_tu', 'pres_el', 'pres_nos', 'pres_ellos', 'pret_yo', 'pret_tu', 'pret_el', 'pret_nos', 'pret_ellos', 'gerund', 'participle')
ID_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')

def problems(n):
    p = []
    if not isinstance(n, dict): return ['not an object']
    for k in ('id', 'type', 'tl', 'en', 'topic'):
        if not n.get(k) or not isinstance(n[k], str): p.append('missing ' + k)
    if p: return p
    if n['type'] not in TYPES: p.append('bad type ' + n['type'])
    if not ID_RE.match(n['id']): p.append('id not kebab-case: ' + n['id'])
    if not isinstance(n.get('tier', 2), int) or not 1 <= n.get('tier', 2) <= 4: p.append('tier must be 1-4')
    if n.get('confidence') not in (None, 'high', 'check'): p.append('confidence must be high|check')
    for k in ('accept', 'accept_tl'):
        if k in n and (not isinstance(n[k], list) or not all(isinstance(x, str) for x in n[k])): p.append(k + ' must be a list of strings')
    ex = n.get('examples', [])
    if not isinstance(ex, list): p.append('examples must be a list')
    else:
        for e in ex:
            if not isinstance(e, dict) or not e.get('tl') or not e.get('en'): p.append('example needs tl and en')
    if n['type'] in ('vocab', 'verb', 'phrase') and not ex: p.append('needs at least one example')
    if n['type'] == 'verb':
        a = n.get('aspects'); f = n.get('forms')
        if isinstance(f, dict):
            missing = [k for k in ES_FORMS if not f.get(k)]
            if missing: p.append('verb forms missing ' + '/'.join(missing))
        elif not isinstance(a, dict) or not all(a.get(k) for k in ASPECTS): p.append('verb needs aspects ' + '/'.join(ASPECTS) + ' or forms')
        if not n.get('root'): p.append('verb needs root')
        if not n.get('focus'): p.append('verb needs focus')
    if n['type'] == 'cloze':
        if len(re.findall(r'\{\{.+?\}\}', n['tl'])) != 1: p.append('cloze needs exactly one {{blank}}')
        if not n.get('hint'): p.append('cloze needs hint')
    if n['type'] == 'grammar':
        if not n.get('prompt'): p.append('grammar needs prompt')
        if not n.get('explanation'): p.append('grammar needs explanation')
    return p

def load(paths):
    notes = []
    for path in paths:
        if os.path.isdir(path):
            for f in sorted(os.listdir(path)):
                if f.endswith('.json'): notes.extend(load([os.path.join(path, f)]))
            continue
        with open(path, encoding='utf-8') as fh: data = json.load(fh)
        arr = data if isinstance(data, list) else data.get('notes', [])
        for n in arr:
            if isinstance(n, dict): n['_src'] = os.path.basename(path)
        notes.extend(arr)
    return notes

def key(n): return (n.get('type'), re.sub(r'\s+', ' ', n.get('tl', '').strip().lower()), n.get('en', '').strip().lower())

def cmd_validate(args):
    bad = 0
    for path in args.files:
        notes = load([path])
        for n in notes:
            pr = problems(n)
            if pr: bad += 1; print(f"{path}: {n.get('id', '?') if isinstance(n, dict) else '?'}: {'; '.join(pr)}")
        print(f"{path}: {len(notes)} notes, {sum(1 for n in notes if problems(n))} with problems")
    return 1 if bad else 0

STOP = {'to', 'the', 'a', 'an', 'be', 'is', 'are', 'of', 'in', 'on', 'at', 'for', 'and', 'or', 'it', 'you', 'i', 'me', 'my', 'your'}
def words(s): return {w for w in re.findall(r"[a-z']+", s.lower()) if w not in STOP}
import unicodedata
def norm_tl(s):
    s = unicodedata.normalize('NFD', s.strip().lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r"[^a-z0-9ñ\s-]", '', re.sub(r'\s+', ' ', s).replace("'", ''))
RANK = {'verb': 0, 'vocab': 1, 'phrase': 2, 'cloze': 3, 'grammar': 3}

def merge_into(keep, other):
    """Fold `other` into `keep`: union accept lists and examples, keep the lower tier and any taglish/stress/notes missing."""
    for k in ('accept', 'accept_tl'):
        vals = list(keep.get(k, [])) + [v for v in other.get(k, []) if v not in keep.get(k, [])]
        if vals: keep[k] = vals
    if other.get('en') and other['en'] != keep.get('en'):
        keep.setdefault('accept', [])
        if other['en'] not in keep['accept']: keep['accept'].append(other['en'])
    seen = {e['tl'].strip().lower() for e in keep.get('examples', [])}
    for e in other.get('examples', []):
        if e['tl'].strip().lower() not in seen and len(keep.setdefault('examples', [])) < 3: keep['examples'].append(e); seen.add(e['tl'].strip().lower())
    keep['tier'] = min(keep.get('tier', 2), other.get('tier', 2))
    for k in ('taglish', 'casual', 'stress', 'notes', 'pos', 'gender'):
        if not keep.get(k) and other.get(k): keep[k] = other[k]
    if other.get('confidence') == 'check': keep['confidence'] = 'check'

ART = re.compile(r'^(el|la|los|las|un|una)\s+(?=\S)', re.I)
def strip_article(n):
    """Spanish nouns: keep the bare noun as the headword, accept the article form as an alternative."""
    if n.get('type') != 'vocab' or not n.get('gender'): return
    m = ART.match(n['tl'])
    if not m: return
    full = n['tl']; n['tl'] = n['tl'][m.end():]
    n.setdefault('accept_tl', [])
    if full not in n['accept_tl']: n['accept_tl'].insert(0, full)

def same_sense(a, b):
    """Same headword and overlapping meaning (shared content word, or verb vs vocab tagged as verb)."""
    if a['type'] in ('cloze', 'grammar') or b['type'] in ('cloze', 'grammar'): return False
    ea, eb = words(a['en']), words(b['en'])
    if ea & eb: return True
    return {a['type'], b['type']} == {'verb', 'vocab'} and (a.get('pos') == 'verb' or b.get('pos') == 'verb')

def cmd_build(args):
    notes = load(args.src)
    out, seen_ids, by_tl, merged, bad = [], {}, {}, 0, 0
    for n in notes:
        pr = problems(n)
        if pr: bad += 1; print(f"skip {n.get('id', '?') if isinstance(n, dict) else '?'} ({n.get('_src') if isinstance(n, dict) else ''}): {'; '.join(pr)}", file=sys.stderr); continue
        n.pop('_src', None)
        strip_article(n)
        tl = norm_tl(n['tl'])
        target = next((m for m in by_tl.get(tl, []) if same_sense(m, n)), None)
        if target is not None:
            # keep the richer type (verb > vocab > phrase); fold the other in
            if RANK.get(n['type'], 3) < RANK.get(target['type'], 3):
                merge_into(n, target); out[out.index(target)] = n; by_tl[tl][by_tl[tl].index(target)] = n; n['id'] = target['id']
            else: merge_into(target, n)
            merged += 1; continue
        base = n['id']; i = 2
        while n['id'] in seen_ids: n['id'] = f"{base}-{i}"; i += 1
        seen_ids[n['id']] = 1
        out.append(n); by_tl.setdefault(tl, []).append(n)
    deck = {'name': args.name, 'version': args.version or datetime.date.today().isoformat(), 'notes': out}
    with open(args.output, 'w', encoding='utf-8') as fh: json.dump(deck, fh, ensure_ascii=False, separators=(',', ':'))
    print(f"wrote {args.output}: {len(out)} notes ({merged} same-word duplicates merged, {bad} invalid skipped)")
    return 0

def cmd_stats(args):
    with open(args.file, encoding='utf-8') as fh: data = json.load(fh)
    notes = data if isinstance(data, list) else data['notes']
    from collections import Counter
    print(f"{len(notes)} notes · version {data.get('version', '?') if isinstance(data, dict) else '?'}")
    for label, c in (('by type', Counter(n['type'] for n in notes)), ('by topic', Counter(n['topic'] for n in notes)), ('by tier', Counter(n.get('tier', '?') for n in notes))):
        print(label + ': ' + ', '.join(f"{k} {v}" for k, v in sorted(c.items(), key=lambda kv: str(kv[0]))))
    print(f"flagged for review (confidence=check): {sum(1 for n in notes if n.get('confidence') == 'check')}")
    print(f"with casual/taglish variant: {sum(1 for n in notes if n.get('taglish') or n.get('casual') or any(e.get('taglish') or e.get('casual') for e in n.get('examples', [])))}")
    return 0

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate'); v.add_argument('files', nargs='+'); v.set_defaults(fn=cmd_validate)
    b = sub.add_parser('build'); b.add_argument('src', nargs='+'); b.add_argument('-o', '--output', default='deck.json'); b.add_argument('--name', default='Salita starter deck'); b.add_argument('--version', default=''); b.set_defaults(fn=cmd_build)
    s = sub.add_parser('stats'); s.add_argument('file'); s.set_defaults(fn=cmd_stats)
    a = ap.parse_args(); sys.exit(a.fn(a))

if __name__ == '__main__': main()
