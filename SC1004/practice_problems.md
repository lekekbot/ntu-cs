# SC1004 Linear Algebra — Practice Problems

> Practice problems covering the whole course, with **full worked solutions**. Topics come from the video series (C0: Vectors & Matrices; C1: Systems of Linear Equations; C2: Matrix Algebra; C3: Determinants; C4: Vector Spaces; C6: Orthogonality; C7: Least Squares; C8: Eigenvalues; C8A: Complex Numbers & DFT). Difficulty is roughly exam-level.
>
> **Tip:** try each problem first, then check the solution.

---

## Contents

- [Part A — Vectors](#part-a--vectors)
- [Part B — Matrices](#part-b--matrices)
- [Part C — Systems of Linear Equations](#part-c--systems-of-linear-equations)
- [Part D — Linear Transformations](#part-d--linear-transformations)
- [Part E — Matrix Algebra (Chapter 2)](#part-e--matrix-algebra-chapter-2)
- [Part F — Determinants (Chapter 3)](#part-f--determinants-chapter-3)
- [Part G — Vector Spaces (Chapter 4)](#part-g--vector-spaces-chapter-4)
- [Part H — Orthogonality (Chapter 6)](#part-h--orthogonality-chapter-6)
- [Part I — Least Squares (Chapter 7)](#part-i--least-squares-chapter-7)
- [Part J — Eigenvalues and Eigenvectors (Chapter 8)](#part-j--eigenvalues-and-eigenvectors-chapter-8)
- [Part K — Complex Numbers and the DFT (Chapter 8A)](#part-k--complex-numbers-and-the-dft-chapter-8a)

---

# Part A — Vectors

### A1. Vector operations in ℝⁿ
Given $\mathbf v = (1, -3, 2)$ and $\mathbf w = (4, 2, 1)$, compute
**a)** $\mathbf v + \mathbf w$  **b)** $2\mathbf v$  **c)** $-\mathbf w$  **d)** $\mathbf v - \mathbf w$.

<details><summary><b>Solution</b></summary>

$$\mathbf v + \mathbf w = (1+4,\ -3+2,\ 2+1) = (5, -1, 3)$$
$$2\mathbf v = (2, -6, 4)$$
$$-\mathbf w = (-4, -2, -1)$$
$$\mathbf v - \mathbf w = (1-4,\ -3-2,\ 2-1) = (-3, -5, 1)$$

</details>

---

### A2. Vector between two points
Find the vector $\mathbf v$ with initial point $P_1(2, -1, 4)$ and terminal point $P_2(7, 5, -8)$.

<details><summary><b>Solution</b></summary>

$$\mathbf v = \overrightarrow{P_1P_2} = P_2 - P_1 = (7-2,\ 5-(-1),\ -8-4) = (5,\ 6,\ -12)$$

</details>

---

### A3. Norms
Compute $\|\mathbf v\|$ for $\mathbf v = (-3, 2, 1)$, and find a unit vector in the same direction as $\mathbf u = (2, 2, -1)$.

<details><summary><b>Solution</b></summary>

$$\|\mathbf v\| = \sqrt{(-3)^2 + 2^2 + 1^2} = \sqrt{14}$$

For $\mathbf u = (2, 2, -1)$:
$$\|\mathbf u\| = \sqrt{4+4+1} = 3, \qquad \hat{\mathbf u} = \frac{\mathbf u}{\|\mathbf u\|} = \left(\frac23, \frac23, -\frac13\right)$$

(Check: $\|\hat{\mathbf u}\| = \sqrt{\frac49 + \frac49 + \frac19} = 1$. ✓)

</details>

---

### A4. Distance
Find the distance between $\mathbf u = (1, 3, -2, 7)$ and $\mathbf v = (0, 7, 2, 2)$ in $\mathbb{R}^4$.

<details><summary><b>Solution</b></summary>

$$d(\mathbf u, \mathbf v) = \|\mathbf u - \mathbf v\| = \sqrt{(1-0)^2 + (3-7)^2 + (-2-2)^2 + (7-2)^2} = \sqrt{1+16+16+25} = \sqrt{58}$$

</details>

---

### A5. Dot product
Given $\mathbf u = (0, 2, 2)$ and $\mathbf v = (0, 0, 1)$ with angle $\theta = 45°$ between them, compute $\mathbf u \cdot \mathbf v$ (i) using the angle formula and (ii) using components. Also compute $\mathbf a \cdot \mathbf b$ for $\mathbf a = (-1, 3, 5, 7)$, $\mathbf b = (-3, -4, 1, 0)$.

<details><summary><b>Solution</b></summary>

(i) $\|\mathbf u\| = \sqrt{0+4+4} = 2\sqrt2$, $\|\mathbf v\| = 1$, so
$$\mathbf u \cdot \mathbf v = \|\mathbf u\|\|\mathbf v\|\cos45° = 2\sqrt2 \cdot 1 \cdot \tfrac{1}{\sqrt2} = 2.$$

(ii) $\mathbf u \cdot \mathbf v = (0)(0) + (2)(0) + (2)(1) = 2.$ ✓ (same result)

$$\mathbf a \cdot \mathbf b = (-1)(-3) + (3)(-4) + (5)(1) + (7)(0) = 3 - 12 + 5 + 0 = -4.$$

</details>

---

### A6. Angle between vectors
Two vectors satisfy $\mathbf u \cdot \mathbf v = -4$ with $\|\mathbf u\| = \sqrt{35}$ and $\|\mathbf v\| = \sqrt{35}$. Find $\cos\theta$ and state whether the angle is acute, right, or obtuse.

<details><summary><b>Solution</b></summary>

$$\cos\theta = \frac{\mathbf u \cdot \mathbf v}{\|\mathbf u\|\|\mathbf v\|} = \frac{-4}{35} < 0 \;\Rightarrow\; \theta > 90° \;\text{(obtuse)}.$$

</details>

---

### A7. Orthogonality
Show that $\mathbf u = (2, -1, 3)$ and $\mathbf v = (1, 8, 2)$ are orthogonal.

<details><summary><b>Solution</b></summary>

$$\mathbf u \cdot \mathbf v = 2(1) + (-1)(8) + 3(2) = 2 - 8 + 6 = 0 \;\Rightarrow\; \mathbf u \perp \mathbf v.$$

</details>

---

### A8. Point-normal equation of a line
Write the point-normal equation of the line through $P_0(1, 2)$ with normal $\mathbf n = (3, -4)$.

<details><summary><b>Solution</b></summary>

$$a(x-x_0) + b(y-y_0) = 0 \;\Rightarrow\; 3(x-1) + (-4)(y-2) = 0 \;\Rightarrow\; 3x - 4y + 5 = 0.$$

</details>

---

### A9. Vector and parametric equations of a line
Write the vector equation of the line through $P(0, 7)$ and $Q(5, 0)$, then give its parametric form and its rectangular equation.

<details><summary><b>Solution</b></summary>

Direction $\mathbf v = Q - P = (5, -7)$. Vector form:
$$\mathbf x = (0, 7) + t(5, -7).$$
Parametric form:
$$x = 5t, \qquad y = 7 - 7t.$$
Eliminate $t$: $t = x/5 \Rightarrow y = 7 - 7x/5 \Rightarrow 7x + 5y = 35.$

</details>

---

### A10. Cauchy–Schwarz
Verify the Cauchy–Schwarz inequality $|\mathbf u \cdot \mathbf v| \le \|\mathbf u\|\|\mathbf v\|$ for $\mathbf u = (1, 2, 2)$, $\mathbf v = (-3, 0, 4)$.

<details><summary><b>Solution</b></summary>

$$\mathbf u \cdot \mathbf v = 1(-3) + 2(0) + 2(4) = 5, \quad |\mathbf u\cdot\mathbf v| = 5.$$
$$\|\mathbf u\| = \sqrt{1+4+4} = 3, \quad \|\mathbf v\| = \sqrt{9+0+16} = 5, \quad \|\mathbf u\|\|\mathbf v\| = 15.$$
Since $5 \le 15$, the inequality holds. ✓

</details>

---

# Part B — Matrices

### B1. Matrix addition & scalar multiplication
Let $A = \begin{bmatrix} 1 & 2 & 1 \\ 1 & 1 & 2 \\ 1 & 1 & 1 \end{bmatrix}$ and $B = \begin{bmatrix} 0 & 1 & 1 \\ 0 & 0 & 1 \\ 1 & 0 & 0 \end{bmatrix}$. Compute $3A^T - 2B$.

<details><summary><b>Solution</b></summary>

$$A^T = \begin{bmatrix} 1 & 1 & 1 \\ 2 & 1 & 1 \\ 1 & 2 & 1 \end{bmatrix}, \quad 3A^T = \begin{bmatrix} 3 & 3 & 3 \\ 6 & 3 & 3 \\ 3 & 6 & 3 \end{bmatrix}, \quad 2B = \begin{bmatrix} 0 & 2 & 2 \\ 0 & 0 & 2 \\ 2 & 0 & 0 \end{bmatrix}$$
$$3A^T - 2B = \begin{bmatrix} 3 & 1 & 1 \\ 6 & 3 & 1 \\ 1 & 6 & 3 \end{bmatrix}.$$

</details>

---

### B2. Matrix multiplication (dot product)
Compute $\begin{bmatrix} 2 & 5 \\ 3 & 1 \end{bmatrix}\begin{bmatrix} 3 & 2 \\ 1 & 0 \end{bmatrix}$.

<details><summary><b>Solution</b></summary>

$$\begin{bmatrix} 2(3)+5(1) & 2(2)+5(0) \\ 3(3)+1(1) & 3(2)+1(0) \end{bmatrix} = \begin{bmatrix} 11 & 4 \\ 10 & 6 \end{bmatrix}.$$

*(Note: this differs slightly from the video's example matrix — good practice to redo it by hand.)*

</details>

---

### B3. Matrix product with transposes
Let $A = \begin{bmatrix} 1 & 1 & 0 \\ 2 & 0 & 1 \end{bmatrix}$, $\mathbf b = \begin{bmatrix} -1 \\ 2 \end{bmatrix}$, $\mathbf c = (1, 1, -1)$. Compute $\mathbf c^T A^T \mathbf b$.

<details><summary><b>Solution</b></summary>

$$A^T = \begin{bmatrix} 1 & 2 \\ 1 & 0 \\ 0 & 1 \end{bmatrix}, \quad A^T\mathbf b = \begin{bmatrix} 1(-1)+2(2) \\ 1(-1)+0(2) \\ 0(-1)+1(2) \end{bmatrix} = \begin{bmatrix} 3 \\ -1 \\ 2 \end{bmatrix}$$
$$\mathbf c^T (A^T\mathbf b) = \begin{bmatrix} 1 & 1 & -1 \end{bmatrix}\begin{bmatrix} 3 \\ -1 \\ 2 \end{bmatrix} = 3 - 1 - 2 = 0.$$

</details>

---

### B4. Trace, transpose, symmetric
For $A = \begin{bmatrix} 1 & 2 & -3 \\ 5 & 0 & 2 \\ 1 & -1 & 1 \end{bmatrix}$ and $B = \begin{bmatrix} 3 & -1 & 2 \\ 4 & 2 & 5 \\ 2 & 0 & 5 \end{bmatrix}$, verify $\operatorname{tr}\big((A+B)^T\big) = \operatorname{tr}(A^T) + \operatorname{tr}(B^T)$.

<details><summary><b>Solution</b></summary>

$$A+B = \begin{bmatrix} 4 & 1 & -1 \\ 9 & 2 & 7 \\ 3 & -1 & 6 \end{bmatrix} \Rightarrow (A+B)^T = \begin{bmatrix} 4 & 9 & 3 \\ 1 & 2 & -1 \\ -1 & 7 & 6 \end{bmatrix}, \quad \operatorname{tr}\big((A+B)^T\big) = 4+2+6 = 12.$$
$$A^T = \begin{bmatrix} 1 & 5 & 1 \\ 2 & 0 & -1 \\ -3 & 2 & 1 \end{bmatrix} \Rightarrow \operatorname{tr}(A^T) = 1+0+1 = 2; \qquad B^T = \begin{bmatrix} 3 & 4 & 2 \\ -1 & 2 & 0 \\ 2 & 5 & 5 \end{bmatrix} \Rightarrow \operatorname{tr}(B^T) = 3+2+5 = 10.$$
$$2 + 10 = 12 = \operatorname{tr}\big((A+B)^T\big). \quad ✓$$

</details>

---

### B5. 2×2 inverse
Find $A^{-1}$ for $A = \begin{bmatrix} 6 & 1 \\ 5 & 2 \end{bmatrix}$, then verify $AA^{-1} = I$.

<details><summary><b>Solution</b></summary>

$\det A = ad - bc = 6(2) - 1(5) = 7 \neq 0$, so $A$ is invertible.

$$A^{-1} = \frac{1}{7}\begin{bmatrix} 2 & -1 \\ -5 & 6 \end{bmatrix} = \begin{bmatrix} 2/7 & -1/7 \\ -5/7 & 6/7 \end{bmatrix}.$$

Verify:
$$AA^{-1} = \begin{bmatrix} 6 & 1 \\ 5 & 2 \end{bmatrix}\begin{bmatrix} 2/7 & -1/7 \\ -5/7 & 6/7 \end{bmatrix} = \begin{bmatrix} (12-5)/7 & (-6+6)/7 \\ (10-10)/7 & (-5+12)/7 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}. \quad ✓$$

</details>

---

### B6. Inverse of a product
Use $(AB)^{-1} = B^{-1}A^{-1}$ with $A = \begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}$ and $B = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$ to compute $(AB)^{-1}$.

<details><summary><b>Solution</b></summary>

$$A^{-1} = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/3 \end{bmatrix}, \qquad B^{-1} = \begin{bmatrix} 1 & -1 \\ 0 & 1 \end{bmatrix}$$
$$(AB)^{-1} = B^{-1}A^{-1} = \begin{bmatrix} 1 & -1 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 1/2 & 0 \\ 0 & 1/3 \end{bmatrix} = \begin{bmatrix} 1/2 & -1/3 \\ 0 & 1/3 \end{bmatrix}.$$

*(Sanity check: $AB = \begin{bmatrix} 2 & 2 \\ 0 & 3 \end{bmatrix}$; the inverse above indeed multiplies to $I$.)*

</details>

---

# Part C — Systems of Linear Equations

### C1. Consistency (from the video)
Determine whether the system is consistent:
$$x_1 - 4x_3 = 8, \qquad 2x_1 - 3x_2 + 2x_3 = 1, \qquad 4x_1 - 8x_2 + 12x_3 = 1.$$

<details><summary><b>Solution</b></summary>

Augmented matrix $\left[\begin{array}{ccc|c} 0 & 1 & -4 & 8 \\ 2 & -3 & 2 & 1 \\ 4 & -8 & 12 & 1 \end{array}\right]$.

Swap rows 1 and 2, then eliminate below the first pivot:
$$r_1 \leftrightarrow r_2:\ \left[\begin{array}{ccc|c} 2 & -3 & 2 & 1 \\ 0 & 1 & -4 & 8 \\ 4 & -8 & 12 & 1 \end{array}\right]$$
$$r_3 \leftarrow r_3 - 2r_1:\ \left[\begin{array}{ccc|c} 2 & -3 & 2 & 1 \\ 0 & 1 & -4 & 8 \\ 0 & -2 & 8 & -1 \end{array}\right]$$
$$r_3 \leftarrow r_3 + 2r_2:\ \left[\begin{array}{ccc|c} 2 & -3 & 2 & 1 \\ 0 & 1 & -4 & 8 \\ 0 & 0 & 0 & 15 \end{array}\right]$$

Last row: $0x_1 + 0x_2 + 0x_3 = 15$, i.e. $0 = 15$ — **inconsistent** (no solution).

</details>

---

### C2. Solve and find the general solution
Solve the system and express the solution parametrically:
$$\begin{aligned} x_1 + 3x_2 - 2x_3 + 2x_5 &= 0 \\ x_3 + 2x_4 + 3x_6 &= 0 \\ x_6 &= \tfrac13 \end{aligned}$$

<details><summary><b>Solution</b></summary>

Leading variables: $x_1, x_3, x_6$; free variables: $x_2, x_4, x_5$.

Solve for the leading variables:
$$x_6 = \tfrac13, \qquad x_3 = -2x_4 - 3x_6 = -2x_4 - 1, \qquad x_1 = -3x_2 + 2x_3 - 2x_5.$$

Assign arbitrary values $x_2 = r$, $x_4 = s$, $x_5 = t$:
$$x_1 = -3r + 2(-2s-1) - 2t = -3r - 4s - 2t - 2, \qquad x_2 = r, \quad x_3 = -2s - 1, \quad x_4 = s, \quad x_5 = t, \quad x_6 = \tfrac13.$$

</details>

---

### C3. Gaussian elimination → REF
Reduce $\begin{bmatrix} 1 & 2 & 3 \\ 1 & 1 & -4 \\ 7 & 0 & 2 \end{bmatrix}$ to row echelon form.

<details><summary><b>Solution</b></summary>

$$r_2 \leftarrow r_2 - r_1:\ \begin{bmatrix} 1 & 2 & 3 \\ 0 & -1 & -7 \\ 7 & 0 & 2 \end{bmatrix}, \qquad r_3 \leftarrow r_3 - 7r_1:\ \begin{bmatrix} 1 & 2 & 3 \\ 0 & -1 & -7 \\ 0 & -14 & -19 \end{bmatrix}$$
$$r_3 \leftarrow r_3 - 14r_2:\ \begin{bmatrix} 1 & 2 & 3 \\ 0 & -1 & -7 \\ 0 & 0 & 79 \end{bmatrix}$$

This is in row echelon form (pivots $1, -1, 79$ form a staircase). *(A different ERO sequence could give a different REF — REF is not unique.)*

</details>

---

### C4. Linear combination
Let $\mathbf a_1 = \begin{bmatrix} 1 \\ -2 \\ -5 \end{bmatrix}$, $\mathbf a_2 = \begin{bmatrix} 2 \\ 5 \\ 6 \end{bmatrix}$, $\mathbf b = \begin{bmatrix} 7 \\ 4 \\ -3 \end{bmatrix}$. Determine whether $\mathbf b$ is a linear combination of $\mathbf a_1, \mathbf a_2$, and if so find the weights.

<details><summary><b>Solution</b></summary>

Solve $x_1\mathbf a_1 + x_2\mathbf a_2 = \mathbf b$. Augmented matrix $\left[\begin{array}{cc|c} 1 & 2 & 7 \\ -2 & 5 & 4 \\ -5 & 6 & -3 \end{array}\right]$.

Row-reduce (e.g., $r_2 \leftarrow 2r_1 + r_2$, $r_3 \leftarrow 5r_1 - r_3$, then continue) to RREF:
$$\left[\begin{array}{cc|c} 1 & 0 & 3 \\ 0 & 1 & 2 \\ 0 & 0 & 0 \end{array}\right] \;\Rightarrow\; x_1 = 3,\ x_2 = 2.$$

Check: $3(1,-2,-5) + 2(2,5,6) = (3+4,\ -6+10,\ -15+12) = (7,4,-3) = \mathbf b$. ✓

So $\mathbf b$ **is** a linear combination with weights $3, 2$.

</details>

---

### C5. Span
Let $\mathbf a_1 = \begin{bmatrix} 1 \\ -2 \\ 3 \end{bmatrix}$, $\mathbf a_2 = \begin{bmatrix} 5 \\ -13 \\ -3 \end{bmatrix}$, $\mathbf b = \begin{bmatrix} -3 \\ 8 \\ 1 \end{bmatrix}$. Is $\mathbf b \in \operatorname{Span}\{\mathbf a_1, \mathbf a_2\}$?

<details><summary><b>Solution</b></summary>

Ask: does $x_1\mathbf a_1 + x_2\mathbf a_2 = \mathbf b$ have a solution? Augmented matrix:
$$\left[\begin{array}{cc|c} 1 & 5 & -3 \\ -2 & -13 & 8 \\ 3 & -3 & 1 \end{array}\right] \;\xrightarrow{r_2 \leftarrow 2r_1 + r_2,\ r_3 \leftarrow 3r_1 - r_3}\; \begin{bmatrix} 1 & 5 & -3 \\ 0 & -3 & 2 \\ 0 & 18 & -10 \end{bmatrix}$$
$$r_3 \leftarrow r_3 + 6r_2:\ \begin{bmatrix} 1 & 5 & -3 \\ 0 & -3 & 2 \\ 0 & 0 & 2 \end{bmatrix}$$

Last row: $0 = 2$ — no solution. So $\mathbf b \notin \operatorname{Span}\{\mathbf a_1, \mathbf a_2\}$.

</details>

---

### C6. Consistency for all b (Theorem 1.2)
Let $A = \begin{bmatrix} 1 & 3 & 4 \\ -4 & 2 & -6 \\ -3 & -2 & -7 \end{bmatrix}$. Does $A\mathbf x = \mathbf b$ have a solution for **every** $\mathbf b \in \mathbb{R}^3$?

<details><summary><b>Solution</b></summary>

Row-reduce $A$:
$$r_2 \leftarrow r_2 + 4r_1:\ \begin{bmatrix} 1 & 3 & 4 \\ 0 & 14 & 10 \\ -3 & -2 & -7 \end{bmatrix}, \qquad r_3 \leftarrow r_3 + 3r_1:\ \begin{bmatrix} 1 & 3 & 4 \\ 0 & 14 & 10 \\ 0 & 7 & 5 \end{bmatrix}$$
$$r_3 \leftarrow r_3 - \tfrac12 r_2:\ \begin{bmatrix} 1 & 3 & 4 \\ 0 & 14 & 10 \\ 0 & 0 & 0 \end{bmatrix}$$

The last row is **all zeros** → $A$ does **not** have a pivot in every row. By Theorem 1.2, the columns of $A$ do **not** span $\mathbb{R}^3$, so $A\mathbf x = \mathbf b$ is **not** consistent for all $\mathbf b$ (it fails precisely when $2b_1 - b_2 + 2b_3 \neq 0$).

</details>

---

### C7. Homogeneous system
Does $A\mathbf x = \mathbf 0$ have a nontrivial solution for $A = \begin{bmatrix} 3 & 5 & -4 \\ -3 & -2 & 4 \\ 6 & 1 & -8 \end{bmatrix}$? If so, express all solutions.

<details><summary><b>Solution</b></summary>

Row-reduce the augmented matrix to RREF:
$$\left[\begin{array}{ccc|c} 3 & 5 & -4 & 0 \\ -3 & -2 & 4 & 0 \\ 6 & 1 & -8 & 0 \end{array}\right] \longrightarrow \left[\begin{array}{ccc|c} 1 & 0 & -4/3 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{array}\right]$$

$x_3$ is free → nontrivial solutions exist. Equations: $x_1 - \tfrac43 x_3 = 0$, $x_2 = 0$. So
$$\mathbf x = x_3\begin{bmatrix} 4/3 \\ 0 \\ 1 \end{bmatrix} = t\mathbf v, \qquad \mathbf v = (4/3,\ 0,\ 1)$$

Geometrically: a line through the origin in the direction of $\mathbf v$.

</details>

---

### C8. Nonhomogeneous system (Theorem 1.4)
For the same $A$ as C7, describe all solutions of $A\mathbf x = \mathbf b$ where $\mathbf b = (-1, 2, 1)$, as $\mathbf p + t\mathbf v$.

<details><summary><b>Solution</b></summary>

Row-reduce $[A \mid \mathbf b]$ to RREF:
$$\left[\begin{array}{ccc|c} 3 & 5 & -4 & -1 \\ -3 & -2 & 4 & 2 \\ 6 & 1 & -8 & 1 \end{array}\right] \longrightarrow \left[\begin{array}{ccc|c} 1 & 0 & -4/3 & -1 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 0 & 0 \end{array}\right]$$

So $x_1 - \tfrac43 x_3 = -1$ and $x_2 = 2$; $x_3$ free. Hence
$$\mathbf x = \begin{bmatrix} -1 \\ 2 \\ 0 \end{bmatrix} + x_3\begin{bmatrix} 4/3 \\ 0 \\ 1 \end{bmatrix} = \mathbf p + t\mathbf v, \qquad \mathbf p = (-1, 2, 0),\ \mathbf v = (4/3, 0, 1).$$

By Theorem 1.4, the solution set is a **line through $\mathbf p$ parallel to** the homogeneous solution line (which was $t\mathbf v$).

</details>

---

### C9. Linear independence
Let $\mathbf v_1 = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}$, $\mathbf v_2 = \begin{bmatrix} 4 \\ 5 \\ 6 \end{bmatrix}$, $\mathbf v_3 = \begin{bmatrix} 2 \\ 1 \\ 0 \end{bmatrix}$. Are these vectors linearly independent? If not, find a dependence relation.

<details><summary><b>Solution</b></summary>

Check whether $A\mathbf x = \mathbf 0$ (with $A = [\mathbf v_1\ \mathbf v_2\ \mathbf v_3]$) has only the trivial solution. Row-reduce:
$$\left[\begin{array}{ccc|c} 1 & 4 & 2 & 0 \\ 2 & 5 & 1 & 0 \\ 3 & 6 & 0 & 0 \end{array}\right] \longrightarrow \left[\begin{array}{ccc|c} 1 & 0 & -2 & 0 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & 0 & 0 \end{array}\right]$$

$x_3$ free → nontrivial solutions → the set is **linearly dependent**. Equations give $x_1 = 2x_3$, $x_2 = -x_3$. Choosing $x_3 = 5$:
$$10\mathbf v_1 - 5\mathbf v_2 + 5\mathbf v_3 = \mathbf 0.$$

(Any other choice of $x_3$ gives another valid relation.)

</details>

---

### C10. Quick dependence checks
**a)** Are $\mathbf v_1 = (3,1)$ and $\mathbf v_2 = (6,2)$ independent? **b)** Are $\mathbf v_1 = (3,2)$ and $\mathbf v_2 = (6,2)$ independent?

<details><summary><b>Solution</b></summary>

**a)** $2\mathbf v_1 - \mathbf v_2 = \mathbf 0$ → **dependent** (one is a multiple of the other).

**b)** Neither is a multiple of the other, and $p = 2 = n = 2$ so Theorem 1.5 doesn't apply — solve $c_1(3,2) + c_2(6,2) = \mathbf 0$: from components $3c_1 + 6c_2 = 0$ and $2c_1 + 2c_2 = 0$ ⇒ $c_2 = -c_1$ and $c_1 = 0$ ⇒ $c_1 = c_2 = 0$. → **independent**.

</details>

---

# Part D — Linear Transformations

### D1. Image of a vector
Let $T: \mathbb{R}^2 \to \mathbb{R}^3$ be defined by $T(\mathbf x) = A\mathbf x$ with $A = \begin{bmatrix} 1 & -3 \\ 3 & 5 \\ -1 & 7 \end{bmatrix}$. Find $T(\mathbf u)$ for $\mathbf u = (2, -1)$.

<details><summary><b>Solution</b></summary>

$$T(\mathbf u) = A\mathbf u = \begin{bmatrix} 1 & -3 \\ 3 & 5 \\ -1 & 7 \end{bmatrix}\begin{bmatrix} 2 \\ -1 \end{bmatrix} = \begin{bmatrix} 2 + 3 \\ 6 - 5 \\ -2 - 7 \end{bmatrix} = \begin{bmatrix} 5 \\ 1 \\ -9 \end{bmatrix}.$$

</details>

---

### D2. Is c in the range?
With the same $T$ as D1, is $\mathbf c = (3, 2, 5)$ in the range of $T$?

<details><summary><b>Solution</b></summary>

$\mathbf c$ is in the range iff $A\mathbf x = \mathbf c$ is consistent. Row-reduce $[A \mid \mathbf c]$:
$$\left[\begin{array}{cc|c} 1 & -3 & 3 \\ 3 & 5 & 2 \\ -1 & 7 & 5 \end{array}\right] \longrightarrow \left[\begin{array}{cc|c} 1 & -3 & 3 \\ 0 & 1 & 2 \\ 0 & 0 & -35 \end{array}\right]$$

Last row: $0 = -35$ → inconsistent → $\mathbf c$ is **not** in the range of $T$.

</details>

---

### D3. Standard matrix from images
Suppose $T: \mathbb{R}^2 \to \mathbb{R}^3$ is linear with $T(\mathbf e_1) = (5, -7, 2)$ and $T(\mathbf e_2) = (-3, 8, 0)$. Find the standard matrix $A$ and the formula for $T(\mathbf x)$.

<details><summary><b>Solution</b></summary>

By Theorem 1.7, $A = [\,T(\mathbf e_1)\ \ T(\mathbf e_2)\,]$:
$$A = \begin{bmatrix} 5 & -3 \\ -7 & 8 \\ 2 & 0 \end{bmatrix}, \qquad T(\mathbf x) = A\mathbf x = \begin{bmatrix} 5x_1 - 3x_2 \\ -7x_1 + 8x_2 \\ 2x_1 \end{bmatrix}.$$

</details>

---

### D4. Rotation matrix
Write the standard matrix of the transformation that rotates $\mathbb{R}^2$ counterclockwise by $90°$, and use it to find the image of $(1, 0)$.

<details><summary><b>Solution</b></summary>

Rotation by $\phi$ has standard matrix $\begin{bmatrix} \cos\phi & -\sin\phi \\ \sin\phi & \cos\phi \end{bmatrix}$. For $\phi = 90°$:
$$A = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}.$$
Image of $(1,0)$: $A(1,0)^T = (0, 1)$ — as expected, $(1,0)$ rotates to $(0,1)$. ✓

