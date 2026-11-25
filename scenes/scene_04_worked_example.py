"""Scene 4: Worked Example — f(x, y) = x^2 + y^2 at P0 = (1, 2) in direction u = <3/5, 4/5>."""

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


class Scene04WorkedExample(BaseMathScene):
    def construct(self) -> None:
        self.setup_scene()
        header = make_scene_header(
            "Scene 4 • Worked Example",
            "f(x, y) = x² + y² at P₀ = (1, 2)",
            self.sans_font,
        )
        self.play(FadeIn(header), run_time=0.6)

        # Left coordinate plane sized so (1, 2) + (2, 4) = (3, 6) fits cleanly
        plane = NumberPlane(
            x_range=(-1.5, 4.5, 1),
            y_range=(-1.0, 6.5, 1),
            x_length=5.2,
            y_length=5.4,
            axis_config={"stroke_color": AXIS, "stroke_width": 1.8},
            background_line_style={"stroke_color": GRID, "stroke_width": 1.0, "stroke_opacity": 0.5},
        ).move_to(LEFT * 3.3 + DOWN * 0.15)

        origin = plane.c2p(0, 0)
        sx = np.linalg.norm(plane.c2p(1, 0) - origin)
        circle_5 = Circle(radius=np.sqrt(5) * sx, color=GRID, stroke_width=2.0, stroke_opacity=0.85).move_to(origin)

        p0_pt = plane.c2p(1, 2)
        p0_dot = Dot(p0_pt, color=CORAL, radius=0.085)
        p0_lbl = pill_label(MathTex("P_0(1, 2)", color=CORAL, font_size=24).next_to(p0_dot, LEFT, buff=0.12))

        # Step 1 card: function & point
        step1 = make_card(
            VGroup(
                MathTex(r"f(x, y) = x^2 + y^2,\quad P_0 = (1, 2)", color=TEXT_WHITE, font_size=21),
                MathTex(r"f(1, 2) = 1^2 + 2^2 = 5", color=AMBER, font_size=21),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.10),
            pad_y=0.20,
        ).move_to(RIGHT * 3.1 + UP * 2.45)

        self.play_beat(
            "s4.1",
            [
                ([Create(plane), Create(circle_5), FadeIn(p0_dot), FadeIn(p0_lbl)], 1.6),
                ([FadeIn(step1)], 1.0),
            ],
            post_wait=1.0,
        )

        # Step 2: Partials & gradient
        grad_arr = Arrow(p0_pt, plane.c2p(3, 6), buff=0, color=TEAL, stroke_width=4.8)
        grad_lbl = pill_label(MathTex(r"\nabla f(1,2)=\langle 2,4\rangle", color=TEAL, font_size=23).next_to(grad_arr.get_end(), DOWN + RIGHT, buff=0.08))

        step2 = make_card(
            VGroup(
                MathTex(r"\frac{\partial f}{\partial x} = 2x,\qquad \frac{\partial f}{\partial y} = 2y", color=CYAN, font_size=21),
                MathTex(r"\nabla f(1, 2) = \langle 2(1), 2(2) \rangle = \langle 2, 4 \rangle", color=TEAL, font_size=21),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.10),
            pad_y=0.20,
        ).next_to(step1, DOWN, buff=0.16, aligned_edge=LEFT)

        self.play_beat(
            "s4.2",
            [
                ([FadeIn(step2)], 1.4),
                ([GrowArrow(grad_arr), FadeIn(grad_lbl)], 1.3),
            ],
            post_wait=1.0,
        )

        # Step 3: Unit vector u = <3/5, 4/5>
        u_arr = Arrow(p0_pt, plane.c2p(1 + 0.6, 2 + 0.8), buff=0, color=CYAN, stroke_width=4.4)
        u_lbl = pill_label(MathTex(r"\mathbf{u}=\langle \tfrac{3}{5}, \tfrac{4}{5}\rangle", color=CYAN, font_size=22).next_to(u_arr.get_end(), RIGHT, buff=0.1))

        step3 = make_card(
            VGroup(
                MathTex(r"\mathbf{u} = \left\langle \frac{3}{5},\, \frac{4}{5} \right\rangle", color=CYAN, font_size=21),
                MathTex(
                    r"\|\mathbf{u}\| = \sqrt{\left(\frac{3}{5}\right)^2 + \left(\frac{4}{5}\right)^2} = \sqrt{\frac{9}{25}+\frac{16}{25}} = 1",
                    color=TEXT_WHITE,
                    font_size=19,
                ),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.10),
            pad_y=0.20,
        ).next_to(step2, DOWN, buff=0.16, aligned_edge=LEFT)

        self.play_beat(
            "s4.3",
            [
                ([GrowArrow(u_arr), FadeIn(u_lbl)], 1.2),
                ([FadeIn(step3)], 1.4),
            ],
            post_wait=1.0,
        )

        # Step 4: Dot product and max steepness comparison
        step4 = make_card(
            VGroup(
                MathTex(
                    r"D_{\mathbf{u}} f(1,2) = \langle 2, 4 \rangle \cdot \left\langle \frac{3}{5}, \frac{4}{5} \right\rangle = \frac{6}{5} + \frac{16}{5} = \frac{22}{5} = 4.4",
                    color=TEAL,
                    font_size=19,
                ),
                MathTex(
                    r"\|\nabla f(1,2)\| = \sqrt{2^2 + 4^2} = \sqrt{20} = 2\sqrt{5} \approx 4.47",
                    color=AMBER,
                    font_size=20,
                ),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.10),
            pad_y=0.20,
            stroke_color=TEAL,
        ).next_to(step3, DOWN, buff=0.16, aligned_edge=LEFT)

        self.play_beat(
            "s4.4",
            [
                ([FadeIn(step4)], 1.8),
            ],
            post_wait=1.4,
        )

        self.play(
            FadeOut(
                VGroup(
                    header, plane, circle_5, p0_dot, p0_lbl,
                    grad_arr, grad_lbl, u_arr, u_lbl,
                    step1, step2, step3, step4,
                )
            ),
            run_time=0.7,
        )
