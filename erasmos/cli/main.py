import click
from pathlib import Path
from ..core import tts as ttslib
from ..core.models import Document
from . import utilities as cli_utils
from ..core.config import ensure_dirs
from ..core import utilities as core_utils
from ..core import meta_document as metadoclib
from ..core.parser import parse_markdown_file

@click.group()
@click.version_option(version="0.0.1")
def cli():
    """Erasmos - Markdown to audio converter"""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path),
              help='Output mp3 file (default: <input_filename>.mp3)')
@click.option('--meta', '-m',
              type=click.Choice(metadoclib.MetaDocumentGenerator.options()),
              default=metadoclib.MetaDocumentGenerator.UNMARKDOWN,
              help='Meta document parser that prepares Markdown for TTS (default: unmarkdown)')
@click.option('--tts', '-t',
              type=click.Choice(ttslib.TTSEngines.options()),
              default=ttslib.TTSEngines.GOOGLE_TTS,
              help='TTS engine to use (default: google_tts)')
@click.option('--lang', '-l', default='en',
              help='Language for text-to-speech')
def convert(input_file, output, meta, tts, lang):
    """Converts a Markdown file to audio"""
    # Conversion implementation

    metadoc_method = getattr(metadoclib, meta)
    tts_method = getattr(ttslib, tts)

    core_utils.validate_file_extension(input_file,'md')

    output = cli_utils.get_output_filename(input_file, output)
    core_utils.validate_file_extension(output,'mp3')
    
    doc = parse_markdown_file(input_file)
    doc = metadoc_method(doc)
    audio_path = tts_method(doc, lang)
    audio_path = Path(audio_path)
    
    audio_path.rename(output)
    
    cli_utils.clean_temp_files()


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path))
@click.option('--meta', '-m',
              type=click.Choice(metadoclib.MetaDocumentGenerator.options()),
              default=metadoclib.MetaDocumentGenerator.UNMARKDOWN,
              help='Meta document parser that prepares Markdown for TTS (default: unmarkdown)')
def preview(input_file, output, meta):
    """Shows a preview of the processed document without generating audio"""

    metadoc_method = getattr(metadoclib, meta)
    core_utils.validate_file_extension(input_file, 'md')

    output = cli_utils.get_output_filename(input_file, output, 'txt')
    core_utils.validate_file_extension(output, 'txt')

    doc = parse_markdown_file(input_file)
    doc: Document = metadoc_method(doc)
    
    if doc.parsed_body:
        stack = [doc.parsed_body]
        merged_parts = []
        
        while stack:
            el = stack.pop(0)
            content = ''.join([str(p.content) for p in el.parts])
            merged_parts.append(content)
            
            stack = el.children + stack
        
        doc_content = ''.join(merged_parts)
        
        with open(output, "w") as f:
            f.write(doc_content)
        
    else:
        raise Exception("Metadocument parsing failed!")
    

if __name__ == '__main__':
    ensure_dirs()
    cli()
