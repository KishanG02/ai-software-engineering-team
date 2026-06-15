from pathlib import Path


def save_output(
    filename: str,
    content: str
) -> str:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename

    filepath.write_text(
        content,
        encoding="utf-8"
    )

    return str(filepath)