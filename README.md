# Leitner Deutsch (لایتنر آلمانی)

A private, offline-first web app (PWA) for learning 6,081 German words, German → Farsi, with the five-box Leitner system. The interface is in Farsi (right-to-left) by default. It can be switched to English on the first screen or in Settings.


## Run it

It's a static site with no build step:

```sh
python tools/serve.py        # http://localhost:8000
```

## What's specific to German

- **Word bank.** The official Goethe-Zertifikat lists for A1, A2 and B1, plus the most frequent B2 words by corpus frequency. Nouns carry their article, tinted by gender (der / die / das), and their plural. Verbs show present, past and Perfekt (`geht · ging · ist gegangen`).
- **Pronunciation.** Uses the device's German speech voice (`de-DE` preferred). Phonetics come from ipa-dict (Wiktionary).
- **Distractors.** Look-alike German words (bitten / bieten / beten) mixed with same-part-of-speech, same-level words.


## Editing the word bank

1. Edit `tools/fa/*.txt`.
2. Run `python tools/build_words.py`.
3. Change `VERSION` in `sw.js` so installed copies pick up the new data.