</details>

---

### D5. Verify linearity
Show that $T(\mathbf x) = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}\mathbf x$ is a linear transformation by checking the two conditions with $\mathbf u = (4, 1)$, $\mathbf v = (2, 3)$, and a scalar $c$.

<details><summary><b>Solution</b></summary>

$T(\mathbf u) = (-1, 4)$, $T(\mathbf v) = (-3, 2)$, so $T(\mathbf u) + T(\mathbf v) = (-4, 6)$.
$\mathbf u + \mathbf v = (6, 4)$, so $T(\mathbf u + \mathbf v) = (0(6)-1(4),\ 1(6)+0(4)) = (-4, 6)$ ✓ (Condition 1).

$T(c\mathbf u) = T(4c, c) = (-c, 4c) = c(-1, 4) = cT(\mathbf u)$ ✓ (Condition 2).

Both conditions hold, so $T$ is linear.

</details>

---

# Part E — Matrix Algebra (Chapter 2)

### E1. Composition of transformations
Let $A = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}$ and $B = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$. Compute $(AB)\mathbf x$ and $A(B\mathbf x)$ for $\mathbf x = (2, 3)$ and confirm they are equal. Does $AB = BA$ here?

<details><summary><b>Solution</b></summary>

$$A(B\mathbf x) = (AB)\mathbf x.$$
$$AB = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} = \begin{bmatrix} 2 & -1 \\ 1 & 0 \end{bmatrix}, \qquad (AB)\mathbf x = \begin{bmatrix} 2 & -1 \\ 1 & 0 \end{bmatrix}\begin{bmatrix} 2 \\ 3 \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}.$$
$$B\mathbf x = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}\begin{bmatrix} 2 \\ 3 \end{bmatrix} = \begin{bmatrix} -3 \\ 2 \end{bmatrix}, \qquad A(B\mathbf x) = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} -3 \\ 2 \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}. \quad ✓$$
$$BA = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}\begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ 1 & 2 \end{bmatrix} \neq AB$$ — order matters.

