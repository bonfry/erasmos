"""This module is responsible for generating document metadata.

It provides strategies for extracting key information from a document's
structured content, such as the title and abstract.
"""

from enum import StrEnum

from .models import *
from .utilities import transform_element, get_raw_text


class MetaDocumentGenerator(StrEnum):
    """Enum for different document metadata generators.

    Each member of this enum represents a strategy for generating a
    specific piece of metadata, such as the title or abstract.
    """

    UNMARKDOWN = 'unmarkdown'

    @classmethod
    def options(cls):
        return [c.value for c in cls] # pyrefly: ignore


def unmarkdown(doc: Document) -> Document:
    """Unmarkdown the document.

    This function takes a Document object, processes its elements to
    remove markdown formatting, and returns the modified Document.

    Args:
        doc: The Document object to be unmarkdown.

    Returns:
        The unmarkdown Document object.
    """

    def unmarkdown_el(el: DocumentElement) -> DocumentElement:
        el.parts = [
            DocPart(content=get_raw_text(str(p.content)))
            for p in el.parts
        ]

        return el

    parsed_body: DocumentElement = transform_element(
        doc.body, 
        unmarkdown_el,
        recursive=True)

    doc.parsed_body = parsed_body

    return doc
