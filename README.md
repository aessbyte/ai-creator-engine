# ai-creator-engine

Automation pipeline for generating short-form video assets.

## TTS architecture

The project now uses a provider layer instead of coupling the video pipeline to one voice model.

Current provider:

- **OmniVoice** via `minipasila/omnivoice-api-server`
- endpoint: `POST /tts_to_audio/`
- output: WAV
- default language: Portuguese (`pt`)

This repository does **not** run the heavy OmniVoice model inside GitHub Actions. The workflow calls an external OmniVoice server (local machine exposed securely, cloud GPU, Colab tunnel, etc.). This keeps GitHub Actions lightweight and lets the TTS backend be replaced later.

### Local/API usage

```bash
export OMNIVOICE_BASE_URL="http://127.0.0.1:8020"
export OMNIVOICE_SPEAKER="narrador.wav"

python -m tts.cli \
  --text "Teste de narracao." \
  --output out/narration.wav
```

Or synthesize a text file:

```bash
python -m tts.cli \
  --text-file script.txt \
  --voice narrador.wav \
  --language pt \
  --output out/narration.wav
```

### Trigger from the phone with GitHub Actions

Workflow: **Generate Narration** (`.github/workflows/tts.yml`).

Before running it, create the repository secret:

- `OMNIVOICE_BASE_URL`: public/reachable URL of the OmniVoice API server.

Then open **Actions → Generate Narration → Run workflow**, paste the text, select the speaker and run. The generated `narration.wav` is uploaded as a GitHub artifact.

### Voice reference recommendations

The OmniVoice API server documentation recommends clean reference clips around **3–10 seconds**, mono **24 kHz / 16-bit WAV**, without music/background noise. A `.txt` transcript with the same base filename can be supplied server-side to avoid ASR and improve cloning consistency.

## Next providers

The interface lives in `tts/base.py`. Additional engines (Pocket-TTS, VoxCPM, LocalAI, cloud APIs) can be added as providers without changing the rest of the rendering pipeline.