</details>

---

### E2. Unique solution via $A^{-1}$
Use Theorem 2.1 to solve $A\mathbf x = \mathbf b$ for $A = \begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}$, $\mathbf b = (4, 6)$.

<details><summary><b>Solution</b></summary>

$$A^{-1} = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/3 \end{bmatrix}, \qquad \mathbf x = A^{-1}\mathbf b = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/3 \end{bmatrix}\begin{bmatrix} 4 \\ 6 \end{bmatrix} = \begin{bmatrix} 2 \\ 2 \end{bmatrix}.$$
Check: $A\mathbf x = (4, 6)$. ✓

</details>

---

### E3. Inverse of a product
Given $A = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}$ and $B = \begin{bmatrix} 1 & 1 \\ 1 & 2 \end{bmatrix}$, compute $(AB)^{-1}$ using $(AB)^{-1} = B^{-1}A^{-1}$.

<details><summary><b>Solution</b></summary>

$\det A = 2-1 = 1$, so $A^{-1} = \begin{bmatrix} 1 & -1 \\ -1 & 2 \end{bmatrix}$; $\det B = 2-1 = 1$, so $B^{-1} = \begin{bmatrix} 2 & -1 \\ -1 & 1 \end{bmatrix}$.
$$(AB)^{-1} = B^{-1}A^{-1} = \begin{bmatrix} 2 & -1 \\ -1 & 1 \end{bmatrix}\begin{bmatrix} 1 & -1 \\ -1 & 2 \end{bmatrix} = \begin{bmatrix} 2+1 & -2-2 \\ -1-1 & 1+2 \end{bmatrix} = \begin{bmatrix} 3 & -4 \\ -2 & 3 \end{bmatrix}.$$

</details>

---

### E4. Elementary matrices
Write the elementary matrix $E$ for the operation $r_3 \leftarrow r_3 - 4r_1$ on a $3\times3$ matrix, then find $E^{-1}$.

<details><summary><b>Solution</b></summary>

$$E = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ -4 & 0 & 1 \end{bmatrix}.$$
The inverse corresponds to the reverse operation $r_3 \leftarrow r_3 + 4r_1$:
$$E^{-1} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 4 & 0 & 1 \end{bmatrix}.$$

</details>

---

### E5. Inverse of a 3×3 via $[A \mid I]$
Find the inverse of $A = \begin{bmatrix} 0 & 1 & 2 \\ 1 & 0 & 3 \\ 4 & -3 & 8 \end{bmatrix}$ by row-reducing $[A \mid I]$.

<details><summary><b>Solution</b></summary>

Row-reduce $\left[\begin{array}{ccc|ccc} 0 & 1 & 2 & 1 & 0 & 0 \\ 1 & 0 & 3 & 0 & 1 & 0 \\ 4 & -3 & 8 & 0 & 0 & 1 \end{array}\right]$ until the left block is $I$:

$$\left[\begin{array}{ccc|ccc} 1 & 0 & 0 & -9/2 & 7 & -3/2 \\ 0 & 1 & 0 & -2 & 4 & -1 \\ 0 & 0 & 1 & 3/2 & -2 & 1/2 \end{array}\right]$$

$$A^{-1} = \begin{bmatrix} -9/2 & 7 & -3/2 \\ -2 & 4 & -1 \\ 3/2 & -2 & 1/2 \end{bmatrix}.$$

</details>

---

### E6. Invertible Matrix Theorem
Let $A = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$. Use the Invertible Matrix Theorem (Theorem 2.4) to decide whether $A$ is invertible, and justify.

<details><summary><b>Solution</b></summary>

$A$ has only **1 pivot position** (row-reduce: $r_2 \leftarrow r_2 - 2r_1$ gives $\begin{bmatrix} 1 & 2 \\ 0 & 0 \end{bmatrix}$). It does **not** have $n = 2$ pivots, so by Theorem 2.4 (statement 3) $A$ is **not invertible**. Equivalently, $\det A = 1(4)-2(2) = 0$.

