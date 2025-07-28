# Erasmos

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bonfry/doc_podaster)](https://github.com/bonfry/doc_podaster/releases/latest)
[![GitHub license](https://img.shields.io/github/license/bonfry/doc_podaster)](https://github.com/bonfry/doc_podaster/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/bonfry/doc_podaster)](https://github.com/bonfry/doc_podaster/commits/main)
This project allows you to transform documents into listenable audio tracks. The project is designed to integrate various approaches for document analysis and audio conversion.

## Installation

Clone the repository

```bash
git clone https://github.com/bonfry/doc_podaster.git
```

Install the Python project

```bash
cd erasmos
pip install .[cli] # only cli dependencies
pip install .[api] # only api dependencies
pip install .[all] # all dependencies
```

## CLI

You can get a preview of the parsed document

```bash
erasmos preview <FILENAME>
```

Or convert it to an mp3 file in the same path as the input file

```bash
erasmos convert <FILENAME>
```

## HTTP Server

You can start the FastAPI server

```bash
erasmos-server
```

The web APIs expose the following endpoints:

- `/document/preview`: to preview the document
- `/document/convert`: to convert the document to audio

## Roadmap

The project is currently in a simplified preliminary version. It will be considered an incremental process where features will be added or improved with each version:

### Initial version (v 0.0.1) ☑️

- Initial project structure
- Simplified parsing of Markdown documents
- TTS implementation with Google TTS API

### Increment 1

- Multilingual document handling
- TBD
