"""Scene 6: Summary, References, and AI Tools Disclosure."""

from __future__ import annotations

from manim import *

from scenes.common import (
    AMBER,
    CYAN,
    MUTED,
    TEAL,
    TEXT_WHITE,
    BaseMathScene,
    make_card,
    make_scene_header,
)


class Scene06SummaryCredits(BaseMathScene):
    def construct(self) -> None:
        self.setup_scene()
        header = make_scene_header(
            "Scene 6 • Summary & Credits",
            "Key Takeaways",
            self.sans_font,
        )
        self.play(FadeIn(header), run_time=0.6)

        t1 = make_card(
            VGroup(
                Text("1. Gradient Vector", font_size=18, weight=BOLD, color=TEAL, font=self.sans_font),
                MathTex(
                    r"\nabla f = \left\langle \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right\rangle",
                    color=TEXT_WHITE,
                    font_size=25,
                ),
                Text("Points in steepest ascent, ⊥ level curves", font_size=15, color=MUTED, font=self.sans_font),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            stroke_color=TEAL,
        )

        t2 = make_card(
            VGroup(
                Text("2. Directional Derivative", font_size=18, weight=BOLD, color=CYAN, font=self.sans_font),
                MathTex(r"D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u} \quad (\|\mathbf{u}\| = 1)", color=TEXT_WHITE, font_size=25),
                Text("Requires a unit direction vector", font_size=15, color=MUTED, font=self.sans_font),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            stroke_color=CYAN,
        )

        t3 = make_card(
            VGroup(
                Text("3. Rate-of-Change Bounds", font_size=18, weight=BOLD, color=AMBER, font=self.sans_font),
                MathTex(r"-\|\nabla f\| \le D_{\mathbf{u}} f \le \|\nabla f\|", color=TEXT_WHITE, font_size=25),
                Text("Max when θ = 0°, zero when θ = 90°", font_size=15, color=MUTED, font=self.sans_font),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            stroke_color=AMBER,
        )

        takeaways = VGroup(t1, t2, t3).arrange(DOWN, buff=0.28).move_to(DOWN * 0.15)

        self.play_beat(
            "s6.1",
            [
                ([FadeIn(t1, shift=UP * 0.15)], 1.2),
                ([FadeIn(t2, shift=UP * 0.15)], 1.2),
            ],
            post_wait=0.8,
        )

        self.play_beat(
            "s6.2",
            [
                ([FadeIn(t3, shift=UP * 0.15)], 1.3),
            ],
            post_wait=1.2,
        )

        self.play(FadeOut(takeaways), run_time=0.6)

        # Credits & AI Disclosure card
        credits_title = Text("References, Tools & AI Disclosure", font_size=24, weight=BOLD, color=TEAL, font=self.sans_font)
        refs = Text(
            "References: Stewart, Calculus: Early Transcendentals (Ch. 14) • M3 Lecture Notes",
            font_size=16,
            color=TEXT_WHITE,
            font=self.sans_font,
        )
        tools = Text(
            "Tools: Manim Community v0.22.1 • Python 3.12.3 • BasicTeX (pdflatex, dvisvgm 3.6) • FFmpeg 9.1",
            font_size=15,
            color=MUTED,
            font=self.sans_font,
        )
        kit_note = Text(
            "Starter framework structure adapted from sohamdhande/m3-manim-animation-kit",
            font_size=15,
            color=MUTED,
            font=self.sans_font,
        )
        ai_note = Text(
            "AI Disclosure: Google Antigravity assisted with project planning and Python/Manim code generation.\n"
            "Final mathematical review and verification by the student is pending prior to submission.",
            font_size=15,
            color=AMBER,
            font=self.sans_font,
            line_spacing=1.25,
        )
        credits_card = make_card(
            VGroup(credits_title, refs, tools, kit_note, ai_note).arrange(DOWN, aligned_edge=LEFT, buff=0.22),
            pad_x=0.6,
            pad_y=0.45,
        ).move_to(ORIGIN)

        if self._caption_mobj is not None:
            self.remove(self._caption_mobj)

        self.play(FadeIn(credits_card), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(VGroup(header, credits_card)), run_time=0.8)
