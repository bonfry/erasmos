import os
from pathlib import Path
from ...cli import utilities
from ...core import tts as ttslib
from ...core.models import Document
from fastapi.responses import FileResponse
from ...core.parser import parse_markdown_file
from ...core import meta_document as metadoclib
from fastapi import APIRouter, Depends, UploadFile

router = APIRouter()


@router.post("/preview")
def preview(
        file: UploadFile,
        meta: metadoclib.MetaDocumentGenerator = metadoclib.MetaDocumentGenerator.UNMARKDOWN):

    metadoc_method = getattr(metadoclib, meta)
    input_filename = Path(file.filename)
    utilities.validate_file_extension(input_filename, 'md')

    doc = parse_markdown_file(file.file)
    doc = metadoc_method(doc)

    if doc.parsed_body:
        stack = [doc.parsed_body]
        merged_parts = []

        while stack:
            el = stack.pop(0)
            content = ''.join([str(p.content) for p in el.parts])
            merged_parts.append(content)

            stack = el.children + stack

        doc_content = ''.join(merged_parts)

        tmp_output_path = (
            Path("tmp")
            / input_filename.with_suffix('.output.txt'))

        with open(tmp_output_path, "w") as f:
            f.write(doc_content)

        return FileResponse(
            tmp_output_path,
            filename=str(input_filename.with_suffix('.txt')))

    else:
        raise Exception("Metadocument parsing failed!")


@router.post("/convert")
def convert(
        file: UploadFile,
        meta: metadoclib.MetaDocumentGenerator = metadoclib.MetaDocumentGenerator.UNMARKDOWN,
        tts: ttslib.TTSEngines = ttslib.TTSEngines.GOOGLE_TTS,
        lang: str = "en"):

    metadoc_method = getattr(metadoclib, meta)
    tts_method = getattr(ttslib, tts)
    input_filename = Path(file.filename)

    utilities.validate_file_extension(input_filename, 'md')

    doc = parse_markdown_file(file.file)
    doc = metadoc_method(doc)
    audio_path = tts_method(doc)
    audio_path = Path(audio_path)

    return FileResponse(
        audio_path,
        filename=str(input_filename.with_suffix('.mp3')))