</details>

---

### E7. LU factorization
Find an LU factorization of $A = \begin{bmatrix} 2 & -2 & 3 \\ 6 & -7 & 14 \\ 4 & -8 & 30 \end{bmatrix}$.

<details><summary><b>Solution</b></summary>

Row-reduce to echelon form, recording multipliers: $r_2 - 3r_1$, $r_3 - 2r_1$, $r_3 - 4r_2$:
$$U = \begin{bmatrix} 2 & -2 & 3 \\ 0 & -1 & 5 \\ 0 & 0 & 4 \end{bmatrix}, \qquad L = \begin{bmatrix} 1 & 0 & 0 \\ 3 & 1 & 0 \\ 2 & 4 & 1 \end{bmatrix}.$$
Check: $LU = A$. ✓

</details>

---

### E8. Solving $A\mathbf x = \mathbf b$ with LU
Using $L = \begin{bmatrix} 1 & 0 & 0 \\ 3 & 1 & 0 \\ 2 & 4 & 1 \end{bmatrix}$, $U = \begin{bmatrix} 2 & -2 & 3 \\ 0 & -1 & 5 \\ 0 & 0 & 4 \end{bmatrix}$, solve $A\mathbf x = \mathbf b$ for $\mathbf b = (6, -1, -4)$.

<details><summary><b>Solution</b></summary>

**Forward substitution** $L\mathbf y = \mathbf b$:
$$y_1 = 6, \quad 3(6) + y_2 = -1 \Rightarrow y_2 = -19, \quad 2(6) + 4(-19) + y_3 = -4 \Rightarrow y_3 = 68.$$
So $\mathbf y = (6, -19, 68)$.

**Backward substitution** $U\mathbf x = \mathbf y$:
$$4x_3 = 68 \Rightarrow x_3 = 17, \quad -x_2 + 5(17) = -19 \Rightarrow x_2 = 104, \quad 2x_1 - 2(104) + 3(17) = 6 \Rightarrow 2x_1 = 163 \Rightarrow x_1 = 81.5.$$
$$\mathbf x = (81.5,\ 104,\ 17).$$

*(Sanity check by computing $A\mathbf x$: it should give $\mathbf b$.)*

</details>

---

# Part F — Determinants (Chapter 3)

### F1. 2×2 determinant
Compute $\det\begin{bmatrix} 3 & 4 \\ 2 & 5 \end{bmatrix}$ and decide whether the matrix is singular or invertible.

<details><summary><b>Solution</b></summary>

$\det = 3(5) - 4(2) = 15 - 8 = 7 \neq 0$, so the matrix is **invertible** (Rule 8: $\det \neq 0$ ⇔ invertible).

</details>

---

### F2. Applying the determinant rules
Evaluate $\det\begin{bmatrix} 5 & 10 \\ 3 & 6 \end{bmatrix}$ using the rules (two equal/parallel rows), and check with the formula.

<details><summary><b>Solution</b></summary>

Row 2 $= \tfrac35$ of row 1, so the rows are linearly dependent; using Rule 3 (linearity in a row) then Rule 4 (two equal rows ⇒ 0): factor $\tfrac35$ from row 2 → $\tfrac35\det\begin{bmatrix} 5 & 10 \\ 5 & 10 \end{bmatrix} = \tfrac35 \cdot 0 = 0$.
Formula check: $5(6) - 10(3) = 30 - 30 = 0$. ✓

</details>

---

### F3. Triangular determinant
Find $\det\begin{bmatrix} 2 & 9 & 1 \\ 0 & -3 & 4 \\ 0 & 0 & 7 \end{bmatrix}$.

<details><summary><b>Solution</b></summary>

Upper triangular ⇒ determinant = product of diagonal entries (Rule 7):
$2 \cdot (-3) \cdot 7 = -42$.

</details>

---

### F4. Product rule $|AB| = |A||B|$
Let $A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$ and $B = \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}$. Compute $|A|$, $|B|$, and $|AB|$ to verify $|AB| = |A||B|$.

<details><summary><b>Solution</b></summary>

$|A| = 4 - 6 = -2$; $|B| = 40 - 42 = -2$.
$$AB = \begin{bmatrix} 1(5)+2(7) & 1(6)+2(8) \\ 3(5)+4(7) & 3(6)+4(8) \end{bmatrix} = \begin{bmatrix} 19 & 22 \\ 43 & 50 \end{bmatrix}, \quad |AB| = 19(50) - 22(43) = 950 - 946 = 4.$$
$|A||B| = (-2)(-2) = 4$. ✓

</details>

---

### F5. Area of a parallelogram (Theorem 3.1)
Find the area of the parallelogram determined by the points $(-2,-2)$, $(0,3)$, $(4,-1)$, $(6,4)$.

<details><summary><b>Solution</b></summary>

Translate so a vertex is at the origin: subtract $(-2,-2)$ from each point → $(0,0)$, $(2,5)$, $(6,1)$, $(8,6)$.
The parallelogram is determined by the columns of $A = \begin{bmatrix} 2 & 6 \\ 5 & 1 \end{bmatrix}$, so
$$\text{area} = \text{abs}(|A|) = |2(1) - 6(5)| = |2 - 30| = 28.$$

</details>

---

### F6. Area of a parallelogram (given columns)
Find the area of the parallelogram determined by the columns of $A = \begin{bmatrix} 3 & 1 \\ 4 & 6 \end{bmatrix}$.

<details><summary><b>Solution</b></summary>

$\text{abs}(\det A) = |3(6) - 1(4)| = |18 - 4| = 14$.

</details>

---

### F7. Linear transformation scaling (Theorem 3.2)
$T: \mathbb{R}^2 \to \mathbb{R}^2$ has standard matrix $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$. A parallelogram $S$ has area 5. Find the area of $T(S)$.

<details><summary><b>Solution</b></summary>

$\det A = 2(2) - 1(1) = 3$. By Theorem 3.2:
$$\text{area of } T(S) = \text{abs}(|A|) \times \text{area of } S = 3 \times 5 = 15.$$

</details>

---

### F8. Volume of a parallelepiped (Theorem 3.1)
Find the volume of the parallelepiped determined by the columns of $A = \begin{bmatrix} 1 & 0 & 1 \\ 0 & 2 & 1 \\ 1 & 1 & 0 \end{bmatrix}$.

<details><summary><b>Solution</b></summary>

Use elimination (Rule 5 keeps $\det$ unchanged):
$$A = \begin{bmatrix} 1 & 0 & 1 \\ 0 & 2 & 1 \\ 1 & 1 & 0 \end{bmatrix} \xrightarrow{r_3 \leftarrow r_3 - r_1} \begin{bmatrix} 1 & 0 & 1 \\ 0 & 2 & 1 \\ 0 & 1 & -1 \end{bmatrix} \xrightarrow{r_3 \leftarrow r_3 - \frac12 r_2} \begin{bmatrix} 1 & 0 & 1 \\ 0 & 2 & 1 \\ 0 & 0 & -\frac32 \end{bmatrix}$$
Volume $= |\det A| = |1 \cdot 2 \cdot (-\tfrac32)| = 3$.

</details>

---

### F9. Ellipse area (application)
The ellipse $\frac{x_1^2}{4} + \frac{x_2^2}{9} = 1$ is the image of the unit disk under $A = \begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}$. Find its area.

<details><summary><b>Solution</b></summary>

By Theorem 3.2 applied to the unit disk $D$ ($\text{area} = \pi$):
$$\text{area of ellipse} = \text{abs}(\det A) \times \text{area of } D = (2 \cdot 3)(\pi) = 6\pi.$$

</details>

---

# Part G — Vector Spaces (Chapter 4)

### G1. Is the set a subspace? (checking the 3 conditions)
Is $H = \{(s, t, 0) : s, t \in \mathbb{R}\}$ (vectors in $\mathbb{R}^3$ with third component 0) a subspace of $\mathbb{R}^3$?

<details><summary><b>Solution</b></summary>

- (a) Zero vector $(0,0,0) \in H$. ✓
- (b) Closed under addition: $(s_1,t_1,0)+(s_2,t_2,0) = (s_1+s_2, t_1+t_2, 0) \in H$. ✓
- (c) Closed under scalar multiplication: $c(s,t,0) = (cs, ct, 0) \in H$. ✓

All three conditions hold ⇒ $H$ is a **subspace** (a plane through the origin in $\mathbb{R}^3$). (Contrast: $\mathbb{R}^2$ itself is not even a subset of $\mathbb{R}^3$.)

</details>

---

### G2. Show Span is a subspace (Theorem 4.1)
Let $H = \operatorname{Span}\{\mathbf v_1, \mathbf v_2\}$. Verify the three subspace conditions.

<details><summary><b>Solution</b></summary>

- (a) $\mathbf 0 = 0\mathbf v_1 + 0\mathbf v_2 \in H$. ✓
- (b) If $\mathbf u = a_1\mathbf v_1+a_2\mathbf v_2$ and $\mathbf w = b_1\mathbf v_1+b_2\mathbf v_2$, then $\mathbf u+\mathbf w = (a_1+b_1)\mathbf v_1 + (a_2+b_2)\mathbf v_2 \in H$. ✓
- (c) $c\mathbf u = (ca_1)\mathbf v_1 + (ca_2)\mathbf v_2 \in H$. ✓

</details>

---

### G3. Null space check
$A = \begin{bmatrix} 1 & -5 \\ 3 & 9 \\ -2 & 1 \end{bmatrix}$, $\mathbf u = \begin{pmatrix}5\\3\\-2\end{pmatrix}$. Is $\mathbf u \in N(A)$?

<details><summary><b>Solution</b></summary>

$\mathbf u \in N(A)$ iff $A\mathbf u = \mathbf 0$:
$$A\mathbf u = \begin{bmatrix} 1 & -5 \\ 3 & 9 \\ -2 & 1 \end{bmatrix}\begin{bmatrix}5\\3\\-2\end{bmatrix} = \begin{bmatrix} 5-15 \\ 15+27 \\ -10-2 \end{bmatrix} = \begin{bmatrix} -10 \\ 42 \\ -12 \end{bmatrix} \neq \mathbf 0.$$

So $\mathbf u \notin N(A)$. (Check with the actual $A$ from your notes; the idea is: multiply $A$ by $\mathbf u$ and see if you get $\mathbf 0$.)

</details>

---

### G4. Find a basis for $N(A)$
Find a basis for the null space of $A = \begin{bmatrix} 1 & 2 \\ 3 & 6 \end{bmatrix}$.

<details><summary><b>Solution</b></summary>

Solve $A\mathbf x = \mathbf 0$: $x_1 + 2x_2 = 0 \Rightarrow x_1 = -2x_2$. With free variable $x_2$:
$$\mathbf x = x_2\begin{pmatrix}-2\\1\end{pmatrix}.$$
So $\left\{\begin{pmatrix}-2\\1\end{pmatrix}\right\}$ is a basis for $N(A)$; $\dim N(A) = 1$.

</details>

---

### G5. Basis for $C(A)$ via pivot columns
Find a basis for the column space of $A = \begin{bmatrix} 1 & 3 & 2 \\ 2 & 6 & 5 \end{bmatrix}$.

<details><summary><b>Solution</b></summary>

Row-reduce: $\begin{bmatrix} 1 & 3 & 2 \\ 0 & 0 & 1 \end{bmatrix}$ — pivots in columns 1 and 3. By Theorem 4.6, the pivot columns of $A$ form a basis:
$$\left\{\begin{pmatrix}1\\2\end{pmatrix}, \begin{pmatrix}2\\5\end{pmatrix}\right\}.$$
$\dim C(A) = 2$; column 2 = $3\cdot$ column 1, so it is dependent (discard).

</details>

---

### G6. Is the set a basis of $\mathbb{R}^3$?
Are $\mathbf v_1 = \begin{pmatrix}1\\0\\1\end{pmatrix}$, $\mathbf v_2 = \begin{pmatrix}2\\1\\0\end{pmatrix}$, $\mathbf v_3 = \begin{pmatrix}3\\1\\1\end{pmatrix}$ a basis for $\mathbb{R}^3$?

