# M3 Internal Assessment — Gradient and Directional Derivatives

An original, mathematically rigorous **Manim Community Edition** animation explaining **partial derivatives**, the **gradient vector**, **directional derivatives**, and **steepest ascent** using the worked example $f(x, y) = x^2 + y^2$.

- **Repository:** https://github.com/suhanisingh2608/m3-assignment
- **Final Video:** [Final_Video.mp4](output/Final_Video.mp4) (`1920×1080`, `30 fps`, `16:9`)
- **Subtitles:** [Final_Video.srt](output/Final_Video.srt)
- **Storyboard PDF:** [Storyboard.pdf](storyboard/Storyboard.pdf)
- **Math Verification Oracle:** [MATH_CHECK.md](docs/MATH_CHECK.md)

---

## Mathematical Concept Explained

1. **Partial Derivatives & Gradient Vector:**
   $$\nabla f(x, y) = \left\langle \frac{\partial f}{\partial x},\, \frac{\partial f}{\partial y} \right\rangle$$
2. **Directional Derivative (with unit direction $\mathbf{u}$, $\|\mathbf{u}\| = 1$):**
   $$D_{\mathbf{u}} f(x, y) = \nabla f(x, y) \cdot \mathbf{u} = \|\nabla f\|\cos\theta$$
3. **Why $\nabla f$ Points in the Direction of Steepest Increase:**
   Since $\|\mathbf{u}\| = 1$ and $-1 \le \cos\theta \le 1$, the maximum rate of change $\|\nabla f\|$ occurs at $\theta = 0^\circ$ (aligned with $\nabla f$), and zero change occurs at $\theta = 90^\circ$ (tangent to level curves).
4. **Worked Example ($f(x, y) = x^2 + y^2$ at $P_0(1, 2)$):**
   - $\nabla f(1, 2) = \langle 2, 4 \rangle$, $\|\nabla f(1, 2)\| = \sqrt{20} = 2\sqrt{5} \approx 4.4721$
   - Unit direction $\mathbf{u} = \left\langle \frac{3}{5}, \frac{4}{5} \right\rangle$ ($\|\mathbf{u}\| = 1$)
   - $D_{\mathbf{u}} f(1, 2) = \frac{22}{5} = 4.4$
   - Angle between $\mathbf{u}$ and $\nabla f(1, 2)$: $\theta = \arccos\!\left(\frac{2.2}{\sqrt{5}}\right) \approx 10.3^\circ$

---

## Tools & Dependencies

- **Python:** `3.12.3` (isolated `.venv`)
- **Manim Community Edition:** `0.22.1`
- **Scientific Libraries:** `numpy`, `scipy`, `python-dotenv`
- **LaTeX Toolchain:** BasicTeX (`pdflatex` TeX Live 2026, `dvisvgm` 3.6)
- **Video & Audio:** `ffmpeg` 9.1, offline macOS `say` TTS + `.srt` subtitle generation

---

## Render & Assembly Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# (Optional) Regenerate offline narration WAV clips
PYTHONPATH="." python scripts/generate_voiceovers.py

# Render all 6 scenes at 1080p, 30 fps
export PATH="/Library/TeX/texbin:/opt/homebrew/bin:$PATH"
export PYTHONPATH="."
manim -qh scenes/scene_01_hook.py Scene01Hook
manim -qh scenes/scene_02_concept.py Scene02Concept
manim -qh scenes/scene_03_intuition.py Scene03Intuition
manim -qh scenes/scene_04_worked_example.py Scene04WorkedExample
manim -qh scenes/scene_05_interpretation.py Scene05Interpretation
manim -qh scenes/scene_06_summary_credits.py Scene06SummaryCredits

# Assemble final MP4 and merged SRT subtitles
python scenes/assemble_video.py --quality 1080p30 --output output/Final_Video.mp4

# Compile Storyboard PDF
cd storyboard && pdflatex storyboard.tex && pdflatex storyboard.tex
```

---

## AI Tools Disclosure

AI assistance (**Google Antigravity**) was used for project planning and Python/Manim code generation. Offline voiceover audio was generated locally via macOS `say`. Final mathematical review and verification by the student is pending prior to final submission. See [AI_DISCLOSURE.md](docs/AI_DISCLOSURE.md) for details.
