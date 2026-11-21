# SC1004 / CX1104 — Study Guide: Chapters 6 → 8

> **What to learn, in order, for Chapters 6–8 (Part 2).**
> Chapter 6 *Orthogonality* · Chapter 7 *Least Squares* · Chapter 8 *Eigenvalues & Eigenvectors*.
>
> Each chapter below lists **what you must be able to do**, **what to know cold**, **pitfalls that cost marks**, and the practice problems that test it.
> Reference material: [C6 guide](./C6/Linear_Algebra_C6_Complete_Study_Guide.md) · [C7 guide](./C7/Linear_Algebra_C7_Complete_Study_Guide.md) · [C8 guide](./C8/Linear_Algebra_C8_Complete_Study_Guide.md) · [C8A guide](./C8A/Linear_Algebra_C8A_Complete_Study_Guide.md) — each ends with a **📐 Formula Sheet** revision page. For 8A there is also a teaching version: [C8A Study Guide](./C8A/C8A_Study_Guide.md) (ELI5 → step-by-step → detailed, plus full Tut8A solutions).
> Theorem statements: [theorems.md](./theorems.md) Parts VII–IX. Vocabulary: [definitions.md](./definitions.md). Problems: [practice_problems.md](./practice_problems.md) Parts H–J.

---

## The big picture (learn this before anything else)

```
Ch 6  Orthogonality      ──▶  Ch 7  Least Squares      ──▶  Ch 8  Eigenvalues
dot product, norm,             "b is not in Col A,           A x = λx,
⊥ projections,                 so minimize ‖b − Ax‖,         diagonalize A = PDP⁻¹,
orthonormal bases,             normal equation,             change of basis,
Gram–Schmidt, QR               projection matrix P          powers Aᵏ
```

The **one connective idea**: an orthogonal projection gives the *closest* point of a subspace to a vector. Chapter 7 is Chapter 6 applied to the column space of $A$; Chapter 8 is the same "pick a better basis" idea, where the better basis is the eigenvector basis.

**Study order:** 6.1 → 6.2 → 6.3 → 7.1 → 7.2 → 8.1.1–8.1.4 → 8.1.5–8.1.6.

---

## Chapter 6 — Orthogonality

### What you must be able to DO
1. **Compute norm and distance** — $\lVert\mathbf v\rVert=\sqrt{\sum v_i^2}$, $\;d(\mathbf u,\mathbf v)=\lVert\mathbf u-\mathbf v\rVert$, and **normalise** (make length 1): $\hat{\mathbf u}=\mathbf v/\lVert\mathbf v\rVert$ for $\mathbf v\neq\mathbf 0$.
2. **Compute the dot product two ways** — component form $\mathbf u\cdot\mathbf v=\sum u_iv_i=\mathbf u^{\mathsf T}\mathbf v$ (a scalar; not the outer product $\mathbf u\mathbf v^{\mathsf T}$), and angle form $\mathbf u\cdot\mathbf v=\lVert\mathbf u\rVert\lVert\mathbf v\rVert\cos\theta$. Use it to find **angles**, **test orthogonality** ($=0$), and read the sign (acute / right / obtuse).
3. **Apply the two inequalities** — Cauchy–Schwarz $\lvert\mathbf u\cdot\mathbf v\rvert\le\lVert\mathbf u\rVert\lVert\mathbf v\rVert$, and the triangle inequality $\lVert\mathbf u+\mathbf v\rVert\le\lVert\mathbf u\rVert+\lVert\mathbf v\rVert$ (plus the distance version).
4. **Write the point–normal form** of a line/plane: $a(x-x_0)+b(y-y_0)+c(z-z_0)=0$, normal $\mathbf n=(a,b,c)$.
5. **Project a vector onto a vector**: $\operatorname{proj}_{\mathbf a}\mathbf u=\dfrac{\mathbf u\cdot\mathbf a}{\lVert\mathbf a\rVert^{2}}\mathbf a$, and the **orthogonal component** $\mathbf u-\operatorname{proj}_{\mathbf a}\mathbf u$.
6. **Project onto a subspace** with an orthogonal basis — Theorem 8:
   $\hat{\mathbf y}=\dfrac{\mathbf y\cdot\mathbf u_1}{\mathbf u_1\cdot\mathbf u_1}\mathbf u_1+\cdots+\dfrac{\mathbf y\cdot\mathbf u_p}{\mathbf u_p\cdot\mathbf u_p}\mathbf u_p$, and with an orthonormal basis, $\hat{\mathbf y}=UU^{\mathsf T}\mathbf y$.