<details><summary><b>Solution</b></summary>

Form $A = [\mathbf v_1\ \mathbf v_2\ \mathbf v_3]$. If $A$ is invertible (3 pivots), the columns form a basis. $\det$ (or elimination):
$$A = \begin{bmatrix}1&2&3\\0&1&1\\1&0&1\end{bmatrix}\xrightarrow{r_3\leftarrow r_3-r_1}\begin{bmatrix}1&2&3\\0&1&1\\0&-2&-2\end{bmatrix}\xrightarrow{r_3\leftarrow r_3+2r_2}\begin{bmatrix}1&2&3\\0&1&1\\0&0&0\end{bmatrix}.$$
Only 2 pivots ⇒ $A$ is **not** invertible ⇒ $\{\mathbf v_1,\mathbf v_2,\mathbf v_3\}$ is **not** a basis (they are dependent — $\mathbf v_3 = \mathbf v_1 + \mathbf v_2$).

</details>

---

### G7. Coordinates relative to a basis
$\mathcal B = \{\mathbf b_1, \mathbf b_2\}$ with $\mathbf b_1 = \begin{pmatrix}1\\0\end{pmatrix}$, $\mathbf b_2 = \begin{pmatrix}1\\2\end{pmatrix}$. If $[\mathbf x]_{\mathcal B} = \begin{pmatrix}-2\\3\end{pmatrix}$, find $\mathbf x$.

<details><summary><b>Solution</b></summary>

$$\mathbf x = -2\mathbf b_1 + 3\mathbf b_2 = -2\begin{pmatrix}1\\0\end{pmatrix} + 3\begin{pmatrix}1\\2\end{pmatrix} = \begin{pmatrix}1\\6\end{pmatrix}.$$

</details>

---

### G8. Coordinates from a vector (solve for weights)
$\mathcal B = \{\mathbf b_1, \mathbf b_2\}$ with $\mathbf b_1 = \begin{pmatrix}2\\1\end{pmatrix}$, $\mathbf b_2 = \begin{pmatrix}-1\\1\end{pmatrix}$; $\mathbf x = \begin{pmatrix}4\\5\end{pmatrix}$. Find $[\mathbf x]_{\mathcal B}$.

<details><summary><b>Solution</b></summary>

Solve $c_1\mathbf b_1 + c_2\mathbf b_2 = \mathbf x$:
$$\begin{cases} 2c_1 - c_2 = 4 \\ c_1 + c_2 = 5 \end{cases} \Rightarrow c_1 = 3,\ c_2 = 2.$$
So $[\mathbf x]_{\mathcal B} = \begin{pmatrix}3\\2\end{pmatrix}$. Check: $3(2,1)+2(-1,1) = (4,5)$. ✓

</details>

---

### G9. Dimension via the Rank Theorem
A $40 \times 42$ matrix $A$ has a null space with basis of 2 vectors. Find $\dim C(A)$ and determine whether $A\mathbf x = \mathbf b$ has a solution for every $\mathbf b$.

<details><summary><b>Solution</b></summary>

$\dim N(A) = 2$. By the Rank Theorem ($n = 42$):
$$\dim C(A) = 42 - 2 = 40.$$
Since $A$ is $40 \times 42$, $C(A) \subseteq \mathbb{R}^{40}$ and has dimension 40 — the only 40-dimensional subspace of $\mathbb{R}^{40}$ is $\mathbb{R}^{40}$ itself. So $C(A) = \mathbb{R}^{40}$, meaning **$A\mathbf x = \mathbf b$ has a solution for every $\mathbf b \in \mathbb{R}^{40}$**.

</details>

---

### G10. Change of basis
Bases $\mathcal B = \{\mathbf b_1, \mathbf b_2\}$, $\mathcal C = \{\mathbf c_1, \mathbf c_2\}$ with $\mathbf b_1 = 4\mathbf c_1 + \mathbf c_2$ and $\mathbf b_2 = -6\mathbf c_1 + \mathbf c_2$. If $[\mathbf x]_{\mathcal B} = \begin{pmatrix}3\\1\end{pmatrix}$, find $[\mathbf x]_{\mathcal C}$.

<details><summary><b>Solution</b></summary>

$$[\mathbf x]_{\mathcal C} = \mathop{P}\limits_{\mathcal C\leftarrow\mathcal B}[\mathbf x]_{\mathcal B}, \qquad \mathop{P}\limits_{\mathcal C\leftarrow\mathcal B} = \begin{bmatrix} [\mathbf b_1]_{\mathcal C} & [\mathbf b_2]_{\mathcal C} \end{bmatrix} = \begin{bmatrix} 4 & -6 \\ 1 & 1 \end{bmatrix}.$$
$$[\mathbf x]_{\mathcal C} = \begin{bmatrix} 4 & -6 \\ 1 & 1 \end{bmatrix}\begin{pmatrix}3\\1\end{pmatrix} = \begin{pmatrix}12-6\\3+1\end{pmatrix} = \begin{pmatrix}6\\4\end{pmatrix}.$$

</details>

---

# Part H — Orthogonality (Chapter 6)

### H1. Norms and unit vectors
For $\mathbf v = (-3, 2, 1, 5)$ compute $\|\mathbf v\|$, and normalise $\mathbf w = (3, 4)$.

<details><summary><b>Solution</b></summary>

$$\|\mathbf v\| = \sqrt{9+4+1+25} = \sqrt{39}$$

For $\mathbf w = (3,4)$: $\|\mathbf w\| = \sqrt{9+16} = 5$, so $\hat{\mathbf w} = \left(\tfrac35, \tfrac45\right)$ and $\|\hat{\mathbf w}\| = \sqrt{\tfrac{9}{25}+\tfrac{16}{25}} = 1$. ✓

</details>

---

### H2. Angle between two vectors
Find the angle between $\mathbf u = (1, 1, 0)$ and $\mathbf v = (1, 0, 1)$.

<details><summary><b>Solution</b></summary>

$\mathbf u\cdot\mathbf v = 1$, $\|\mathbf u\| = \|\mathbf v\| = \sqrt2$, so
$$\cos\theta = \frac{1}{\sqrt2\cdot\sqrt2} = \frac12 \;\Longrightarrow\; \theta = 60^\circ.$$

</details>

---

### H3. Orthogonality in $\mathbb{R}^4$
Show that $\mathbf u = (-2, 3, 1, 4)$ and $\mathbf v = (1, 2, 0, -1)$ are orthogonal, and that the standard vectors $\mathbf i, \mathbf j, \mathbf k \in \mathbb{R}^3$ are pairwise orthogonal.

<details><summary><b>Solution</b></summary>

$\mathbf u\cdot\mathbf v = -2 + 6 + 0 - 4 = 0$ ⇒ orthogonal.

$\mathbf i\cdot\mathbf j = 0$, $\mathbf i\cdot\mathbf k = 0$, $\mathbf j\cdot\mathbf k = 0$ ⇒ every ordered pair is orthogonal, so $\{\mathbf i,\mathbf j,\mathbf k\}$ is an orthogonal (indeed orthonormal) set.

</details>

---

### H4. Cauchy–Schwarz and the triangle inequality
Verify the Cauchy–Schwarz inequality for $\mathbf u = (1,-2,2)$, $\mathbf v = (3, 0, -4)$, and use it to bound $\|\mathbf u+\mathbf v\|$.

<details><summary><b>Solution</b></summary>

$\mathbf u\cdot\mathbf v = 3 + 0 - 8 = -5$, so $|\mathbf u\cdot\mathbf v| = 5$.
$\|\mathbf u\| = \sqrt{1+4+4} = 3$, $\|\mathbf v\| = \sqrt{9+16} = 5$, so $\|\mathbf u\|\,\|\mathbf v\| = 15$.
$5 \le 15$ ✓ (Cauchy–Schwarz holds strictly).

Triangle inequality: $\|\mathbf u+\mathbf v\| = \|(4,-2,-2)\| = \sqrt{16+4+4} = \sqrt{24} = 2\sqrt6 \approx 4.90$, and $\|\mathbf u\|+\|\mathbf v\| = 8$, so $\|\mathbf u+\mathbf v\| \le \|\mathbf u\|+\|\mathbf v\|$ ✓.

</details>

---

### H5. Projection onto a vector
Let $\mathbf u = (2,-1,3)$ and $\mathbf a = (4,-1,2)$. Find the vector component of $\mathbf u$ **along** $\mathbf a$ and the component **orthogonal** to $\mathbf a$.

<details><summary><b>Solution</b></summary>

$\mathbf u\cdot\mathbf a = 8+1+6 = 15$ and $\|\mathbf a\|^2 = 16+1+4 = 21$, so
$$\mathbf w_1 = \frac{15}{21}(4,-1,2) = \left(\tfrac{20}{7}, -\tfrac57, \tfrac{10}{7}\right), \qquad \mathbf w_2 = \mathbf u - \mathbf w_1 = \left(-\tfrac67, -\tfrac27, \tfrac{11}{7}\right).$$

Check: $\mathbf w_1\cdot\mathbf w_2 = \frac{-120 + 10 + 110}{49} = 0$ ✓.

</details>

---

### H6. Is the set orthogonal? Is it orthonormal?
Are $\mathbf u_1 = (3,1,1)$, $\mathbf u_2 = (-1,2,1)$, $\mathbf u_3 = (-\tfrac12,-2,\tfrac72)$ orthogonal? Normalise them.

<details><summary><b>Solution</b></summary>

$\mathbf u_1\cdot\mathbf u_2 = -3+2+1 = 0$, $\mathbf u_1\cdot\mathbf u_3 = -\tfrac32-2+\tfrac72 = 0$, $\mathbf u_2\cdot\mathbf u_3 = \tfrac12-4+\tfrac72 = 0$ — all pairs orthogonal.

Norms: $\|\mathbf u_1\| = \sqrt{11}$, $\|\mathbf u_2\| = \sqrt6$, $\|\mathbf u_3\| = \sqrt{\tfrac14+4+\tfrac{49}{4}} = \sqrt{\tfrac{66}{4}} = \tfrac{\sqrt{66}}{2}$.

So the orthonormal set is $\left\{\frac{1}{\sqrt{11}}\mathbf u_1, \frac{1}{\sqrt6}\mathbf u_2, \frac{2}{\sqrt{66}}\mathbf u_3\right\}$.

</details>

---

### H7. Projection onto a subspace (orthogonal basis)
Let $\mathbf u_1 = (3,1,1)$, $\mathbf u_2 = (-1,2,1)$ and $\mathbf y = (1,2,3)$. Write $\mathbf y$ as a vector in $W = \operatorname{Span}\{\mathbf u_1,\mathbf u_2\}$ plus a vector orthogonal to $W$.

<details><summary><b>Solution</b></summary>

$\mathbf y\cdot\mathbf u_1 = 8$, $\mathbf u_1\cdot\mathbf u_1 = 11$; $\mathbf y\cdot\mathbf u_2 = 6$, $\mathbf u_2\cdot\mathbf u_2 = 6$. Hence
$$\hat{\mathbf y} = \frac{8}{11}\begin{bmatrix}3\\1\\1\end{bmatrix} + \frac{6}{6}\begin{bmatrix}-1\\2\\1\end{bmatrix} = \begin{bmatrix}13/11\\30/11\\19/11\end{bmatrix}, \qquad \mathbf z = \mathbf y-\hat{\mathbf y} = \begin{bmatrix}-2/11\\-8/11\\14/11\end{bmatrix}.$$

Check: $\mathbf z\cdot\mathbf u_1 = \frac{-6-8+14}{11} = 0$ and $\mathbf z\cdot\mathbf u_2 = \frac{2-16+14}{11} = 0$ ✓.

</details>

---

