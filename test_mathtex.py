from manim import *

class TestMathTexRender(Scene):
    def construct(self):
        title = Text("M3 Calculus: Derivatives & Gradient", font_size=32).to_edge(UP)
        
        # 1. Partial derivative
        partial_deriv = MathTex(r"\frac{\partial f}{\partial x}", color=BLUE)
        
        # 2. Gradient vector
        gradient_vec = MathTex(r"\nabla f(x, y) = \left\langle \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right\rangle", color=YELLOW)
        
        # 3. Directional derivative
        dir_deriv = MathTex(r"D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}", color=GREEN)
        
        formulas = VGroup(partial_deriv, gradient_vec, dir_deriv).arrange(DOWN, buff=0.6).next_to(title, DOWN, buff=0.8)
        
        self.play(FadeIn(title))
        self.play(Write(partial_deriv))
        self.play(Write(gradient_vec))
        self.play(Write(dir_deriv))
        self.wait(1)
