"""This module defines the data models for the Erasmos project.

It uses Pydantic for data validation and serialization, ensuring that
the data structures used across the application are consistent and reliable.
"""

from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel


class PartType(StrEnum):
    TEXT = "text"


class DocPart(BaseModel):
    type: PartType = PartType.TEXT
    content: str | object


class DocumentElement(BaseModel):
    """Represents a structured element within a document.

    This class models a generic block of content, such as a paragraph or a
    heading, identified by its type and containing one or more parts.
    """
    parts: list[DocPart]
    children: list[DocumentElement]


class Document(BaseModel):
    """Represents a full document with its content and metadata.

    This is the main model that aggregates the structured content (elements)
    and the metadata of a document.
    """
    id: str
    name: str
    body: DocumentElement
    parsed_body: DocumentElement | None = None
