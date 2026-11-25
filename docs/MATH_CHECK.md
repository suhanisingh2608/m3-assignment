# Mathematical Verification Oracle — Gradient and Directional Derivatives

**Topic:** Gradient and Directional Derivatives  
**Course:** M3 — Linear Algebra and Calculus  
**Status:** Drafted for student review (pending final student sign-off)

---

## 1. Core Definitions

- **Scalar field:** $f(x, y)$ differentiable on $\mathbb{R}^2$.
- **Partial derivatives:**
  $$\frac{\partial f}{\partial x}, \qquad \frac{\partial f}{\partial y}$$
- **Gradient vector:**
  $$\nabla f(x, y) = \left\langle \frac{\partial f}{\partial x},\, \frac{\partial f}{\partial y} \right\rangle$$
- **Unit direction vector:** $\mathbf{u} = \langle u_1, u_2 \rangle$ with $\|\mathbf{u}\| = \sqrt{u_1^2 + u_2^2} = 1$.
- **Directional derivative:**
  $$D_{\mathbf{u}} f(x, y) = \nabla f(x, y) \cdot \mathbf{u} = \frac{\partial f}{\partial x} u_1 + \frac{\partial f}{\partial y} u_2$$

---

## 2. Steepest Increase Proof

Using the geometric dot product where $\theta \in [0^\circ, 180^\circ]$ is the angle between $\nabla f$ and $\mathbf{u}$:
$$D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u} = \|\nabla f\|\,\|\mathbf{u}\|\cos\theta = \|\nabla f\|\cos\theta \quad (\text{since } \|\mathbf{u}\| = 1)$$

Since $-1 \le \cos\theta \le 1$:
- $\theta = 0^\circ \implies \cos\theta = 1 \implies D_{\mathbf{u}} f = \|\nabla f\|$ (maximum rate of change, same direction as $\nabla f$).
- $\theta = 90^\circ \implies \cos\theta = 0 \implies D_{\mathbf{u}} f = 0$ (tangent to level curve $f(x, y) = c$).
- $\theta = 180^\circ \implies \cos\theta = -1 \implies D_{\mathbf{u}} f = -\|\nabla f\|$ (steepest decrease, opposite $\nabla f$).

---

## 3. Worked Example Verification: $f(x, y) = x^2 + y^2$

- **Evaluation point:** $P_0 = (1, 2)$, where $f(1, 2) = 1^2 + 2^2 = 5$.
- **Partial derivatives:**
  $$\frac{\partial f}{\partial x} = 2x, \qquad \frac{\partial f}{\partial y} = 2y$$
- **Gradient:**
  $$\nabla f(x, y) = \langle 2x, 2y \rangle \implies \nabla f(1, 2) = \langle 2(1), 2(2) \rangle = \langle 2, 4 \rangle$$
- **Magnitude of gradient:**
  $$\|\nabla f(1, 2)\| = \sqrt{2^2 + 4^2} = \sqrt{4 + 16} = \sqrt{20} = 2\sqrt{5} \approx 4.4721$$
- **Unit direction vector:** $\mathbf{u} = \left\langle \frac{3}{5}, \frac{4}{5} \right\rangle = \langle 0.6, 0.8 \rangle$
  - Unit check: $\|\mathbf{u}\| = \sqrt{\left(\frac{3}{5}\right)^2 + \left(\frac{4}{5}\right)^2} = \sqrt{\frac{9}{25} + \frac{16}{25}} = \sqrt{\frac{25}{25}} = 1$.
- **Directional derivative:**
  $$D_{\mathbf{u}} f(1, 2) = \langle 2, 4 \rangle \cdot \left\langle \frac{3}{5}, \frac{4}{5} \right\rangle = 2\left(\frac{3}{5}\right) + 4\left(\frac{4}{5}\right) = \frac{6}{5} + \frac{16}{5} = \frac{22}{5} = 4.4$$
- **Angle between $\mathbf{u}$ and $\nabla f(1, 2)$:**
  $$\cos\theta = \frac{\nabla f(1, 2) \cdot \mathbf{u}}{\|\nabla f(1, 2)\|\,\|\mathbf{u}\|} = \frac{4.4}{2\sqrt{5}} = \frac{2.2}{\sqrt{5}} \approx 0.98387 \implies \theta = \arccos\!\left(\frac{2.2}{\sqrt{5}}\right) \approx 10.305^\circ \approx 10.3^\circ$$
- **Tangent direction check:** $\mathbf{u}_\perp = \left\langle -\frac{2}{\sqrt{5}}, \frac{1}{\sqrt{5}} \right\rangle \implies \nabla f(1, 2) \cdot \mathbf{u}_\perp = 2\left(-\frac{2}{\sqrt{5}}\right) + 4\left(\frac{1}{\sqrt{5}}\right) = 0$.
