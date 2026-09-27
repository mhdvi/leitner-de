# Leitner Deutsch (لایتنر آلمانی)

A private, offline-first web app (PWA) for learning 6,081 German words, German → Farsi, with the five-box Leitner system. The interface is in Farsi (right-to-left) by default. It can be switched to English on the first screen or in Settings.

This app is a sibling of the English version in `../lightner` and shares its architecture.

## Run it

It's a static site with no build step:

```sh
python tools/serve.py        # http://localhost:8000
```

Any static host works, including GitHub Pages. Both apps can live on the same origin (for example `username.github.io/Leitner/` and `username.github.io/leitner-de/`). Their storage keys and cache names don't overlap.

## What's specific to German

- **Word bank.** The official Goethe-Zertifikat lists for A1, A2 and B1, plus the most frequent B2 words by corpus frequency. Nouns carry their article, tinted by gender (der / die / das), and their plural. Verbs show present, past and Perfekt (`geht · ging · ist gegangen`).
- **Pronunciation.** Uses the device's German speech voice (`de-DE` preferred). Phonetics come from ipa-dict (Wiktionary).
- **Distractors.** Look-alike German words (bitten / bieten / beten) mixed with same-part-of-speech, same-level words.

## Project layout

Same as the English app, plus:

```
js/i18n.js              Farsi and English interface strings, number/date formatting, RTL switch
tools/fa/*.txt          Farsi meanings: `key=meaning`; `key=-` drops a word;
                        `key=meaning|pos|new key` fixes a part of speech or article
tools/build_words.py    rebuilds js/data/words.js (also fixes known Perfekt auxiliary errors in the source)
```

## Editing the word bank

1. Edit `tools/fa/*.txt`.
2. Run `python tools/build_words.py`.
3. Change `VERSION` in `sw.js` so installed copies pick up the new data.
