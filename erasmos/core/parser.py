"""This module provides document parsing capabilities for the Erasmos project.

It is responsible for reading files (e.g., Markdown) and transforming them
into a structured representation using the data models defined in the project.
"""
import mistletoe
from . import models
from ast import Return
from _io import _IOBase
from pathlib import Path
from shutil import Error
from mistletoe import Document
from mistletoe.block_token import Heading
from mistletoe.markdown_renderer import MarkdownRenderer

def parse_markdown_file(f: str | Path | _IOBase) :
    """Parses a Markdown file from various sources.

    This function can handle a file path (as a string or Path object) or a
    file-like object.

    Args:
        f: The source of the Markdown content.

    Raises:
        Error: If the input type is not supported.

    Returns:
        The parsed document structure.
    """
    if isinstance(f, _IOBase):
        content = f.read()
        
        if isinstance(content,bytes):
            content = content.decode("utf-8")
            
        return parse_markdown(content)
    elif isinstance(f, str) or isinstance(f, Path):
        with open(f) as _file_:
            content = _file_.read()
            return parse_markdown(content)
    else:
        raise Error(f"Type {type(f)} not supported")


def parse_markdown(text: str):
    """Parses a string of Markdown text.

    This function processes a Markdown string and attempts to build a
    hierarchical structure of DocumentElement objects.

    Args:
        text: The Markdown text to parse.
    """

    with MarkdownRenderer() as renderer:
        doc = Document(text)

        current_depth = 0
        node_stack = [models.DocumentElement(children=[], parts=[])]
        current_node = node_stack[-1]
        start_point = 0

        if isinstance(doc.children[start_point], Heading):
            c: Heading = doc.children[start_point]
            depth_stack = [c.level]
            start_point += 1

            text_part = models.DocPart(content = renderer.render(c))
            current_node.parts.append(text_part)

        for c in doc.children[start_point:]:

            if isinstance(c, Heading):
                # TODO: Gestione gerarchie dei nodi durante la lettura
                new_node = models.DocumentElement(children=[], parts=[])

                if c.level > current_depth:
                    current_node.children.append(new_node)
                    node_stack.append(new_node)
                    current_node = new_node
                    current_depth = c.level
                elif c.level == current_depth:
                    node_stack[-2].children.append(new_node)
                    node_stack[-1] = new_node
                    current_node = new_node
                elif c.level < current_depth:
                    node_stack.pop()
                    node_stack[-2].children.append(new_node)
                    node_stack[-1] = new_node
                    current_node = new_node
                    current_depth = c.level

            text_part = models.DocPart(content = renderer.render(c))
            current_node.parts.append(text_part)

    mk_document = models. Document(
        id="test_01", name="Prova", body=node_stack[0])
    
    return mk_document

    
    
    
    