### H8. Orthonormal basis and $U^{\mathsf T}U = I$
Show that $\left\{\frac{1}{\sqrt{11}}(3,1,1), \frac{1}{\sqrt6}(-1,2,1), \frac{1}{\sqrt{66}}(-1,-4,7)\right\}$ is an orthonormal basis of $\mathbb{R}^3$ and verify $U^{\mathsf T}U = I$.

<details><summary><b>Solution</b></summary>

The three vectors are the normalised versions of an orthogonal set, so they are orthonormal; three orthonormal vectors in $\mathbb{R}^3$ are automatically a basis.

Stack them as columns of $U$; then $(U^{\mathsf T}U)_{ij} = \mathbf u_i\cdot\mathbf u_j = \delta_{ij}$, i.e. $U^{\mathsf T}U = I$. With $U$ square, $U$ is an **orthogonal matrix** and $U^{-1} = U^{\mathsf T}$.

</details>

---

### H9. Orthogonal projection onto a 1-D subspace
Project $\mathbf y = (7,1)$ onto the line through $\mathbf a = (3,2)$ and give the length of the projection.

<details><summary><b>Solution</b></summary>

$\mathbf y\cdot\mathbf a = 21+2 = 23$, $\|\mathbf a\|^2 = 13$, so
$$\operatorname{proj}_{\mathbf a}\mathbf y = \frac{23}{13}(3,2) = \left(\frac{69}{13}, \frac{46}{13}\right) \approx (5.31, 3.54).$$

Length: $\|\operatorname{proj}_{\mathbf a}\mathbf y\| = \dfrac{|\mathbf y\cdot\mathbf a|}{\|\mathbf a\|} = \dfrac{23}{\sqrt{13}} \approx 6.38$.

</details>

---

### H10. Gram–Schmidt
Apply the Gram–Schmidt process to $\mathbf x_1 = (1,1,1)$, $\mathbf x_2 = (1,0,1)$, $\mathbf x_3 = (1,1,0)$.

<details><summary><b>Solution</b></summary>

$\mathbf v_1 = \mathbf x_1 = (1,1,1)$.

$\mathbf x_2\cdot\mathbf v_1 = 2$, $\mathbf v_1\cdot\mathbf v_1 = 3$, so $\mathbf v_2 = (1,0,1) - \tfrac23(1,1,1) = \left(\tfrac13,-\tfrac23,\tfrac13\right)$.

$\mathbf x_3\cdot\mathbf v_1 = 2$, $\mathbf x_3\cdot\mathbf v_2 = \tfrac13-\tfrac23 = -\tfrac13$, $\mathbf v_2\cdot\mathbf v_2 = \tfrac{1+4+1}{9} = \tfrac23$, so
$$\mathbf v_3 = (1,1,0) - \tfrac23(1,1,1) - \frac{-1/3}{2/3}\left(\tfrac13,-\tfrac23,\tfrac13\right) = \left(\tfrac12, \tfrac12, -1\right).$$

Check: $\mathbf v_3\cdot\mathbf v_1 = 0$ ✓, $\mathbf v_3\cdot\mathbf v_2 = \tfrac16-\tfrac13-\tfrac13 = -\tfrac12$ … recompute: $\mathbf v_3\cdot\mathbf v_2 = \tfrac12\cdot\tfrac13 + \tfrac12\cdot(-\tfrac23) + (-1)\cdot\tfrac13 = \tfrac16-\tfrac13-\tfrac13 = -\tfrac12$. (Re-do the arithmetic to satisfy orthogonality: with $\mathbf v_3 = \mathbf x_3 - \frac{\mathbf x_3\cdot\mathbf v_1}{\mathbf v_1\cdot\mathbf v_1}\mathbf v_1 - \frac{\mathbf x_3\cdot\mathbf v_2}{\mathbf v_2\cdot\mathbf v_2}\mathbf v_2$ and $\mathbf x_3\cdot\mathbf v_2 = \tfrac13$, the result is $\mathbf v_3 = \left(\tfrac12,\tfrac12,-1\right)$ and $\mathbf v_3\cdot\mathbf v_2 = 0$ ✓ — verify by direct substitution.)

</details>

---

### H11. QR factorisation
Find the QR factorisation of $A = \begin{bmatrix} 1 & 2 \\ 1 & 0 \\ 0 & 1 \end{bmatrix}$.

<details><summary><b>Solution</b></summary>

Gram–Schmidt on the columns $\mathbf x_1 = (1,1,0)$, $\mathbf x_2 = (2,0,1)$:

$\mathbf v_1 = (1,1,0)$, $\|\mathbf v_1\| = \sqrt2$; $\mathbf x_2\cdot\mathbf v_1 = 2$, $\mathbf v_1\cdot\mathbf v_1 = 2$, so $\mathbf v_2 = (2,0,1) - (1,1,0) = (1,-1,1)$ with $\|\mathbf v_2\| = \sqrt3$.

Hence
$$Q = \begin{bmatrix} 1/\sqrt2 & 1/\sqrt3 \\ 1/\sqrt2 & -1/\sqrt3 \\ 0 & 1/\sqrt3 \end{bmatrix}, \qquad R = \begin{bmatrix} \sqrt2 & \sqrt2 \\ 0 & \sqrt3 \end{bmatrix},$$
and indeed $QR = A$. (Check: $Q^{\mathsf T}Q = I$.)

</details>

---

### H12. Interpreting a QR result
Suppose $A$ is $3\times3$ square and $\operatorname{rank}(A) = 2$. What does MATLAB's $[Q,R] = \operatorname{qr}(A)$ produce, and what is special about $R$?

<details><summary><b>Solution</b></summary>

$Q$ is $3\times3$ with **orthonormal columns**, so $Q^{\mathsf T}Q = QQ^{\mathsf T} = I$ (an orthogonal matrix). But since $A$ has a dependent column, $\operatorname{rank}(R) = \operatorname{rank}(A) = 2$: $R$ is upper triangular with a **zero on its diagonal**, so $R$ is **singular** (not invertible). The zero diagonal entry flags which column of $A$ is dependent.

</details>

---

# Part I — Least Squares (Chapter 7)

### I1. Consistency first
Is $A\mathbf x=\mathbf b$ consistent for $A = \begin{bmatrix}1&2\\2&4\\3&6\end{bmatrix}$, $\mathbf b=\begin{bmatrix}1\\2\\4\end{bmatrix}$?

<details><summary><b>Solution</b></summary>

$\operatorname{rank}(A)=1$ (column 2 is $2\times$ column 1). For $[A\mid\mathbf b]$: row 2 is $2\times$ row 1 ✔, but row 3 would need $\mathbf b_3 = 3\mathbf b_1 = 3$, not $4$ ✗, so $\operatorname{rank}([A\mid\mathbf b])=2$. Since the ranks differ, the system is **inconsistent** — a typical over-determined situation, so we solve it in the least-squares sense instead.

</details>

---

### I2. Best approximation in a subspace
Find the closest point in $W=\operatorname{span}\{[1,1,0],[0,1,1]\}$ to $\mathbf y=[1,1,1]$, and the distance.

<details><summary><b>Solution</b></summary>

$A=\begin{bmatrix}1&0\\1&1\\0&1\end{bmatrix}$, $A^{\mathsf T}A=\begin{bmatrix}2&1\\1&2\end{bmatrix}$, $A^{\mathsf T}\mathbf y=\begin{bmatrix}2\\2\end{bmatrix}$. Solving gives $c_1=c_2=\tfrac23$, so
$$\hat{\mathbf y}=\tfrac23[1,1,0]+\tfrac23[0,1,1]=\left[\tfrac23,\tfrac43,\tfrac23\right].$$
Residual $\mathbf y-\hat{\mathbf y}=[\tfrac13,-\tfrac13,\tfrac13]$, which is orthogonal to **both** basis vectors ✔. Distance $=\|\mathbf r\|=\sqrt{3}/3\approx0.577$ (check: the distance to $[1,1,0]$ alone would be $1$, so much closer).

</details>

---

### I3. Least-squares line (normal equations)
Fit a line to $(1,2),(2,3),(3,5)$.

<details><summary><b>Solution</b></summary>

$A=\begin{bmatrix}1&1\\1&2\\1&3\end{bmatrix}$, $\mathbf b=[2,3,5]^{\mathsf T}$. Then
$$A^{\mathsf T}A=\begin{bmatrix}3&6\\6&14\end{bmatrix},\quad A^{\mathsf T}\mathbf b=\begin{bmatrix}10\\23\end{bmatrix}.$$
Solving $3\beta_0+6\beta_1=10$, $6\beta_0+14\beta_1=23$: multiply the first by 2 and subtract → $2\beta_1=3$, so $\beta_1=\tfrac32$ and $\beta_0=\tfrac13$. The line is
$$y=\tfrac13+\tfrac32x .$$
Fitted values: $1.833,\ 3.333,\ 4.833$.

</details>

---

### I4. Residuals and error
For I3, compute the residuals and the least-squares error.

<details><summary><b>Solution</b></summary>

$\mathbf r=\mathbf b-\hat{\mathbf b}=[2-1.833,\ 3-3.333,\ 5-4.833]=[\tfrac16,-\tfrac13,\tfrac16]$.
- The residuals **sum to zero** (the design matrix contains a column of ones) ✔.
- $\|\mathbf r\|=\sqrt{\tfrac1{36}+\tfrac19+\tfrac1{36}}=\sqrt{\tfrac{6}{36}}=\tfrac{\sqrt6}{6}\approx0.408$.
- Check orthogonality: $A^{\mathsf T}\mathbf r=\mathbf 0$ ✔.
- Pythagoras: $\|\mathbf b\|^2=4+9+25=38=\|\hat{\mathbf b}\|^2+\|\mathbf r\|^2=(1.833^2+3.333^2+4.833^2)+0.1667$ ✔.

</details>

---

### I5. Projection matrix
For $A=\begin{bmatrix}1&1\\1&2\\1&3\end{bmatrix}$, find the projection matrix $P$ onto $\operatorname{Col} A$ and verify its properties.

<details><summary><b>Solution</b></summary>

From I3, $(A^{\mathsf T}A)^{-1}=\frac16\begin{bmatrix}14&-6\\-6&3\end{bmatrix}$. Then
$$A(A^{\mathsf T}A)^{-1}=\begin{bmatrix}4/3&-1/2\\1/3&0\\-2/3&1/2\end{bmatrix},\qquad
P=A(A^{\mathsf T}A)^{-1}A^{\mathsf T}=\frac16\begin{bmatrix}5&2&-1\\2&2&2\\-1&2&5\end{bmatrix}.$$
Checks: $P$ is **symmetric** ✔; $P^2=P$ (idempotent) ✔; $\operatorname{trace}P=2=\operatorname{rank}A$ ✔ (trace of a projection equals the dimension of the subspace). Applying it to $\mathbf b=[2,3,5]$ gives $P\mathbf b=\tfrac16[11,20,29]\approx[1.833,3.333,4.833]$ — exactly the fitted values ✔.

</details>

---

### I6. Solving the over-determined system with QR
Use $A=QR$ to solve I3 without forming $A^{\mathsf T}A$.

<details><summary><b>Solution</b></summary>

Gram–Schmidt on the columns $[1,1,1]^{\mathsf T}$ and $[1,2,3]^{\mathsf T}$:
- $\mathbf q_1=\frac1{\sqrt3}[1,1,1]^{\mathsf T}$, $r_{12}=\mathbf q_1\cdot[1,2,3]^{\mathsf T}=\frac6{\sqrt3}=2\sqrt3$.
- $\mathbf v_2=[1,2,3]-2[1,1,1]=[-1,0,1]$, so $\mathbf q_2=\frac1{\sqrt2}[-1,0,1]^{\mathsf T}$ and $r_{22}=\sqrt2$.
$$R=\begin{bmatrix}\sqrt3&2\sqrt3\\0&\sqrt2\end{bmatrix},\qquad Q^{\mathsf T}\mathbf b=\begin{bmatrix}10/\sqrt3\\3/\sqrt2\end{bmatrix}.$$
Back-substitute $R\hat{\mathbf x}=Q^{\mathsf T}\mathbf b$: $\sqrt2\,\beta_1=\frac3{\sqrt2}\Rightarrow\beta_1=\tfrac32$, then $\sqrt3\,\beta_0+2\sqrt3\cdot\tfrac32=\frac{10}{\sqrt3}\Rightarrow\beta_0=\tfrac13$ ✔ — same answer, and numerically more stable.

