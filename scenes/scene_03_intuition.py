"""Scene 3: Visual Intuition — Why the gradient points in the direction of steepest increase."""

from __future__ import annotations

import numpy as np
from manim import *

from scenes.common import (
    AMBER,
    AXIS,
    CORAL,
    CYAN,
    GRID,
    MUTED,
    PANEL_BG,
    PANEL_STROKE,
    TEAL,
    TEXT_WHITE,
    BaseMathScene,
    make_card,
    make_scene_header,
    pill_label,
)


class Scene03Intuition(BaseMathScene):
    def construct(self) -> None:
        self.setup_scene()
        header = make_scene_header(
            "Scene 3 • Visual Intuition",
            "Why the Gradient Points Steepest",
            self.sans_font,
        )
        self.play(FadeIn(header), run_time=0.6)

        plane = NumberPlane(
            x_range=(-2.5, 2.5, 1),
            y_range=(-2.5, 2.5, 1),
            x_length=5.4,
            y_length=5.4,
            axis_config={"stroke_color": AXIS, "stroke_width": 1.8},
            background_line_style={"stroke_color": GRID, "stroke_width": 1.0, "stroke_opacity": 0.5},
        ).move_to(LEFT * 3.1 + DOWN * 0.1)

        origin = plane.c2p(0, 0)
        unit_r = np.linalg.norm(plane.c2p(1, 0) - origin)
        contours = VGroup(
            *[
                Circle(radius=r * unit_r, color=GRID, stroke_width=1.4, stroke_opacity=0.65).move_to(origin)
                for r in (0.7, 1.3, 1.9)
            ]
        )
        unit_circle = Circle(radius=unit_r, color=CYAN, stroke_width=1.6, stroke_opacity=0.65).move_to(origin)

        # Fixed gradient pointing at 35 degrees
        grad_angle = 35 * DEGREES
        grad_end = origin + unit_r * 1.85 * np.array([np.cos(grad_angle), np.sin(grad_angle), 0.0])
        grad_arr = Arrow(origin, grad_end, buff=0, color=TEAL, stroke_width=5.0)
        lbl_grad = pill_label(MathTex(r"\nabla f", color=TEAL, font_size=28).next_to(grad_end, UR, buff=0.08))

        theta_tracker = ValueTracker(55 * DEGREES)

        def make_u_arrow() -> Arrow:
            ang = grad_angle + theta_tracker.get_value()
            end = origin + unit_r * np.array([np.cos(ang), np.sin(ang), 0.0])
            return Arrow(origin, end, buff=0, color=CYAN, stroke_width=4.2)

        u_arr = always_redraw(make_u_arrow)
        u_lbl = always_redraw(
            lambda: pill_label(
                MathTex(r"\mathbf{u}", color=CYAN, font_size=24).next_to(
                    origin + unit_r * 1.18 * np.array([
                        np.cos(grad_angle + theta_tracker.get_value()),
                        np.sin(grad_angle + theta_tracker.get_value()),
                        0.0,
                    ]),
                    ORIGIN,
                )
            )
        )

        # Right side: Dot product identity card
        id_card = make_card(
            VGroup(
                Text("Dot Product Identity", font_size=17, weight=BOLD, color=TEXT_WHITE, font=self.sans_font),
                MathTex(
                    r"D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u} = \|\nabla f\|\,\|\mathbf{u}\|\cos\theta",
                    color=TEXT_WHITE,
                    font_size=24,
                ),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        ).move_to(RIGHT * 3.1 + UP * 1.55)

        self.play_beat(
            "s3.1",
            [
                ([Create(plane), Create(contours), Create(unit_circle)], 1.4),
                ([GrowArrow(grad_arr), FadeIn(lbl_grad), FadeIn(u_arr), FadeIn(u_lbl)], 1.2),
                ([FadeIn(id_card)], 1.0),
            ],
            post_wait=1.0,
        )

        # Simplified formula since ||u|| = 1
        simp_card = make_card(
            VGroup(
                MathTex(r"\|\mathbf{u}\| = 1 \implies D_{\mathbf{u}} f = \|\nabla f\|\cos\theta", color=TEAL, font_size=26),
            )
        ).move_to(RIGHT * 3.1 + UP * 0.35)

        # Live cos(theta) gauge
        gauge_bg = RoundedRectangle(
            width=4.8, height=0.34, corner_radius=0.08,
            stroke_color=PANEL_STROKE, stroke_width=1.2, fill_color=PANEL_BG, fill_opacity=0.95,
        ).move_to(RIGHT * 3.1 + DOWN * 0.65)
        gauge_zero = Line(gauge_bg.get_top(), gauge_bg.get_bottom(), color=MUTED, stroke_width=1.5).move_to(gauge_bg.get_center())

        def make_gauge_fill() -> Mobject:
            val = np.cos(theta_tracker.get_value())
            half_w = 2.3
            w = max(0.04, abs(val) * half_w)
            col = TEAL if val > 0.1 else (CORAL if val < -0.1 else AMBER)
            bar = Rectangle(width=w, height=0.22, fill_color=col, fill_opacity=0.9, stroke_width=0)
            if val >= 0:
                bar.move_to(gauge_bg.get_center() + RIGHT * (w / 2.0))
            else:
                bar.move_to(gauge_bg.get_center() + LEFT * (w / 2.0))
            return bar

        gauge_fill = always_redraw(make_gauge_fill)
        gauge_labels = VGroup(
            MathTex(r"-\|\nabla f\|", color=CORAL, font_size=20).next_to(gauge_bg, LEFT, buff=0.12),
            MathTex(r"0", color=AMBER, font_size=20).next_to(gauge_bg, DOWN, buff=0.1),
            MathTex(r"+\|\nabla f\|", color=TEAL, font_size=20).next_to(gauge_bg, RIGHT, buff=0.12),
        )

        self.play_beat(
            "s3.2",
            [
                ([FadeIn(simp_card), FadeIn(gauge_bg), FadeIn(gauge_zero), FadeIn(gauge_fill), FadeIn(gauge_labels)], 1.6),
            ],
            post_wait=1.0,
        )

        # Sweep to theta = 0 (steepest increase)
        regime_max = make_card(
            VGroup(
                MathTex(r"\theta = 0^\circ \implies \cos\theta = 1", color=TEAL, font_size=24),
                Text("Maximum ascent: D_u f = ||∇f||", font_size=16, color=TEXT_WHITE, font=self.sans_font),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        ).move_to(RIGHT * 3.1 + DOWN * 1.85)

        self.play_beat(
            "s3.3",
            [
                ([theta_tracker.animate.set_value(0.0)], 2.2),
                ([FadeIn(regime_max)], 1.0),
            ],
            post_wait=1.0,
        )

        # Sweep to theta = 90 (tangent, zero change) and 180 (steepest descent)
        regime_zero = make_card(
            VGroup(
                MathTex(r"\theta = 90^\circ \implies \cos\theta = 0 \implies D_{\mathbf{u}}f = 0", color=AMBER, font_size=22),
                MathTex(r"\theta = 180^\circ \implies \cos\theta = -1 \implies -\|\nabla f\|", color=CORAL, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        ).move_to(RIGHT * 3.1 + DOWN * 1.85)

        self.play_beat(
            "s3.4",
            [
                ([FadeOut(regime_max), theta_tracker.animate.set_value(90 * DEGREES)], 2.0),
                ([FadeIn(regime_zero)], 0.8),
                ([theta_tracker.animate.set_value(180 * DEGREES)], 2.0),
            ],
            post_wait=1.2,
        )

        self.play(
            FadeOut(
                VGroup(
                    header, plane, contours, unit_circle, grad_arr, lbl_grad,
                    u_arr, u_lbl, id_card, simp_card,
                    gauge_bg, gauge_zero, gauge_fill, gauge_labels, regime_zero,
                )
            ),
            run_time=0.7,
        )
