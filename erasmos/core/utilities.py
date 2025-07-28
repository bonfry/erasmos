"""This module provides utility functions for the Erasmos project.

It contains helper functions for file operations, text processing, and
other common tasks that are shared across different modules.
"""

import re
import random
import subprocess
from pathlib import Path
from typing import Callable
from .models import DocumentElement


def get_raw_text(text: str):

    raw_text = re.sub(r'!$([^$]*)$$[^$]+$', r'\1', text)
    raw_text = re.sub(r'$([^$]+)$$[^$]+$', r'\1', raw_text)
    raw_text = re.sub(r'^\s*#+\s+', '', raw_text, flags=re.MULTILINE)
    raw_text = re.sub(r'(\*\*|__|\*|_|~~)(.*?)\1', r'\2', raw_text)
    raw_text = re.sub(r'`([^`]+)`', r'\1', raw_text)
    raw_text = re.sub(r'^\s*>\s?', '', raw_text, flags=re.MULTILINE)
    raw_text = re.sub(r'^\s*([*\-+])\s+', '', raw_text, flags=re.MULTILINE)
    raw_text = re.sub(r'^\s*\d+\.\s+', '', raw_text, flags=re.MULTILINE)
    raw_text = re.sub(r'^\s*([-*_]){3,}\s*$', '', raw_text, flags=re.MULTILINE)
    raw_text = re.sub(r'\n{2,}', '\n', raw_text).strip()

    return raw_text.strip()


def merge_element(el: DocumentElement):
    return ''.join([str(p.content) for p in el.parts])


def transform_element(el: DocumentElement, method: Callable[[DocumentElement], DocumentElement], recursive=False):

    new_el = method(el)

    new_el.children = [
        transform_element(child, method, recursive)
        for child in el.children]

    return new_el


def merge_mp3s(input_files: list[str], output_file):
    if not input_files:
        print("Errore: La lista dei file di input è vuota.")
        return

    command = ["ffmpeg", "-y"]

    for f in input_files:
        command += ["-i", f]

    command.append('-filter_complex')

    filter = ""

    for i in range(len(input_files)):
        filter += f"[{i}:a]"

    filter += f"concat=n={len(input_files)}:v=0:a=1[out]"
    command.append(filter)
    command += ["-map", "[out]", output_file]

    subprocess.run(command)


def transform_element_to_audio(el: DocumentElement, method: Callable[[DocumentElement], str], recursive=True) -> str:

    main_audio = method(el)

    children_audio = [
        transform_element_to_audio(child, method, recursive)
        for child in el.children]

    audio_files = [main_audio] + children_audio

    if len(audio_files) > 1:
        filename = f"tmp/{random_code(10)}.mp3"
        merge_mp3s(audio_files, filename)
        return filename
    else:
        return main_audio


def random_code(size=10):
    __random_bucket__ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTSUVWXYZ1234567890'

    result = ""

    for _ in range(size):
        next_char_code = random.randint(0, len(__random_bucket__)-1)
        result += __random_bucket__[next_char_code]

    return result


def sanitize_name(name: str):
    """Sanitizes a string to be used as a valid filename.

    Removes special characters and replaces spaces with underscores.

    Args:
        name: The string to sanitize.

    Returns:
        A sanitized string suitable for use in a filename.
    """
    return (
        name
        .lower()
        .replace(" ", "_",)
    )


def validate_file_extension(path: Path, extension: str):
    """Validate file with a specific extension"""
    if path and not str(path).endswith(f'.{extension}'):
        raise Exception(f'File must be a .{extension} file')
    return path