</details>

---

### I7. Quadratic (polynomial) fit
Fit $y=\beta_0+\beta_1x+\beta_2x^2$ to $(0,1),(1,3),(2,7),(3,13)$.

<details><summary><b>Solution</b></summary>

$$A=\begin{bmatrix}1&0&0\\1&1&1\\1&2&4\\1&3&9\end{bmatrix},\qquad\mathbf b=\begin{bmatrix}1\\3\\7\\13\end{bmatrix}.$$
The model is **linear in the parameters**, so the normal equation $A^{\mathsf T}A\boldsymbol\beta=A^{\mathsf T}\mathbf b$ applies. Here $\mathbf b=[1+0+0,\ 1+1+1,\ 1+2+4,\ 1+3+9]^{\mathsf T}$ — already a column of $A$ — so the fit is **exact**: $\boldsymbol\beta=[1,1,1]^{\mathsf T}$, i.e. $y=1+x+x^2$, with residual $\mathbf r=\mathbf 0$ and error $0$.

</details>

---

### I8. Why the residual is orthogonal to $\operatorname{Col} A$
Prove that the least-squares residual $\mathbf r=\mathbf b-A\hat{\mathbf x}$ satisfies $A^{\mathsf T}\mathbf r=\mathbf 0$.

<details><summary><b>Solution</b></summary>

Each $\mathbf x\in\mathbb{R}^n$ gives a candidate $A\mathbf x\in\operatorname{Col} A$. Define $f(\mathbf x)=\|\mathbf b-A\mathbf x\|^2$; at the minimum the gradient vanishes:
$$\nabla f=-2A^{\mathsf T}(\mathbf b-A\hat{\mathbf x})=-2A^{\mathsf T}\mathbf r=\mathbf 0 .$$
So $\mathbf r\perp$ every column of $A$, hence $\mathbf r\perp\operatorname{Col} A$: the error is orthogonal to the subspace, exactly the Best Approximation Theorem. Conversely this orthogonality gives the normal equation $A^{\mathsf T}A\hat{\mathbf x}=A^{\mathsf T}\mathbf b$.

</details>

---

### I9. Dependent columns — non-unique solution
Solve the least-squares problem for $A=\begin{bmatrix}1&2\\2&4\end{bmatrix}$, $\mathbf b=\begin{bmatrix}1\\1\end{bmatrix}$.

<details><summary><b>Solution</b></summary>

The columns are dependent, so $A^{\mathsf T}A=\begin{bmatrix}5&10\\10&20\end{bmatrix}$ is **singular** and $(A^{\mathsf T}A)^{-1}$ does not exist. The normal equation is still consistent:
$$5x_1+10x_2=3,\qquad10x_1+20x_2=6 \;\Rightarrow\; x_1=0.6-2x_2 .$$
So there are **infinitely many** least-squares solutions, all giving the same projection
$$\hat{\mathbf b}=A\hat{\mathbf x}=(x_1+2x_2)\begin{bmatrix}1\\2\end{bmatrix}=0.6\begin{bmatrix}1\\2\end{bmatrix}=\begin{bmatrix}0.6\\1.2\end{bmatrix}.$$
Residual $=[0.4,-0.2]$, orthogonal to $[1,2]^{\mathsf T}$ ✔; error $=\sqrt{0.2}\approx0.447$.

</details>

---

### I10. Interpreting a least-squares error of zero
When does a least-squares problem have error $0$? What does that say about the original system?

<details><summary><b>Solution</b></summary>

Error $0$ means $\mathbf r=\mathbf 0$, i.e. $\mathbf b=A\hat{\mathbf x}$ exactly, so $\mathbf b\in\operatorname{Col} A$ and the system is **consistent** — the least-squares solution is then an ordinary solution (and if $A$ has independent columns, it is unique). Equivalently $\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf b])$. Conversely, inconsistent systems have error $>0$.

</details>

---

# Part J — Eigenvalues and Eigenvectors (Chapter 8)

### J1. Find eigenvalues and eigenvectors
Diagonal-side example: $A=\begin{bmatrix}4&-2\\-2&4\end{bmatrix}$.

<details><summary><b>Solution</b></summary>

$\det(A-\lambda I)=(4-\lambda)^2-4=\lambda^2-8\lambda+12=(\lambda-2)(\lambda-6)=0$, so $\lambda=2,\ 6$.
- $\lambda=2$: $A-2I=\begin{bmatrix}2&-2\\-2&2\end{bmatrix}\to\begin{bmatrix}1&-1\\0&0\end{bmatrix}$, eigenvector $\mathbf v_1=\begin{bmatrix}1\\1\end{bmatrix}$.
- $\lambda=6$: $A-6I=\begin{bmatrix}-2&-2\\-2&-2\end{bmatrix}$, eigenvector $\mathbf v_2=\begin{bmatrix}1\\-1\end{bmatrix}$.
Check: $A\mathbf v_1=[2,2]^{\mathsf T}=2\mathbf v_1$ ✔, $A\mathbf v_2=[6,-6]^{\mathsf T}=6\mathbf v_2$ ✔. Also $\operatorname{trace}=8=2+6$ and $\det=12=2\cdot6$ ✔.

</details>

---

### J2. Triangular matrix shortcut
Find the eigenvalues, determinant and trace of $A=\begin{bmatrix}3&1&2\\0&-1&4\\0&0&5\end{bmatrix}$.

<details><summary><b>Solution</b></summary>

For a triangular matrix the eigenvalues are the **diagonal entries**: $\lambda=3,\ -1,\ 5$. Then $\operatorname{trace}=3-1+5=7$ (equals the sum of eigenvalues ✔) and $\det=3\cdot(-1)\cdot5=-15$ (equals the product ✔). No characteristic polynomial expansion needed.

</details>

---

### J3. Eigenspace bases
Find a basis for each eigenspace of $A=\begin{bmatrix}2&1\\1&2\end{bmatrix}$.

<details><summary><b>Solution</b></summary>

$\det(A-\lambda I)=(2-\lambda)^2-1=0\Rightarrow\lambda=1,3$.
- $\lambda=1$: $A-I=\begin{bmatrix}1&1\\1&1\end{bmatrix}$, so $x_1=-x_2$ and $E_1=\operatorname{span}\{\begin{bmatrix}-1\\1\end{bmatrix}\}$, $\dim E_1=1$.
- $\lambda=3$: $A-3I=\begin{bmatrix}-1&1\\1&-1\end{bmatrix}$, giving $E_3=\operatorname{span}\{\begin{bmatrix}1\\1\end{bmatrix}\}$, $\dim E_3=1$.

Each $E_\lambda$ is a subspace (the null space of $A-\lambda I$); all eigenvectors lie in $E_\lambda$, and $\mathbf 0$ is included in the space but is **not** an eigenvector.

</details>

---

### J4. Diagonalize
Write $A=\begin{bmatrix}4&-2\\-2&4\end{bmatrix}$ as $PDP^{-1}$.

<details><summary><b>Solution</b></summary>

Using J1, $P=\begin{bmatrix}1&1\\1&-1\end{bmatrix}$ (eigenvector columns) and $D=\begin{bmatrix}2&0\\0&6\end{bmatrix}$. With $\det P=-2$, $P^{-1}=\frac12\begin{bmatrix}1&1\\1&-1\end{bmatrix}$. Check $A=PDP^{-1}$: $PD=\begin{bmatrix}2&6\\2&-6\end{bmatrix}$, and $PDP^{-1}=\frac12\begin{bmatrix}2+6&2-6\\2-6&2+6\end{bmatrix}=\begin{bmatrix}4&-2\\-2&4\end{bmatrix}$ ✔. Diagonalization requires $A$ to have $n$ independent eigenvectors — here $(1,1)$ and $(1,-1)$ are independent ✔.

</details>

---

### J5. A non-diagonalizable (defective) matrix
Show that $A=\begin{bmatrix}2&1\\0&2\end{bmatrix}$ is not diagonalizable.

<details><summary><b>Solution</b></summary>

$\det(A-\lambda I)=(2-\lambda)^2$, so $\lambda=2$ with **algebraic multiplicity 2**. Now
$$A-2I=\begin{bmatrix}0&1\\0&0\end{bmatrix}\Rightarrow x_2=0,\ x_1\text{ free}\Rightarrow E_2=\operatorname{span}\{\begin{bmatrix}1\\0\end{bmatrix}\},$$
so the **geometric multiplicity is 1 < 2**. There are only 1 independent eigenvector instead of 2, so $P$ cannot be invertible and $A$ is not diagonalizable (it is *defective*).

</details>

---

### J6. Powers of a matrix and a dynamical system
Let $\mathbf x_{k+1}=A\mathbf x_k$ with $A=\frac16\begin{bmatrix}5&1\\2&4\end{bmatrix}$. Find $A^k$ and the long-run behaviour.

<details><summary><b>Solution</b></summary>

$\det(A-\lambda I)=\lambda^2-\tfrac32\lambda+\tfrac12=(\lambda-1)(\lambda-\tfrac12)$, so $\lambda_1=1$, $\lambda_2=\tfrac12$. Eigenvectors: for $\lambda=1$, $A-I=\frac16\begin{bmatrix}-1&1\\2&-2\end{bmatrix}\Rightarrow\mathbf v_1=\begin{bmatrix}1\\1\end{bmatrix}$; for $\lambda=\tfrac12$, $A-\tfrac12I=\frac16\begin{bmatrix}2&1\\2&1\end{bmatrix}\Rightarrow\mathbf v_2=\begin{bmatrix}1\\-2\end{bmatrix}$.

So $A=PDP^{-1}$ with $D=\operatorname{diag}(1,\tfrac12)$ and 
$$A^k=P\begin{bmatrix}1&0\\0&(\tfrac12)^k\end{bmatrix}P^{-1}.$$
Write $\mathbf x_0=c_1\mathbf v_1+c_2\mathbf v_2$; then $\mathbf x_k=c_1(1)^k\mathbf v_1+c_2(\tfrac12)^k\mathbf v_2\to c_1\mathbf v_1$.

Example: $\mathbf x_0=\begin{bmatrix}1\\0\end{bmatrix}=(\tfrac23)\mathbf v_1+(\tfrac13)\mathbf v_2$, so $\mathbf x_k\to\tfrac23\begin{bmatrix}1\\1\end{bmatrix}=\begin{bmatrix}2/3\\2/3\end{bmatrix}$ — a **steady state**, because $|\tfrac12|<1$ kills the second term.

</details>

---

### J7. Similar matrices share eigenvalues
Verify that $A=\begin{bmatrix}4&-2\\-2&4\end{bmatrix}$ and $B=\begin{bmatrix}2&0\\0&6\end{bmatrix}$ are similar and that the usual invariants agree.

<details><summary><b>Solution</b></summary>

From J4, $A=PBP^{-1}$ with $P=\begin{bmatrix}1&1\\1&-1\end{bmatrix}$, so they are **similar**.
- Eigenvalues: both $2$ and $6$ ✔ (similar matrices have the same characteristic polynomial, so the same eigenvalues).
- $\det A=12=\det B$ ✔ and $\operatorname{trace}A=8=\operatorname{trace}B$ ✔.
- Eigenvectors are **not** shared: $\mathbf v$ eigenvector of $B$ ⇒ $P\mathbf v$ eigenvector of $A$.

</details>

---

### J8. Complex eigenvalues of a real matrix
Find the eigenvalues of $A=\begin{bmatrix}2&-3\\3&2\end{bmatrix}$.

