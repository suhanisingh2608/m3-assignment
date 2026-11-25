"""Shared visual design system, narration beats, and paced scene helpers
for the M3 Gradient and Directional Derivatives animation project.
"""

from __future__ import annotations

import os
import wave
from pathlib import Path
from typing import Iterable, Sequence

import manimpango
from manim import *

# ---------------------------------------------------------------------------
# 1. Project Metadata
# ---------------------------------------------------------------------------
PROJECT_TITLE = "Gradient & Directional Derivatives"
PROJECT_SUBTITLE = "Measuring Steepness in Any Direction"
CONCEPT_TAG = "Worked Example: f(x, y) = x^2 + y^2"
COURSE_TAG = "M3 — Linear Algebra and Calculus"

# ---------------------------------------------------------------------------
# 2. Hybrid Dark Visual Design System
# ---------------------------------------------------------------------------
BG = "#0D1117"            # Deep charcoal/navy canvas
GRID = "#526477"          # Subdued cool blue/grey reference grid
AXIS = "#9AAFC2"          # Reference axes
CYAN = "#53D8FB"          # Primary highlight (x-direction / unit vector u)
AMBER = "#FFB84D"         # Secondary highlight (y-direction / angle / tangent)
CORAL = "#FF718D"         # Tracked point P0 / steepest descent
TEAL = "#55D6BE"          # Gradient vector / key result accent
TEAL_AXIS = "#8AEAD8"     # Accent axes / highlights
TEXT_WHITE = "#F4F7FB"    # Crisp primary text
MUTED = "#A8B6C6"         # Secondary captions & subtitles
PANEL_BG = "#111B27"      # Dark translucent card background
PANEL_STROKE = "#34495E"  # Subtle card border

# ---------------------------------------------------------------------------
# 3. Modular Narration Beats (~535 words across 18 beats, targeting 5-7 min)
# ---------------------------------------------------------------------------
# Organized into short semantic beats so voiceover audio (Gemini TTS or
# student recording) can be attached cleanly without changing scene structure.
BEATS: dict[str, str] = {
    "s1.1": (
        "Imagine standing on the side of a smooth hill. In single-variable calculus, "
        "a curve has only one slope at each point. On a two-variable surface, however, "
        "your steepness depends entirely on the direction you choose to walk."
    ),
    "s1.2": (
        "Step one way and you climb rapidly; step along a contour and your height "
        "barely changes. How do we measure the rate of change in any direction, and "
        "find the single direction of steepest ascent?"
    ),
    "s2.1": (
        "We begin with partial derivatives. Holding y fixed, the partial derivative "
        "with respect to x measures the slope purely in the x-direction. Holding x "
        "fixed, the partial derivative with respect to y measures the slope in the y-direction."
    ),
    "s2.2": (
        "Packing these two coordinate slopes together into a vector gives the gradient "
        "of f, written as del f of x, y."
    ),
    "s2.3": (
        "To measure slope in any arbitrary direction u, we require u to be a unit "
        "vector of length one, so we measure change per unit step. The directional "
        "derivative is then the dot product: del f dot u."
    ),
    "s3.1": (
        "Why does the gradient always point in the direction of steepest increase? "
        "Rewrite the dot product using theta, the angle between the gradient vector "
        "and our unit direction vector u."
    ),
    "s3.2": (
        "Because u has length one, the directional derivative simplifies to the "
        "magnitude of the gradient times cosine of theta."
    ),
    "s3.3": (
        "As u rotates around the unit circle, cosine theta reaches its maximum value "
        "of one only when theta equals zero degrees—meaning u points in the exact "
        "same direction as the gradient. The maximum slope is the norm of del f."
    ),
    "s3.4": (
        "When theta is ninety degrees, cosine theta is zero, so walking tangent to "
        "a level curve produces zero instantaneous height change. At one hundred "
        "eighty degrees, you descend as steeply as possible."
    ),
    "s4.1": (
        "Let us work step by step through a concrete example: the paraboloid "
        "f of x, y equals x squared plus y squared, evaluated at the point one, two."
    ),
    "s4.2": (
        "First, compute both partial derivatives: partial f partial x equals two x, "
        "and partial f partial y equals two y. Evaluating at one, two gives the "
        "gradient vector two, four."
    ),
    "s4.3": (
        "Next, choose the direction u equals three-fifths, four-fifths. Its length "
        "is the square root of nine twenty-fifths plus sixteen twenty-fifths, which "
        "equals one—confirming u is a unit vector."
    ),
    "s4.4": (
        "Taking the dot product gives two times three-fifths plus four times "
        "four-fifths, which equals six-fifths plus sixteen-fifths, or twenty-two "
        "fifths—a slope of four point four. Meanwhile, the maximum possible slope "
        "at this point is two root five, approximately four point four seven."
    ),
    "s5.1": (
        "Geometrically, the level curves of x squared plus y squared are concentric "
        "circles centered at the origin."
    ),
    "s5.2": (
        "At the point one, two, the gradient vector two, four points radially outward—"
        "perpendicular to the circle of radius root five. Walking tangent to the "
        "circle gives zero change, while walking radially outward climbs fastest."
    ),
    "s5.3": (
        "Because our chosen direction three-fifths, four-fifths is separated from "
        "the gradient by approximately ten point three degrees, its slope of four "
        "point four captures almost all of the maximum steepness of four point four seven."
    ),
    "s6.1": (
        "To recap: the gradient del f combines the partial derivatives and always "
        "points in the direction of steepest increase, perpendicular to level curves."
    ),
    "s6.2": (
        "For any unit direction u, the directional derivative is del f dot u, "
        "bounded between negative and positive norm of del f. Thank you for watching."
    ),
}


