"""Generate offline narration WAV clips for all beats using macOS `say`."""

from __future__ import annotations

import subprocess
import wave
from pathlib import Path

from scenes.common import BEATS


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wf:
        return wf.getnframes() / float(wf.getframerate())


def main() -> None:
    out_dir = Path("media/voiceovers")
    out_dir.mkdir(parents=True, exist_ok=True)
    total_audio = 0.0
    for beat_id, text in BEATS.items():
        wav_path = out_dir / f"{beat_id}.wav"
        subprocess.run(
            ["/usr/bin/say", "-r", "165", "--data-format=LEI16@22050", "-o", str(wav_path), text],
            check=True,
        )
        dur = wav_duration(wav_path)
        total_audio += dur
        print(f"  {beat_id:6s} -> {dur:5.2f}s ({wav_path})")
    print(f"Total raw speech audio: {total_audio:.2f}s ({total_audio / 60:.2f} min)")


if __name__ == "__main__":
    main()
