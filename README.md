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


## Your own word lists

Settings → Word lists lets you add your own words and study them in the same Leitner boxes.

- **Adding a list.** Paste words or choose a CSV/TXT file, one `word, meaning` per line. The separator can be a comma, tab, `=`, `:` or `;`; extra columns are further meanings, and an optional last column in `/slashes/` is used as the phonetics. Write nouns with their article (*der Hund*, *das Haus*) and they're tinted by gender like the built-in words. There's a template to download, Excel's Windows-1256 Farsi files are read correctly, and a list holds up to 5,000 words.
- **Studying.** New cards come from your enabled lists first, then from the built-in words. A word that is also in the built-in words is studied from your list, with your meaning. Quiz options for list words draw on the same list (when it has 12 or more words) and on the whole word bank.
- **Switching on and off.** The built-in words and each list have a switch (at least one stays on). A switched-off list is paused and keeps its boxes. Deleting a list removes its words and their progress. Each list can be exported as CSV.
- **Storage.** Lists are saved with your progress, so they're included in the backup file. Resetting progress keeps your lists.

## Editing the word bank

1. Edit `tools/fa/*.txt`.
2. Run `python tools/build_words.py`.
3. Change `VERSION` in `sw.js` so installed copies pick up the new data.