def select_sans_font() -> str:
    """Pick a clean modern sans-serif installed on the current OS."""
    available = set(manimpango.list_fonts())
    for candidate in ("Avenir Next", "Helvetica Neue", "Inter", "DejaVu Sans", "Arial"):
        if candidate in available:
            return candidate
    return "Sans"


def pill_label(mobj: Mobject, opacity: float = 0.88, buff: float = 0.06) -> Mobject:
    """Add a canvas-matched halo behind a label so grid lines never cut through math text."""
    mobj.add_background_rectangle(color=BG, opacity=opacity, buff=buff)
    return mobj


def make_card(
    content: Mobject,
    pad_x: float = 0.42,
    pad_y: float = 0.28,
    stroke_color: str = PANEL_STROKE,
    fill_opacity: float = 0.96,
) -> VGroup:
    """Wrap any Mobject or VGroup inside a clean bordered dark card."""
    box = RoundedRectangle(
        width=content.width + pad_x,
        height=content.height + pad_y,
        corner_radius=0.14,
        stroke_color=stroke_color,
        stroke_width=1.25,
        fill_color=PANEL_BG,
        fill_opacity=fill_opacity,
    )
    content.move_to(box.get_center())
    return VGroup(box, content)


def make_scene_header(scene_tag: str, scene_title: str, font_name: str) -> VGroup:
    """Consistent upper-left header shared across all scenes."""
    tag = Text(scene_tag.upper(), font_size=13, weight=BOLD, color=TEAL, font=font_name)
    title = Text(scene_title, font_size=24, weight=BOLD, color=TEXT_WHITE, font=font_name)
    header = VGroup(tag, title).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    header.to_corner(UL, buff=0.34)
    return header


def make_bottom_caption(text: str, font_name: str, color: str = MUTED) -> Text:
    """Consistent bottom guide caption bar."""
    return Text(text, font_size=16, weight=MEDIUM, color=color, font=font_name).to_edge(
        DOWN, buff=0.28
    )


def estimate_beat_duration(beat_id: str, wpm: float = 120.0) -> float:
    """Estimate natural speaking + visual observation duration for a beat."""
    words = len(BEATS[beat_id].split())
    return max(5.0, (words / (wpm / 60.0)) + 2.2)


def _format_srt_ts(seconds: float) -> str:
    total_ms = max(0, int(round(seconds * 1000)))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_m = total_s // 60
    m = total_m % 60
    h = total_m // 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _wav_duration(path: Path) -> float:
    try:
        with wave.open(str(path), "rb") as wf:
            return wf.getnframes() / float(wf.getframerate())
    except Exception:
        return 0.0