7. **State and use the Orthogonal Decomposition** $\mathbf y=\hat{\mathbf y}+\mathbf z$ (unique, $\hat{\mathbf y}\in W$, $\mathbf z\in W^{\perp}$) and the **Best Approximation Theorem** ($\hat{\mathbf y}$ is the unique closest point of $W$ to $\mathbf y$).
8. **Explain why an orthogonal set of nonzero vectors is linearly independent** (so it is a basis for its span) — Theorem 4.
9. **Find coordinates in an orthogonal basis**: $c_j=\dfrac{\mathbf y\cdot\mathbf u_j}{\mathbf u_j\cdot\mathbf u_j}$.
10. **Use orthonormal matrices** — $U^{\mathsf T}U=I$ (Theorem 6); if $U$ is **square** it is an *orthogonal matrix* with $U^{-1}=U^{\mathsf T}$ and $UU^{\mathsf T}=I$; if **rectangular**, $UU^{\mathsf T}$ is the projection onto $\operatorname{Col}U$; and $\lVert U\mathbf x\rVert=\lVert\mathbf x\rVert$ (lengths and angles preserved).
11. **Run Gram–Schmidt** to turn a basis into an orthogonal basis — Theorem 11:
    $\mathbf v_1=\mathbf x_1$, $\;\mathbf v_j=\mathbf x_j-\sum_{i<j}\dfrac{\mathbf x_j\cdot\mathbf v_i}{\mathbf v_i\cdot\mathbf v_i}\mathbf v_i$, then normalise to get $Q$.
12. **Factor $A=QR$** — $Q$ has orthonormal columns spanning $\operatorname{Col}A$, $R$ is upper triangular with $r_{ij}=\dfrac{\mathbf x_j\cdot\mathbf v_i}{\mathbf v_i\cdot\mathbf v_i}$ and $r_{jj}=\lVert\mathbf v_j\rVert$; know **economy vs full** ($\texttt{qr(A,0)}$ vs $\texttt{qr(A)}$).
13. **Solve $A\mathbf x=\mathbf b$ with QR**: $R\mathbf x=Q^{\mathsf T}\mathbf b$, then back-substitute.

### Know cold
$\mathbf u\cdot\mathbf v=\mathbf u^{\mathsf T}\mathbf v$ · $W^{\perp}=\{\mathbf z:\mathbf z\cdot\mathbf w=0\;\forall\mathbf w\in W\}$ · projection matrix $P=QQ^{\mathsf T}$ is **symmetric and idempotent** ($P^{\mathsf T}=P$, $P^2=P$) · Pythagoras for projections:
$\lVert\mathbf y-\mathbf v\rVert^2=\lVert\mathbf y-\hat{\mathbf y}\rVert^2+\lVert\hat{\mathbf y}-\mathbf v\rVert^2$.

### Pitfalls that cost marks
- In Gram–Schmidt, subtract projections onto the **previously computed $\mathbf v_i$**, never the original $\mathbf x_i$.
- Denominator is $\mathbf u_j\cdot\mathbf u_j$, **not** $\lVert\mathbf u_j\rVert$.
- An orthogonal set is only guaranteed independent if the vectors are **nonzero**.
- "Orthogonal matrix" means **square** with orthonormal columns. A rectangular $U$ has $U^{\mathsf T}U=I$ but $UU^{\mathsf T}\neq I$.
- A zero pivot $r_{jj}$ in $R$ signals a **dependent** column of $A$ (then $R$ is singular).

**Practise:** Part H — H1 specs norm/unit vectors, H4 Cauchy–Schwarz, H5–H7 projections, H8 $U^{\mathsf T}U=I$, H10 Gram–Schmidt, H11–H12 QR.

---

## Chapter 7 — Least Squares

