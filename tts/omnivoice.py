import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .base import TTSProvider


class OmniVoiceProvider(TTSProvider):
    """HTTP client for minipasila/omnivoice-api-server.

    The server exposes an XTTS-compatible FastAPI endpoint at /tts_to_audio/.
    Keep the model outside this repository; this client only sends generation jobs.
    """

    def __init__(self, base_url: str | None = None, timeout: int = 300):
        self.base_url = (base_url or os.getenv("OMNIVOICE_BASE_URL", "http://127.0.0.1:8020")).rstrip("/")
        self.timeout = timeout

    def synthesize(
        self,
        text: str,
        output_path: str | Path,
        *,
        voice: str | None = None,
        language: str = "pt",
    ) -> Path:
        if not text.strip():
            raise ValueError("text cannot be empty")
        if not voice:
            voice = os.getenv("OMNIVOICE_SPEAKER")
        if not voice:
            raise ValueError("voice is required (e.g. narrador.wav or OMNIVOICE_SPEAKER)")

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        payload = json.dumps({
            "text": text,
            "speaker_wav": voice,
            "language": language,
        }).encode("utf-8")

        request = Request(
            f"{self.base_url}/tts_to_audio/",
            data=payload,
            headers={"Content-Type": "application/json", "Accept": "audio/wav"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                audio = response.read()
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OmniVoice HTTP {exc.code}: {body}") from exc
        except URLError as exc:
            raise RuntimeError(f"Cannot reach OmniVoice at {self.base_url}: {exc.reason}") from exc

        if not audio:
            raise RuntimeError("OmniVoice returned an empty response")

        output.write_bytes(audio)
        return output

    def list_speakers(self) -> bytes:
        request = Request(f"{self.base_url}/speakers", method="GET")
        with urlopen(request, timeout=self.timeout) as response:
            return response.read()