class BaseMathScene(Scene):
    """Base Manim scene with consistent dark styling, subtitle support, and paced beats.

    No Gemini API key is required to render. Uses offline WAV clips in
    `media/voiceovers/` when present, and exports timed `.srt` cues to
    `media/subtitles/`.
    """

    sans_font: str
    _caption_mobj: Mobject | None = None
    _srt_cues: list[tuple[float, float, str]]

    def setup_scene(self) -> None:
        self.sans_font = select_sans_font()
        self.camera.background_color = BG
        self._caption_mobj = None
        self._srt_cues = []

    def tear_down(self) -> None:
        if getattr(self, "_srt_cues", None):
            sub_dir = Path(__file__).resolve().parent.parent / "media" / "subtitles"
            sub_dir.mkdir(parents=True, exist_ok=True)
            srt_path = sub_dir / f"{self.__class__.__name__}.srt"
            blocks = [
                f"{idx}\n{_format_srt_ts(start)} --> {_format_srt_ts(end)}\n{text}"
                for idx, (start, end, text) in enumerate(self._srt_cues, start=1)
            ]
            srt_path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
        super().tear_down()

    def _build_subtitle(self, text: str) -> VGroup:
        """Render a clean two-line subtitle pill at the bottom of the frame."""
        words = text.split()
        lines: list[str] = []
        current: list[str] = []
        for w in words:
            if len(" ".join(current + [w])) > 84 and current:
                lines.append(" ".join(current))
                current = [w]
            else:
                current.append(w)
        if current:
            lines.append(" ".join(current))
        wrapped = "\n".join(lines[:3])
        txt = Text(
            wrapped,
            font_size=16,
            color=TEXT_WHITE,
            font=self.sans_font,
            line_spacing=1.15,
        )
        pill = RoundedRectangle(
            width=min(12.8, txt.width + 0.44),
            height=txt.height + 0.22,
            corner_radius=0.10,
            stroke_color=PANEL_STROKE,
            stroke_width=0.9,
            fill_color=PANEL_BG,
            fill_opacity=0.90,
        )
        txt.move_to(pill.get_center())
        grp = VGroup(pill, txt).to_edge(DOWN, buff=0.22)
        return grp

    def play_beat(
        self,
        beat_id: str,
        steps: Sequence[tuple[Iterable[Animation] | None, float]],
        post_wait: float = 0.6,
        show_subtitle: bool = True,
    ) -> float:
        """Play animation steps alongside a paced narration beat."""
        spoken_text = BEATS[beat_id]
        wav_path = Path(__file__).resolve().parent.parent / "media" / "voiceovers" / f"{beat_id}.wav"
        audio_dur = _wav_duration(wav_path) if wav_path.exists() else 0.0
        target_duration = max(estimate_beat_duration(beat_id), audio_dur + 0.8 if audio_dur > 0.1 else 0.0)

        start_t = float(self.renderer.time)
        if audio_dur > 0.1:
            self.add_sound(str(wav_path))

        if show_subtitle:
            new_sub = self._build_subtitle(spoken_text)
            if self._caption_mobj is not None:
                self.remove(self._caption_mobj)
            self._caption_mobj = new_sub
            self.add(self._caption_mobj)

        total_desired = sum(dur for _, dur in steps)
        budget = max(0.8, target_duration * 0.90)
        scale = min(1.0, budget / total_desired) if total_desired > 0 else 1.0

        elapsed = 0.0
        for anims, desired in steps:
            dur = max(0.2, desired * scale)
            if anims:
                self.play(*anims, run_time=dur, rate_func=smooth)
            else:
                self.wait(dur)
            elapsed += dur

        remaining = max(0.0, target_duration - elapsed)
        if remaining > 0.05:
            self.wait(remaining)

        end_t = float(self.renderer.time)
        self._srt_cues.append((start_t, end_t, spoken_text))

        if post_wait > 0.0:
            self.wait(post_wait)

        return target_duration + post_wait