### What you must be able to DO
1. **Diagnose a system by shape**: $m=n$ → $\mathbf x=A^{-1}\mathbf b$; $m<n$ → under-determined (infinitely many); $m>n$ → over-determined → **least squares**.
2. **Test consistency**: $A\mathbf x=\mathbf b$ consistent $\iff \mathbf b\in\operatorname{Col}A \iff \operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf b])$.
3. **State the least-squares problem**: find $\hat{\mathbf x}$ minimising $\lVert\mathbf b-A\mathbf x\rVert$ (equivalently the sum of squared residuals $e_1^2+\cdots+e_m^2$).
4. **Derive/apply the normal equation** $A^{\mathsf T}A\hat{\mathbf x}=A^{\mathsf T}\mathbf b$, i.e. $\hat{\mathbf x}=(A^{\mathsf T}A)^{-1}A^{\mathsf T}\mathbf b$.
5. **Explain the geometry**: the residual $\mathbf b-A\hat{\mathbf x}$ is orthogonal to every column of $A$ — *that* is why the equation is called "normal".
6. **Build and use the projection matrix** $P=A(A^{\mathsf T}A)^{-1}A^{\mathsf T}$ — square, **symmetric**, **idempotent**; fitted values $\hat{\mathbf b}=A\hat{\mathbf x}=P\mathbf b$; residual $(I-P)\mathbf b\in(\operatorname{Col}A)^{\perp}$.
7. **Compute the least-squares error** $\lVert\mathbf b-A\hat{\mathbf x}\rVert$.
8. **Solve the over-determined case three ways**: (1) pseudoinverse, (2) normal equation + elimination on $[\,A^{\mathsf T}A\mid A^{\mathsf T}\mathbf b\,]$, (3) **QR**: $R\hat{\mathbf x}=Q^{\mathsf T}\mathbf b$.
9. **Fit a model**: least-squares line $y=\beta_0+\beta_1x$; polynomial $y=\beta_0+\beta_1x+\cdots+\beta_kx^k$; build the **design matrix** (rows $(1,x_j)$, or Vandermonde $(1,x_j,x_j^2)$) and solve the normal equation. Understand **"linear in the parameters"** — that is the only linearity required.
10. **Handle a singular $A^{\mathsf T}A$**: infinitely many least-squares solutions (dependent columns).

### Worked numbers worth memorising (they show up in exams)
| Setup | Result |
|---|---|
| $A=\begin{bmatrix}2&0\\-1&1\\0&2\end{bmatrix}$, $\mathbf b=(1,0,-1)$ | $\hat{\mathbf x}=(\tfrac13,-\tfrac13)$, squared error $\approx 0.680$ |
| $A=\begin{bmatrix}4&0\\0&2\\1&1\end{bmatrix}$, $\mathbf b=(2,0,11)$ | $\hat{\mathbf x}=(1,2)$, $\hat{\mathbf b}=(4,4,3)$, error $=\sqrt{84}\approx 9.17$ |

### Pitfalls
- $A^{\mathsf T}A$ is invertible **only if the columns of $A$ are independent**.
- Do not confuse the **residual vector** with its **norm** (the error).
- Projection onto a **line** is $P=\dfrac{\mathbf v\mathbf v^{\mathsf T}}{\mathbf v^{\mathsf T}\mathbf v}$ — a special case of the general $P$.
- QR is preferred numerically: it avoids forming/squaring the condition number via $A^{\mathsf T}A$.

**Practise:** Part I — I1 consistency, I2–I3 normal equations, I4 residual/error, I5 projection matrix, I6 QR, I7 quadratic fit, I8 why the residual is orthogonal.

---

## Chapter 8 — Eigenvalues & Eigenvectors

### What you must be able to DO
1. **Verify** that $\lambda$ is an eigenvalue and $\mathbf x$ an eigenvector: $A\mathbf x=\lambda\mathbf x$ with $\mathbf x\neq\mathbf 0$.
2. **Find eigenvalues** from the characteristic equation $\det(A-\lambda I)=0$ (degree-$n$ polynomial). Read them **instantly off the diagonal** for triangular/diagonal matrices.
3. **Find eigenvectors** by solving $(A-\lambda I)\mathbf x=\mathbf 0$; give a **basis for each eigenspace** $E_\lambda=N(A-\lambda I)$.
4. **Distinguish algebraic vs geometric multiplicity** — root multiplicity vs $\dim N(A-\lambda I)$ — and detect a **defective** matrix (geometric < algebraic).
5. **Diagonalize**: $A=PDP^{-1}$, where the columns of $P$ are $n$ **linearly independent eigenvectors** and $D$ holds the matching eigenvalues. Know the three criteria: (a) $n$ independent eigenvectors; (b) $n$ **distinct** eigenvalues ⇒ diagonalizable; (c) for every eigenvalue, geometric = algebraic multiplicity.
6. **Explain that eigenvectors for distinct eigenvalues are linearly independent.**
7. **Compute powers fast**: if $A=PDP^{-1}$ then $A^k=PD^kP^{-1}$ — and use this on difference equations / population / Markov-style problems.
8. **Use the shortcuts**: $\det A=\prod_i\lambda_i$, $\operatorname{tr}A=\sum_i\lambda_i$; $A$ invertible $\iff 0$ is **not** an eigenvalue; $A^k\mathbf x=\lambda^k\mathbf x$; $A+cI$ has eigenvalues $\lambda_i+c$; $A^{-1}$ has eigenvalues $1/\lambda_i$.
9. **Change basis / coordinate systems**: $\mathbf x=c_1\mathbf b_1+\cdots+c_n\mathbf b_n\Rightarrow[\mathbf x]_{\mathcal B}=(c_1,\dots,c_n)$; $[\mathbf x]_{\mathcal C}=\mathop{P}\limits_{\mathcal C\leftarrow\mathcal B}[\mathbf x]_{\mathcal B}$; interpret **diagonalization as a change of basis** and compute the $\mathcal B$-matrix $[T]_{\mathcal B}=P_{\mathcal B}^{-1}AP_{\mathcal B}$. Know that **similar matrices** share eigenvalues, determinant, trace (and characteristic polynomial).
10. **Handle complex eigenvalues** of a real matrix: they come in **conjugate pairs** $a\pm bj$; a $2\times2$ rotation by $\theta$ has $\lambda=e^{\pm j\theta}=\cos\theta\pm j\sin\theta$ (no real eigenvectors); the real form uses the block $\begin{bmatrix}a&-b\\b&a\end{bmatrix}$.

