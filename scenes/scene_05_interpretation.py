"""Scene 5: Geometric Interpretation — Level curves, orthogonality, and 10.3 deg alignment."""

from __future__ import annotations

import numpy as np
from manim import *

from scenes.common import (
    AMBER,
    AXIS,
    CORAL,
    CYAN,
    GRID,
    TEAL,
    TEXT_WHITE,
    BaseMathScene,
    make_card,
    make_scene_header,
    pill_label,
)


class Scene05Interpretation(BaseMathScene):
    def construct(self) -> None:
        self.setup_scene()
        header = make_scene_header(
            "Scene 5 • Geometric Interpretation",
            "Level Curves, Normal Gradient & Direction u",
            self.sans_font,
        )
        self.play(FadeIn(header), run_time=0.6)

        plane = NumberPlane(
            x_range=(-3.5, 4.0, 1),
            y_range=(-3.5, 4.5, 1),
            x_length=5.6,
            y_length=5.6,
            axis_config={"stroke_color": AXIS, "stroke_width": 1.8},
            background_line_style={"stroke_color": GRID, "stroke_width": 1.0, "stroke_opacity": 0.45},
        ).move_to(LEFT * 3.0 + DOWN * 0.1)

        origin = plane.c2p(0, 0)
        sx = np.linalg.norm(plane.c2p(1, 0) - origin)

        # Concentric level curves x^2 + y^2 = c
        level_Radii = [1.0, np.sqrt(5), 3.0, np.sqrt(13)]
        level_colors = [GRID, TEAL, GRID, GRID]
        contours = VGroup(
            *[
                Circle(
                    radius=r * sx,
                    color=col,
                    stroke_width=2.4 if col == TEAL else 1.4,
                    stroke_opacity=0.9 if col == TEAL else 0.65,
                ).move_to(origin)
                for r, col in zip(level_Radii, level_colors)
            ]
        )
        c5_lbl = pill_label(MathTex("x^2+y^2=5", color=TEAL, font_size=22).move_to(plane.c2p(-1.9, -1.6)))

        card_levels = make_card(
            VGroup(
                Text("Concentric Level Curves", font_size=17, weight=BOLD, color=TEXT_WHITE, font=self.sans_font),
                MathTex(r"x^2 + y^2 = c \text{ (circles centered at } O\text{)}", color=TEXT_WHITE, font_size=23),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        ).move_to(RIGHT * 3.1 + UP * 1.7)

        self.play_beat(
            "s5.1",
            [
                ([Create(plane), Create(contours), FadeIn(c5_lbl)], 1.6),
                ([FadeIn(card_levels)], 1.0),
            ],
            post_wait=1.0,
        )

        # P0(1,2), radial gradient <2,4> (scaled slightly in arrow display or true vector <2,4> -> (3,6) clipped,
        # let's draw direction of <2,4> with length 1.8 units on this plane so it stays well inside!)
        p0_pt = plane.c2p(1, 2)
        p0_dot = Dot(p0_pt, color=CORAL, radius=0.085)

        grad_dir = np.array([2.0, 4.0]) / np.sqrt(20)
        grad_end = plane.c2p(1 + 1.8 * grad_dir[0], 2 + 1.8 * grad_dir[1])
        grad_arr = Arrow(p0_pt, grad_end, buff=0, color=TEAL, stroke_width=4.8)
        grad_lbl = pill_label(MathTex(r"\nabla f(1,2)", color=TEAL, font_size=24).next_to(grad_arr.get_end(), UL, buff=0.08))

        # Tangent line at (1, 2) perpendicular to <1, 2>
        tang_dir = np.array([-2.0, 1.0]) / np.sqrt(5)
        tang_line = Line(
            plane.c2p(1 - 1.5 * tang_dir[0], 2 - 1.5 * tang_dir[1]),
            plane.c2p(1 + 1.5 * tang_dir[0], 2 + 1.5 * tang_dir[1]),
            color=AMBER,
            stroke_width=2.6,
        )
        right_angle = RightAngle(
            Line(p0_pt, plane.c2p(1 + tang_dir[0], 2 + tang_dir[1])),
            Line(p0_pt, grad_end),
            length=0.22,
            color=AMBER,
        )

        card_ortho = make_card(
            VGroup(
                Text("Orthogonality to Level Curve", font_size=17, weight=BOLD, color=AMBER, font=self.sans_font),
                MathTex(r"\nabla f(1, 2) = \langle 2, 4 \rangle \perp \text{tangent}", color=TEAL, font_size=23),
                MathTex(r"D_{\mathbf{u}_\perp} f = 0 \text{ along } x^2+y^2=5", color=AMBER, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        ).move_to(RIGHT * 3.1 + UP * 0.15)

        self.play_beat(
            "s5.2",
            [
                ([FadeIn(p0_dot), GrowArrow(grad_arr), FadeIn(grad_lbl)], 1.2),
                ([Create(tang_line), Create(right_angle), FadeIn(card_ortho)], 1.5),
            ],
            post_wait=1.0,
        )

        # Unit vector u = <0.6, 0.8> and ~10.3 deg angle comparison
        u_end = plane.c2p(1 + 1.4 * 0.6, 2 + 1.4 * 0.8)
        u_arr = Arrow(p0_pt, u_end, buff=0, color=CYAN, stroke_width=4.4)
        u_lbl = pill_label(MathTex(r"\mathbf{u}", color=CYAN, font_size=24).next_to(u_arr.get_end(), RIGHT, buff=0.08))

        card_angle = make_card(
            VGroup(
                Text("Close Alignment (θ ≈ 10.3°)", font_size=17, weight=BOLD, color=CYAN, font=self.sans_font),
                MathTex(
                    r"\theta = \arccos\!\left(\frac{4.4}{2\sqrt{5}}\right) \approx 10.3^\circ",
                    color=TEXT_WHITE,
                    font_size=23,
                ),
                MathTex(
                    r"D_{\mathbf{u}} f = 4.4 \approx 98.4\% \text{ of } \|\nabla f\|",
                    color=TEAL,
                    font_size=23,
                ),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14),
            stroke_color=CYAN,
        ).move_to(RIGHT * 3.1 + DOWN * 1.55)

        self.play_beat(
            "s5.3",
            [
                ([GrowArrow(u_arr), FadeIn(u_lbl)], 1.1),
                ([FadeIn(card_angle)], 1.4),
            ],
            post_wait=1.2,
        )

        self.play(
            FadeOut(
                VGroup(
                    header, plane, contours, c5_lbl, p0_dot,
                    grad_arr, grad_lbl, tang_line, right_angle,
                    u_arr, u_lbl, card_levels, card_ortho, card_angle,
                )
            ),
            run_time=0.7,
        )
