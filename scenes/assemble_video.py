"""Assemble the six rendered Manim scene MP4s into one combined video.

Usage:
    python scenes/assemble_video.py --quality 480p15 --output output/Preview_Video.mp4
    python scenes/assemble_video.py --quality 1080p30 --output output/Final_Video.mp4
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

SRT_TS_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")

SCENE_SPECS: list[tuple[str, str]] = [
    ("scene_01_hook", "Scene01Hook"),
    ("scene_02_concept", "Scene02Concept"),
    ("scene_03_intuition", "Scene03Intuition"),
    ("scene_04_worked_example", "Scene04WorkedExample"),
    ("scene_05_interpretation", "Scene05Interpretation"),
    ("scene_06_summary_credits", "Scene06SummaryCredits"),
]


def probe_duration(video_path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        text=True,
    ).strip()
    return float(out)


def has_audio_stream(video_path: Path) -> bool:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a",
            "-show_entries",
            "stream=codec_type",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        text=True,
    ).strip()
    return bool(out)


def _ts_to_ms(match: re.Match[str]) -> int:
    h, m, s, ms = (int(g) for g in match.groups())
    return ((h * 60 + m) * 60 + s) * 1000 + ms


def _ms_to_ts(total_ms: int) -> str:
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_m = total_s // 60
    m = total_m % 60
    h = total_m // 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def merge_srts(srt_entries: list[tuple[Path, float]], output_srt: Path) -> None:
    merged_blocks: list[str] = []
    cue_idx = 1
    offset_ms = 0

    for srt_path, scene_dur_s in srt_entries:
        if srt_path.exists():
            raw = srt_path.read_text(encoding="utf-8").strip()
            for block in re.split(r"\n\s*\n", raw):
                lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
                if len(lines) < 3:
                    continue
                shifted = SRT_TS_RE.sub(lambda m: _ms_to_ts(_ts_to_ms(m) + offset_ms), lines[1])
                merged_blocks.append(f"{cue_idx}\n{shifted}\n" + "\n".join(lines[2:]))
                cue_idx += 1
        offset_ms += int(round(scene_dur_s * 1000))

    if merged_blocks:
        output_srt.write_text("\n\n".join(merged_blocks) + "\n", encoding="utf-8")


def assemble(quality: str, output_mp4: Path) -> None:
    root = Path(__file__).resolve().parent.parent
    video_paths: list[Path] = []
    srt_entries: list[tuple[Path, float]] = []
    total_dur = 0.0

    for mod_name, cls_name in SCENE_SPECS:
        vid = root / "media" / "videos" / mod_name / quality / f"{cls_name}.mp4"
        srt = root / "media" / "subtitles" / f"{cls_name}.srt"
        if not vid.exists():
            raise FileNotFoundError(f"Missing rendered scene video: {vid}")
        dur = probe_duration(vid)
        total_dur += dur
        video_paths.append(vid)
        srt_entries.append((srt, dur))
        print(f"  + {cls_name:24s} {dur:6.2f}s")

    print(f"  Total Duration: {total_dur:6.2f}s ({total_dur / 60:.2f} min)")

    all_have_audio = all(has_audio_stream(vp) for vp in video_paths)
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for vp in video_paths:
        cmd.extend(["-i", str(vp)])

    n = len(video_paths)
    if all_have_audio:
        stream_inputs = "".join(f"[{i}:v:0][{i}:a:0]" for i in range(n))
        cmd.extend(
            [
                "-filter_complex",
                f"{stream_inputs}concat=n={n}:v=1:a=1[outv][outa]",
                "-map",
                "[outv]",
                "-map",
                "[outa]",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                str(output_mp4),
            ]
        )
    else:
        stream_inputs = "".join(f"[{i}:v:0]" for i in range(n))
        cmd.extend(
            [
                "-filter_complex",
                f"{stream_inputs}concat=n={n}:v=1:a=0[outv]",
                "-map",
                "[outv]",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                str(output_mp4),
            ]
        )

    subprocess.run(cmd, check=True)
    output_srt = output_mp4.with_suffix(".srt")
    merge_srts(srt_entries, output_srt)
    print(f"\nAssembled video ready: {output_mp4}")
    if output_srt.exists():
        print(f"Merged subtitles ready: {output_srt}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble 6 rendered Manim scenes into one MP4.")
    parser.add_argument("--quality", default="480p15", help="Manim quality folder (e.g. 480p15, 720p30, 1080p30)")
    parser.add_argument("--output", default="output/Preview_Video.mp4", help="Output MP4 path")
    args = parser.parse_args()
    assemble(args.quality, Path(args.output))


if __name__ == "__main__":
    main()
