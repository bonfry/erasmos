"""This module provides text-to-speech (TTS) functionality.

It uses gTTS (Google Text-to-Speech) to convert text into speech and saves
the output as an MP3 file. It includes a simple caching mechanism to avoid
regenerating audio for the same text.
"""

import os
from gtts import gTTS
from enum import StrEnum
from .models import DocumentElement, Document
from .utilities import transform_element_to_audio, random_code, sanitize_name


class TTSEngines(StrEnum):
    GOOGLE_TTS = 'google_tts'

    @classmethod
    def options(cls):
        return [c.value for c in cls]  # pyrefly: ignore


def google_tts(doc: Document, lang='en') -> str:
    """Converts a string of text to an audio file using Google TTS.

        The generated audio file is saved in a temporary directory. A hash of
        the input text is used as the filename to cache results and prevent
        redundant API calls.

        Args:
            text: The text to convert to speech.
            lang: The language of the text (e.g., 'en', 'it').
            slow: If True, the speech will be read at a slower pace.
            tld: The top-level domain for the Google TTS service (e.g., 'com', 'co.uk').

        Returns:
            The path to the generated MP3 audio file.
    """
    def generate_tts(el: DocumentElement):
        text = ''.join([str(p.content) for p in el.parts])
        audio = gTTS(text, lang=lang)

        filename = f"tmp/{random_code(10)}.mp3"

        audio.save(filename)
        return filename

    if doc.parsed_body:
        last_filename = transform_element_to_audio(
            doc.parsed_body,
            generate_tts,
            recursive=True)

        final_filename = f"output/{sanitize_name(doc.name)}.mp3"

        os.rename(last_filename, final_filename)
        return final_filename
    else:
        raise ValueError("parsed_body not generated")