### Pitfalls
- An eigenvector can **never** be $\mathbf 0$; $E_\lambda$ includes $\mathbf 0$ but $\mathbf 0$ is not an eigenvector.
- Write $P$ and $D$ in the **same order** — column $i$ of $P$ pairs with diagonal entry $i$ of $D$.
- A repeated eigenvalue means you **must** check geometric multiplicity; do not assume diagonalizable.
- $\det(A-\lambda I)$ and $\det(\lambda I-A)$ differ by a sign but have the **same roots** — do not panic.

**Practise:** Part J — J1 eigenvalues/eigenvectors, J3 eigenspace bases, J4 diagonalize, J5 defective matrix, J6 powers/dynamical system, J7 similar matrices, J8 complex eigenvalues, J9 change of basis, J10 eigenvalues of $A^2$, $A^{-1}$, $A+cI$.

---

## Note on Chapter 8A (Complex Numbers & DFT)
If your syllabus includes it, treat [C8A](./C8A/C8A_Study_Guide.md) as a **prerequisite for §8.1.6 (complex eigenvalues)** and as an application of orthogonality to a complex inner product. The minimum: conjugate/modulus/polar form → Euler's formula & De Moivre → conjugate-transpose inner product $\langle\mathbf a,\mathbf b\rangle=\mathbf b^{H}\mathbf a$ (conjugate the **second** argument, as in the 8A slides) → the Fourier basis → DFT/IDFT as a **change of basis**. It is really "Chapter 6 orthogonality, but over $\mathbb{C}$".

**Practise:** Part K — K1–K5 complex arithmetic/De Moivre/roots, K6 complex inner product, K7–K9 DFT/IDFT/change of basis, K10 aliasing.

---

## Master checklist (tick these off)

**Chapter 6**
- [ ] Norm, unit vector, distance
- [ ] Dot product both forms; angle between vectors
- [ ] Cauchy–Schwarz & triangle inequality
- [ ] Orthogonal / orthonormal sets; orthogonal ⇒ independent
- [ ] Projection onto a vector & onto a subspace
- [ ] Orthogonal decomposition + Best Approximation Theorem
- [ ] Orthonormal matrices: $U^{\mathsf T}U=I$, square vs rectangular
- [ ] Gram–Schmidt by hand
- [ ] $A=QR$ by hand + solve $A\mathbf x=\mathbf b$ via QR

**Chapter 7**
- [ ] Classify $m=n$, $m<n$, $m>n$
- [ ] Consistency via $\operatorname{Col}A$ / rank
- [ ] Set up and solve the normal equation
- [ ] Why the residual is orthogonal to $\operatorname{Col}A$
- [ ] Projection matrix $P$ and its 3 properties; fitted values & residual
- [ ] Least-squares error
- [ ] Three solution routes (pseudoinverse / elimination / QR)
- [ ] Least-squares line & polynomial fit (design matrix)

**Chapter 8**
- [ ] Find eigenvalues via the characteristic equation
- [ ] Find eigenvector / eigenspace bases
- [ ] Algebraic vs geometric multiplicity; defective matrices
- [ ] Diagonalization criteria
- [ ] $A^k$ via $PD^kP^{-1}$
- [ ] $\det$, trace, invertibility, $A+cI$, $A^{-1}$, $A^k$ eigenvalue rules
- [ ] Coordinate vectors & change of basis
- [ ] Diagonalization as change of basis / similar matrices
- [ ] Complex eigenvalues & rotation matrices

---

## Suggested revision cycle
1. **Read one section** of the chapter guide, then immediately do its formula-sheet row from memory.
2. **Work the matching problems** in [practice_problems.md](./practice_problems.md) (H → I → J) with the solution collapsed.
3. **Re-derive, don't re-read**: normal equation, Gram–Schmidt, diagonalization criteria, and the QR solution route should all be reproducible on a blank page.
4. **Past-paper style sweep**: one least-squares fit + one QR + one full diagonalization + one $A^k$ problem, untimed then timed.

*End of guide.*
