"""Scene 1: Hook and Context — Steepness on a surface depends on direction."""

from __future__ import annotations

import numpy as np
from manim import *

from scenes.common import (
    AMBER,
    AXIS,
    CONCEPT_TAG,
    CORAL,
    COURSE_TAG,
    CYAN,
    GRID,
    MUTED,
    PROJECT_SUBTITLE,
    PROJECT_TITLE,
    TEAL,
    TEXT_WHITE,
    BaseMathScene,
    make_card,
    make_scene_header,
    pill_label,
)


class Scene01Hook(BaseMathScene):
    def construct(self) -> None:
        self.setup_scene()

        # Opening title card
        course = Text(COURSE_TAG, font_size=16, weight=MEDIUM, color=TEAL, font=self.sans_font)
        title = Text(PROJECT_TITLE, font_size=44, weight=BOLD, color=TEXT_WHITE, font=self.sans_font)
        subtitle = Text(PROJECT_SUBTITLE, font_size=22, color=MUTED, font=self.sans_font)
        bar = Line(LEFT * 2.4, RIGHT * 2.4, color=TEAL, stroke_width=2.5)
        tag = Text(CONCEPT_TAG, font_size=17, color=CYAN, font=self.sans_font)
        title_block = VGroup(course, title, subtitle, bar, tag).arrange(DOWN, buff=0.26)

        self.play(FadeIn(title_block, shift=UP * 0.2), run_time=1.4)
        self.wait(2.2)
        self.play(FadeOut(title_block), run_time=0.8)

        # Scene header
        header = make_scene_header("Scene 1 • Hook & Context", "Slope Depends on Direction", self.sans_font)
        self.play(FadeIn(header), run_time=0.6)

        # Left: Contour map on coordinate plane
        plane = NumberPlane(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            x_length=5.6,
            y_length=5.6,
            axis_config={"stroke_color": AXIS, "stroke_width": 1.8},
            background_line_style={"stroke_color": GRID, "stroke_width": 1.1, "stroke_opacity": 0.55},
        ).move_to(LEFT * 2.6 + DOWN * 0.15)

        contours = VGroup(
            *[
                Circle(
                    radius=r * (5.6 / 6.0),
                    color=GRID,
                    stroke_width=1.6,
                    stroke_opacity=0.85,
                ).move_to(plane.c2p(0, 0))
                for r in (0.8, 1.4, 2.0, 2.6)
            ]
        )
        p0_coord = np.array([1.0, 1.0, 0.0])
        p0_pt = plane.c2p(1.0, 1.0)
        p0_dot = Dot(p0_pt, color=CORAL, radius=0.09)
        p0_lbl = pill_label(MathTex("P_0", color=CORAL, font_size=26).next_to(p0_dot, DL, buff=0.1))

        # Right: Contextual question card
        q_title = Text("Key Question", font_size=20, weight=BOLD, color=TEAL, font=self.sans_font)
        q_body = Text(
            "From one point P₀ on a surface,\ndifferent directions give different slopes.",
            font_size=17,
            color=TEXT_WHITE,
            font=self.sans_font,
            line_spacing=1.25,
        )
        q_goal = Text(
            "Which direction climbs fastest?",
            font_size=18,
            weight=BOLD,
            color=AMBER,
            font=self.sans_font,
        )
        q_card = make_card(VGroup(q_title, q_body, q_goal).arrange(DOWN, aligned_edge=LEFT, buff=0.22))
        q_card.move_to(RIGHT * 3.2 + UP * 0.7)

        self.play_beat(
            "s1.1",
            [
                ([Create(plane), Create(contours)], 1.6),
                ([FadeIn(p0_dot), FadeIn(p0_lbl), FadeIn(q_card)], 1.2),
            ],
            post_wait=1.0,
        )

        # Three sample directions from P0
        # 1. Steepest (radial outward)
        arr_steep = Arrow(p0_pt, plane.c2p(2.0, 2.0), buff=0, color=TEAL, stroke_width=4.5)
        lbl_steep = pill_label(Text("Steepest", font_size=15, color=TEAL, font=self.sans_font).next_to(arr_steep.get_end(), UR, buff=0.08))

        # 2. Diagonal (moderate)
        arr_mod = Arrow(p0_pt, plane.c2p(2.2, 0.7), buff=0, color=CYAN, stroke_width=4.0)
        lbl_mod = pill_label(Text("Moderate", font_size=15, color=CYAN, font=self.sans_font).next_to(arr_mod.get_end(), RIGHT, buff=0.08))

        # 3. Tangent to contour (flat)
        arr_flat = Arrow(p0_pt, plane.c2p(0.1, 1.9), buff=0, color=AMBER, stroke_width=4.0)
        lbl_flat = pill_label(Text("Flat (Δz = 0)", font_size=15, color=AMBER, font=self.sans_font).next_to(arr_flat.get_end(), UL, buff=0.08))

        legend = make_card(
            VGroup(
                Text("• Radial outward: maximum climb", font_size=15, color=TEAL, font=self.sans_font),
                Text("• Diagonal: partial climb", font_size=15, color=CYAN, font=self.sans_font),
                Text("• Along contour: zero change", font_size=15, color=AMBER, font=self.sans_font),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        ).move_to(RIGHT * 3.2 + DOWN * 1.15)

        self.play_beat(
            "s1.2",
            [
                ([GrowArrow(arr_steep), FadeIn(lbl_steep)], 1.1),
                ([GrowArrow(arr_mod), FadeIn(lbl_mod)], 1.1),
                ([GrowArrow(arr_flat), FadeIn(lbl_flat), FadeIn(legend)], 1.3),
            ],
            post_wait=1.2,
        )

        self.play(FadeOut(VGroup(header, plane, contours, p0_dot, p0_lbl, arr_steep, lbl_steep, arr_mod, lbl_mod, arr_flat, lbl_flat, q_card, legend)), run_time=0.7)
