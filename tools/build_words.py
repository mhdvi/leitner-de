"""Builds js/data/words.js from the Farsi translation files in tools/fa/.

Sources (downloaded into tools/.cache on first run):
  - German vocabulary with CEFR levels, articles, plurals and verb forms
    (Goethe-Zertifikat word lists A1–B1, B2 from corpus frequency)
  - German IPA dictionary (ipa-dict, derived from Wiktionary)

Translation lines look like `key=farsi`, where key is the word as listed
(nouns with their article). Two optional overrides may follow:
  `key=farsi|pos`             fix the part of speech
  `key=farsi|pos|new key`     also fix the displayed word (e.g. a wrong article)
A meaning of `-` drops the word.

Usage:  python tools/build_words.py
"""
import glob, json, os, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, '.cache')
OUT = os.path.join(ROOT, '..', 'js', 'data', 'words.js')

SOURCES = {
    'de_vocab.json': 'https://raw.githubusercontent.com/ismavid/wortmeister/HEAD/data/vocab.v1.json',
    'de_ipa.txt': 'https://raw.githubusercontent.com/open-dict-data/ipa-dict/master/data/de.txt',
}
POS = {'noun': 'n', 'verb': 'v', 'adj': 'adj', 'adv': 'adv', 'prep': 'prep', 'conj': 'conj',
       'pron': 'pron', 'num': 'num', 'intj': 'excl'}
LEVELS = ['a1', 'a2', 'b1', 'b2']
ARTICLES = ('der ', 'die ', 'das ')
AUX = {'haben': 'hat', 'sein': 'ist'}  # Perfekt shown as 'hat gemacht' / 'ist gegangen'

# The source marks some verbs of motion or change with the wrong auxiliary.
SEIN = set('''fahren abfahren losfahren wegfahren zurückfahren mitfahren fliegen abfliegen aufstehen fallen
auffallen ausfallen einfallen hinfallen umfallen steigen aufsteigen einsteigen aussteigen umsteigen absteigen
sterben wachsen aufwachsen passieren geschehen gelingen misslingen entstehen reisen verreisen anreisen
abreisen einreisen umziehen einziehen folgen begegnen springen rennen schwimmen wandern laufen landen
sinken versinken verschwinden erscheinen einschlafen aufwachen erwachen ankommen zurückkehren fliehen
flüchten stürzen scheitern gelangen geraten auftreten eintreten eintreffen gehen ausgehen weggehen
kommen zurückkommen mitkommen herauskommen bleiben verbleiben werden sein wachsen explodieren
ausbrechen aufbrechen entkommen erkranken ertrinken gleiten kriechen reiten rutschen schleichen
schreiten stolpern ausweichen zerbrechen vergehen umkehren zurückgehen weitergehen
aufgehen untergehen durchfallen aussterben'''.split())

# Forms that are simply wrong in the source.
FORMS = {
    'reisen': 'reist · reiste · ist gereist',
    'verreisen': 'verreist · verreiste · ist verreist',
    'unterschreiben': 'unterschreibt · unterschrieb · hat unterschrieben',
    'winken': 'winkt · winkte · hat gewinkt',
}


def fetch(name):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        print('downloading', name)
        urllib.request.urlretrieve(SOURCES[name], path)
    return path


def strip_article(word):
    for a in ARTICLES:
        if word.startswith(a):
            return word[len(a):]
    return word


def main():
    translations = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'fa', '*.txt'))):
        for line in open(f, encoding='utf-8'):
            line = line.strip()
            if not line:
                continue
            key, _, rest = line.partition('=')
            parts = rest.split('|')
            if parts[0] != '-':
                translations[key] = parts

    data = json.load(open(fetch('de_vocab.json'), encoding='utf-8'))
    fields = data['fields']
    entries = {}
    for row in data['words']:
        w = dict(zip(fields, row))
        key = (w['article'] + ' ' + w['lemma']).strip()
        entries.setdefault(key, w)

    ipa = {}
    for line in open(fetch('de_ipa.txt'), encoding='utf-8'):
        k, _, v = line.rstrip('\n').partition('\t')
        if k not in ipa:
            ipa[k] = v.split(',')[0].strip().strip('/')

    def pronounce(lemma):
        if lemma in ipa:
            return ipa[lemma]
        parts = [ipa.get(p) or ipa.get(p.lower()) for p in lemma.split()]
        return ' '.join(parts) if all(parts) else ''

    rows = []
    missing = []
    for key, parts in translations.items():
        w = entries.get(key)
        if not w:
            missing.append(key)
            continue
        fa = parts[0]
        pos = parts[1] if len(parts) > 1 and parts[1] else POS.get(w['pos'], '')
        word = parts[2] if len(parts) > 2 else key
        lemma = strip_article(word)
        if w['pos'] == 'noun' and len(parts) < 3:
            extra = w['plural'] if w['plural'] and w['plural'] != lemma else ''
        elif w['pos'] == 'verb' and w['pp'] and pos == 'v':
            aux = 'ist' if lemma in SEIN else '/'.join(AUX.get(a, a) for a in w['aux'].split('/') if a)
            extra = FORMS.get(lemma) or ' · '.join(x for x in (w['p3'], w['prt'], f"{aux} {w['pp']}".strip()) if x)
        else:
            extra = ''
        level = w['level'].rstrip('*').lower()
        rows.append((LEVELS.index(level), -w['priority'], [word, fa, pronounce(lemma), pos, level, extra]))

    if missing:
        raise SystemExit(f'unknown keys in translations: {missing[:20]}')

    rows.sort(key=lambda r: (r[0], r[1]))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('// Generated by tools/build_words.py. Do not edit by hand.\n')
        f.write('// [word (nouns with article), farsi, ipa, part of speech, level, plural or verb forms]\n')
        f.write('export default [\n')
        for _, _, r in rows:
            f.write(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + ',\n')
        f.write('];\n')
    counts = {l: sum(1 for r in rows if r[2][4] == l) for l in LEVELS}
    no_ipa = sum(1 for r in rows if not r[2][2])
    print(f'{len(rows)} words written to {os.path.relpath(OUT)}', counts, f'without IPA: {no_ipa}')


if __name__ == '__main__':
    main()
