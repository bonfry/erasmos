# Erasmos

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bonfry/doc_podaster)](https://github.com/bonfry/doc_podaster/releases/latest)
[![GitHub license](https://img.shields.io/github/license/bonfry/doc_podaster)](https://github.com/bonfry/doc_podaster/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/bonfry/doc_podaster)](https://github.com/bonfry/doc_podaster/commits/main)

Questo progetto consente di trasformare i documenti in tracce audio da ascoltare. Il progetto è pensato per integrare diversi approcci per l'analisi del documento e la sua trasformazione in audio.

## Installazione

Scaricare il repository

```bash
git clone https:// 
``` 

Installare il progetto python

```bash
cd erasmos
pip install .[cli] # only cli dependencies
pip install .[api] # only api dependencies
pip install .[all] # all dependencies
``` 

## CLI

Puoi ottenere la preview del documento analizzato

```bash
erasmos preview <FILENAME>
```

Oppure convertirlo in file mp3 nello stesso path del file di input

```bash
erasmos convert <FILENAME>
```

## HTTP Server
E' possibile avviare il server di FastAPI 
```bash
erasmos-server
```

Le api web presentano i seguenti endpoint: 
- `/document/preview`: per effettuare la preview delle api

- `/document/convert`: per convertire il documento in audio

## Roadmap

Al momento il progetto è in una versione preliminare semplificata. Al momento verrà considerato come un processo incrementale dove ad ogni versione verranno aggiunte o migliorate determinate funzionalità:

### Versione iniziale (v 0.0.1) ☑️
- Struttura iniziale del progetto
- Parsing semplificato dei documenti Markdown
- Implementazione TTS con api di Google TTS

### Incremento 1
- Gestione multilingua dei documenti
- TBD