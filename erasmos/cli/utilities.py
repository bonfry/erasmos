import click
import shutil
from pathlib import Path

def get_output_filename(input_file: Path, output_file: Path, extension='mp3') -> Path:
    """Generate the output filename"""
    if output_file:
        return output_file

    return input_file.with_suffix(f'.{extension}')


def clean_temp_files(directory: str = "tmp"):
    """Clean up temporary files"""
    temp_dir = Path(directory)
    if temp_dir.exists():
        for file in temp_dir.glob("*.mp3"):
            file.unlink()
        click.echo(
            f"Cleaned {len(list(temp_dir.glob('*')))} files from {directory}/")

