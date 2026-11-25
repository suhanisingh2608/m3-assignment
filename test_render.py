from manim import *

class TestRender(Scene):
    def construct(self):
        title = Text("Gradient & Directional Derivatives", font_size=36, color=BLUE)
        dot = Dot(color=YELLOW)
        arrow = Arrow(start=ORIGIN, end=RIGHT*2, color=GREEN)
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))
        self.play(FadeIn(dot), GrowArrow(arrow))
        self.wait(1)
