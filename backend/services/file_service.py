from dataclasses import dataclass
from uuid import uuid4

SUPPORTED_IMPORTS = {"txt", "docx", "pdf", "mp3", "wav", "mp4", "mov", "png", "jpg", "webm"}
SUPPORTED_EXPORTS = {"mp3", "wav", "srt", "txt", "json", "preset"}


@dataclass
class ImportedFile:
    import_id: str
    filename: str
    extension: str
    status: str = "accepted"


def import_file(filename: str) -> ImportedFile:
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in SUPPORTED_IMPORTS:
        raise ValueError(f"Unsupported import format: {extension}")
    return ImportedFile(import_id=str(uuid4()), filename=filename, extension=extension)


def export_file(resource_id: str, output_format: str) -> dict:
    output_format = output_format.lower()
    if output_format not in SUPPORTED_EXPORTS:
        raise ValueError(f"Unsupported export format: {output_format}")
    return {
        "export_id": str(uuid4()),
        "resource_id": resource_id,
        "output_format": output_format,
        "status": "queued",
    }
