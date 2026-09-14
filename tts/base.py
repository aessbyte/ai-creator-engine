from abc import ABC, abstractmethod
from pathlib import Path


class TTSProvider(ABC):
    """Common interface for text-to-speech providers."""

    @abstractmethod
    def synthesize(
        self,
        text: str,
        output_path: str | Path,
        *,
        voice: str | None = None,
        language: str = "pt",
    ) -> Path:
        """Generate speech and return the output WAV path."""
        raise NotImplementedError