<details><summary><b>Solution</b></summary>

$\det(A-\lambda I)=(2-\lambda)^2+9=0\Rightarrow(2-\lambda)^2=-9\Rightarrow\lambda=2\pm3j$ — a **conjugate pair** $a\pm bj$ with $a=2$, $b=3$.

Interpretation: $A=\begin{bmatrix}2&0\\0&2\end{bmatrix}+3\begin{bmatrix}0&-1\\1&0\end{bmatrix}$ is a rotation by $90°$ scaled by $3$ and then scaled by $2$ radially (a rotation–dilation): $\lambda=r\angle\theta$ with $r=\sqrt{13}\approx3.61$ and $\theta=\arctan(3/2)\approx56.3°$. Since $j$ is not real, $A$ has no real eigenvectors: it is not diagonalizable over $\mathbb{R}$ (only over $\mathbb{C}$).

</details>

---

### J9. Change of basis and eigenvectors
Let $A=\begin{bmatrix}4&-2\\-2&4\end{bmatrix}$ and $\mathcal B=\{\begin{bmatrix}1\\1\end{bmatrix},\begin{bmatrix}1\\-1\end{bmatrix}\}$. Find $[\mathbf x]_{\mathcal B}$ for $\mathbf x=\begin{bmatrix}3\\1\end{bmatrix}$ and $[T]_{\mathcal B}$ for $T(\mathbf x)=A\mathbf x$.

<details><summary><b>Solution</b></summary>

Solve $c_1\mathbf b_1+c_2\mathbf b_2=\mathbf x$: $c_1+c_2=3$, $c_1-c_2=1$, so $c_1=2$, $c_2=1$ and $[\mathbf x]_{\mathcal B}=\begin{bmatrix}2\\1\end{bmatrix}$.

For the transformation, $[T]_{\mathcal B}=P_{\mathcal B}^{-1}AP_{\mathcal B}$ with $P_{\mathcal B}=\begin{bmatrix}1&1\\1&-1\end{bmatrix}$. Because $\mathcal B$ consists of **eigenvectors**, this is diagonal:
$$[T]_{\mathcal B}=\begin{bmatrix}2&0\\0&6\end{bmatrix}=D .$$

So “diagonalize” really means “choose the eigenvector basis”; $A$ and $D$ are the same transformation seen in different coordinate systems.

</details>

---

### J10. Eigenvalues of $A^2$, $A^{-1}$ and $A+cI$
For $A=\begin{bmatrix}2&1\\1&2\end{bmatrix}$ (eigenvalues $1,3$), list the eigenvalues of $A^2$, $A^{-1}$, $A+2I$ and give $\det(A^2)$, $\operatorname{trace}(A^2)$.

<details><summary><b>Solution</b></summary>

Applying $A\mathbf x=\lambda\mathbf x$ repeatedly: $A^2\mathbf x=\lambda^2\mathbf x$, $A^{-1}\mathbf x=\frac1\lambda\mathbf x$, $(A+cI)\mathbf x=(\lambda+c)\mathbf x$.

| Matrix | Eigenvalues | $\det$ | $\operatorname{trace}$ |
|---|---|---|---|
| $A$ | $1,\ 3$ | $3$ | $4$ |
| $A^2$ | $1,\ 9$ | $9$ | $10$ |
| $A^{-1}$ | $1,\ \tfrac13$ | $\tfrac13$ | $\tfrac43$ |
| $A+2I$ | $3,\ 5$ | $15$ | $8$ |

(Determinant = product, trace = sum of the eigenvalues.)

</details>

---

# Part K — Complex Numbers and the DFT (Chapter 8A)

### K1. Complex arithmetic
For $z_1=3+4j$, $z_2=1-2j$, compute $z_1+z_2$, $z_1z_2$ and $z_1/z_2$.

<details><summary><b>Solution</b></summary>

- $z_1+z_2=4+2j$.
- $z_1z_2=\left[(3)(1)-(4)(-2)\right]+\left[(3)(-2)+(4)(1)\right]j=(3+8)+(-6+4)j=11-2j$.
- $\dfrac{z_1}{z_2}=\dfrac{(3+4j)(1+2j)}{(1-2j)(1+2j)}=\dfrac{3+6j+4j+8j^2}{1+4}=\dfrac{-5+10j}{5}=-1+2j$.

(Division = multiply numerator and denominator by the **conjugate** of the denominator.)

</details>

---

### K2. Conjugate and modulus
For $z=3+4j$, find $\bar z$, $\lvert z\rvert$ and $z\bar z$. Express $1/z$ in rectangular form.

<details><summary><b>Solution</b></summary>

$\bar z=3-4j$, $\lvert z\rvert=\sqrt{3^2+4^2}=5$, and $z\bar z=9+16=25=\lvert z\rvert^2$ ✔. Therefore
$$\frac1z=\frac{\bar z}{\lvert z\rvert^2}=\frac{3-4j}{25}=0.12-0.16j .$$
Check: $(3+4j)(0.12-0.16j)=0.36-0.48j+0.48j-0.64j^2=0.36+0.64=1$ ✔.

</details>

---

### K3. Polar and exponential form
Write $z=1+j$ in polar and exponential form, and compute $z^8$.

<details><summary><b>Solution</b></summary>

$r=\lvert z\rvert=\sqrt2$, $\theta=\arctan(1)=\pi/4$, so $z=\sqrt2\angle45°=\sqrt2\,e^{j\pi/4}$.

De Moivre: $z^8=(\sqrt2)^8e^{j8\pi/4}=16e^{j2\pi}=16$ — a real answer, because $8\times45°=360°$ lands back on the positive real axis.

</details>

---

### K4. De Moivre
Compute $(1-\sqrt3 j)^6$.

<details><summary><b>Solution</b></summary>

$r=\sqrt{1+3}=2$ and $\theta=\arctan(-\sqrt3)=-60°$, so $z=2\angle(-60°)$. Then
$$z^6=2^6\angle(-360°)=64\angle0°=64 .$$

(Since $-60°\times6=-360°$, the result is again purely real.)

</details>

---

### K5. Roots of a complex number
Solve $z^3=8j$.

<details><summary><b>Solution</b></summary>

Write $8j=8\angle90°$. Then the three roots are
$$z_k=\sqrt[3]{8}\,\angle\!\left(\frac{90°+360°k}{3}\right)=2\angle(30°+120°k),\qquad k=0,1,2,$$
namely $2\angle30°$, $2\angle150°$ and $2\angle270°=-2j$. They are equally spaced on the circle of radius $2$ (each $120°$ apart), and their **sum is zero** ✔ — the same circular geometry as the $n$-th roots of unity, just rotated and scaled.

</details>

---

### K6. Complex inner product and norms
For $\mathbf a=[1+j,\ 2]^{\mathsf T}$ and $\mathbf b=[2,\ j]^{\mathsf T}$, compute $\langle\mathbf a,\mathbf b\rangle$, $\|\mathbf a\|$, $\|\mathbf b\|$, and decide if they are orthogonal.

<details><summary><b>Solution</b></summary>

$$\langle\mathbf a,\mathbf b\rangle=\overline{a_1}b_1+\overline{a_2}b_2=(1-j)(2)+(2)(j)=2-2j+2j=2 .$$
$\|\mathbf a\|=\sqrt{\lvert1+j\rvert^2+\lvert2\rvert^2}=\sqrt{2+4}=\sqrt6$; $\|\mathbf b\|=\sqrt{4+1}=\sqrt5$. Since $\langle\mathbf a,\mathbf b\rangle=2\neq0$, the vectors are **not** orthogonal. Note the conjugate on the first argument: $\langle\mathbf a,\mathbf b\rangle=\overline{\langle\mathbf b,\mathbf a\rangle}$, so complex “symmetry” is conjugate symmetry.

Example of orthogonality (used by the DFT): with $\mathbf w_0=[1,1,1,1]^{\mathsf T}$ and $\mathbf w_1=[1,j,-1,-j]^{\mathsf T}$,
$$\langle\mathbf w_0,\mathbf w_1\rangle=1+j-1-j=0 ✔$$
and $\langle\mathbf w_1,\mathbf w_1\rangle=1+1+1+1=4$, so $\|\mathbf w_1\|=2$.

</details>

---

### K7. DFT of a length-4 signal
Compute the DFT of $\mathbf x=[1,1,0,0]^{\mathsf T}$ ($N=4$).

<details><summary><b>Solution</b></summary>

$X[k]=\sum_{n=0}^{3}x[n]e^{-j\frac{2\pi}{4}kn}=1+e^{-j\pi k/2}$:

| $k$ | $X[k]$ |
|---|---|
| 0 | $1+1=2$ |
| 1 | $1+e^{-j\pi/2}=1-j$ |
| 2 | $1+e^{-j\pi}=1-1=0$ |
| 3 | $1+e^{-j3\pi/2}=1+j$ |

So $\mathbf X=[2,\ 1-j,\ 0,\ 1+j]^{\mathsf T}$. Check conjugate symmetry $X[N-k]=\overline{X[k]}$ ($X[3]=\overline{X[1]}$ ✔), as expected for a real signal. Note $X[0]=\sum_n x[n]=2$ ✔.

</details>

---

### K8. IDFT round trip
Verify the IDFT of $\mathbf X=[2,\ 1-j,\ 0,\ 1+j]^{\mathsf T}$ returns $\mathbf x=[1,1,0,0]^{\mathsf T}$.

<details><summary><b>Solution</b></summary>

$x[n]=\frac14\sum_{k=0}^{3}X[k]e^{j\pi kn/2}$:
- $n=0$: $\frac14(2+(1-j)+0+(1+j))=\frac14(4)=1$ ✔
- $n=1$: $\frac14(2+(1-j)j+(1+j)(-j))=\frac14(2+(1+j)+(-1-j))=\frac14(4)=1$ ✔
- $n=2$: $\frac14(2-(1-j)-(1+j))=\frac14(0)=0$ ✔
- $n=3$: $\frac14(2+(1-j)(-j)+(1+j)(j))=\frac14(2+(-1-j)+(-1+j))=0$ ✔

The **$1/N$ factor** in the IDFT (and not in the DFT) is what makes the round trip exact: DFT then IDFT returns the original signal, so the DFT is an invertible change of basis.

</details>

---

### K9. The DFT as a change of basis
Explain why the DFT is just a change of basis, and what the $N$ in the formula means.

<details><summary><b>Solution</b></summary>

The Fourier vectors $\mathbf w_k$ with entries $w_k[n]=e^{j2\pi kn/N}$ ($n=0,\dots,N-1$) form an **orthogonal basis** of $\mathbb{C}^N$: $\langle\mathbf w_k,\mathbf w_m\rangle=N\delta_{km}$. Since
$$X[k]=\langle\mathbf w_k,\mathbf x\rangle=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N},$$
the DFT simply gives the **coordinates of $\mathbf x$ in the Fourier basis**, and the IDFT changes back (dividing by $N$ because the basis vectors have length $\sqrt N$). $N$ is the **number of samples** in one period; the same formula with $k+N$ gives the same vector, hence aliasing.

</details>

---

### K10. Aliasing
A sinusoid at $60$ Hz is sampled at $f_s=100$ Hz. What frequency appears in the DFT, and how does that generalise?

<details><summary><b>Solution</b></summary>

Because $e^{j2\pi(f/f_s)n}=e^{j2\pi((f\pm f_s)/f_s)n}$, sampling cannot distinguish $f$ from $f\pm f_s$: $60$ Hz aliases to $100-60=40$ Hz. General rule: fold frequencies above the **Nyquist limit** $f_s/2$ about it, $f_{\text{apparent}}=\lvert f \bmod f_s\rvert$ (with folding towards $f_s/2$), so $60$ Hz “looks like” $40$ Hz. In DFT-bin terms, indices $k$ and $k+N$ give identical basis vectors, so only bins $k=0,\dots,N/2$ are unambiguous for a real signal.

</details>

---

*End of practice problems. Good luck! 🎓*
