import argparse
from pathlib import Path

from .omnivoice import OmniVoiceProvider


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate narration with ai-creator-engine")
    parser.add_argument("--text", help="Text to synthesize")
    parser.add_argument("--text-file", help="UTF-8 text file to synthesize")
    parser.add_argument("--output", default="out/narration.wav")
    parser.add_argument("--voice", help="Speaker WAV name known by OmniVoice server")
    parser.add_argument("--language", default="pt")
    parser.add_argument("--base-url", help="OmniVoice API URL; otherwise OMNIVOICE_BASE_URL")
    args = parser.parse_args()

    if bool(args.text) == bool(args.text_file):
        parser.error("provide exactly one of --text or --text-file")

    text = args.text if args.text else Path(args.text_file).read_text(encoding="utf-8")
    provider = OmniVoiceProvider(base_url=args.base_url)
    path = provider.synthesize(text, args.output, voice=args.voice, language=args.language)
    print(path)


if __name__ == "__main__":
    main()
