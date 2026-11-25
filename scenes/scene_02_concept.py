"""Scene 2: Concept Introduction — Partial derivatives, gradient, unit vector, and directional derivative."""

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


class Scene02Concept(BaseMathScene):
    def construct(self) -> None:
        self.setup_scene()
        header = make_scene_header(
            "Scene 2 • Concept Introduction",
            "Partial Derivatives, Gradient & Directional Derivative",
            self.sans_font,
        )
        self.play(FadeIn(header), run_time=0.6)

        plane = NumberPlane(
            x_range=(-2.5, 3.5, 1),
            y_range=(-2.0, 3.5, 1),
            x_length=5.6,
            y_length=5.2,
            axis_config={"stroke_color": AXIS, "stroke_width": 1.8},
            background_line_style={"stroke_color": GRID, "stroke_width": 1.1, "stroke_opacity": 0.55},
        ).move_to(LEFT * 3.0 + DOWN * 0.1)

        p0 = plane.c2p(0.0, 0.0)
        p0_dot = Dot(p0, color=CORAL, radius=0.08)

        # Coordinate partial vectors
        vx = Arrow(p0, plane.c2p(1.8, 0.0), buff=0, color=CYAN, stroke_width=4.2)
        vy = Arrow(p0, plane.c2p(0.0, 2.2), buff=0, color=AMBER, stroke_width=4.2)
        lbl_vx = pill_label(MathTex(r"\frac{\partial f}{\partial x}", color=CYAN, font_size=26).next_to(vx.get_end(), DOWN, buff=0.12))
        lbl_vy = pill_label(MathTex(r"\frac{\partial f}{\partial y}", color=AMBER, font_size=26).next_to(vy.get_end(), LEFT, buff=0.12))

        card_partials = make_card(
            VGroup(
                Text("1. Partial Derivatives", font_size=16, weight=BOLD, color=TEXT_WHITE, font=self.sans_font),
                MathTex(r"\frac{\partial f}{\partial x} \text{ (hold } y \text{ fixed)}", color=CYAN, font_size=22),
                MathTex(r"\frac{\partial f}{\partial y} \text{ (hold } x \text{ fixed)}", color=AMBER, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14),
            pad_y=0.22,
        ).move_to(RIGHT * 3.1 + UP * 2.15)

        self.play_beat(
            "s2.1",
            [
                ([Create(plane), FadeIn(p0_dot)], 1.0),
                ([GrowArrow(vx), FadeIn(lbl_vx)], 1.0),
                ([GrowArrow(vy), FadeIn(lbl_vy), FadeIn(card_partials)], 1.2),
            ],
            post_wait=1.0,
        )

        # Combine into gradient vector
        dash_x = DashedLine(plane.c2p(0.0, 2.2), plane.c2p(1.8, 2.2), color=GRID, stroke_width=1.6)
        dash_y = DashedLine(plane.c2p(1.8, 0.0), plane.c2p(1.8, 2.2), color=GRID, stroke_width=1.6)
        grad_arr = Arrow(p0, plane.c2p(1.8, 2.2), buff=0, color=TEAL, stroke_width=5.0)
        lbl_grad = pill_label(MathTex(r"\nabla f", color=TEAL, font_size=28).next_to(grad_arr.get_end(), UR, buff=0.1))

        card_grad = make_card(
            VGroup(
                Text("2. Gradient Vector", font_size=16, weight=BOLD, color=TEXT_WHITE, font=self.sans_font),
                MathTex(
                    r"\nabla f(x, y) = \left\langle \frac{\partial f}{\partial x},\, \frac{\partial f}{\partial y} \right\rangle",
                    color=TEAL,
                    font_size=23,
                ),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14),
            pad_y=0.22,
        ).next_to(card_partials, DOWN, buff=0.22, aligned_edge=LEFT)

        self.play_beat(
            "s2.2",
            [
                ([Create(dash_x), Create(dash_y), GrowArrow(grad_arr), FadeIn(lbl_grad)], 1.4),
                ([FadeIn(card_grad)], 1.0),
            ],
            post_wait=1.0,
        )

        # Unit circle and arbitrary unit direction vector u
        unit_radius = np.linalg.norm(plane.c2p(1.0, 0.0) - p0)
        unit_circle = Circle(radius=unit_radius, color=CYAN, stroke_width=1.8, stroke_opacity=0.65).move_to(p0)
        u_arr = Arrow(p0, plane.c2p(np.cos(0.45), np.sin(0.45)), buff=0, color=CYAN, stroke_width=4.2)
        lbl_u = pill_label(MathTex(r"\mathbf{u},\ \|\mathbf{u}\|=1", color=CYAN, font_size=24).next_to(u_arr.get_end(), DR, buff=0.1))

        card_dir = make_card(
            VGroup(
                Text("3. Directional Derivative", font_size=16, weight=BOLD, color=TEXT_WHITE, font=self.sans_font),
                MathTex(r"\mathbf{u} = \langle u_1, u_2 \rangle,\quad \|\mathbf{u}\| = 1", color=CYAN, font_size=22),
                MathTex(
                    r"D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u} = \frac{\partial f}{\partial x}u_1 + \frac{\partial f}{\partial y}u_2",
                    color=TEXT_WHITE,
                    font_size=22,
                ),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14),
            pad_y=0.22,
        ).next_to(card_grad, DOWN, buff=0.22, aligned_edge=LEFT)

        self.play_beat(
            "s2.3",
            [
                ([Create(unit_circle), GrowArrow(u_arr), FadeIn(lbl_u)], 1.5),
                ([FadeIn(card_dir)], 1.2),
            ],
            post_wait=1.2,
        )

        self.play(
            FadeOut(
                VGroup(
                    header, plane, p0_dot, vx, vy, lbl_vx, lbl_vy,
                    dash_x, dash_y, grad_arr, lbl_grad,
                    unit_circle, u_arr, lbl_u,
                    card_partials, card_grad, card_dir,
                )
            ),
            run_time=0.7,
        )
