# SC1004 — Theorem Navigator: What Gets What

> **What this file is.** A reverse-lookup for the course theorems. Instead of restating every result, it answers two questions fast:
>
> - **"I have / computed X — what does it let me conclude or find?"**
> - **"I need to prove / find Y — which theorem do I reach for?"**
>
> Full statements and proofs live in [theorems.md](theorems.md). This file is the index **by use**. For a proof-first study version that shows how one proof branches into many conclusions, see [proof_branches.md](proof_branches.md).
>
> **Legend:** $\iff$ = exactly equivalent (either direction works); $\Rightarrow$ = one-way only; *italics* = what you must supply; **bold** = the payoff.

## Contents

- [0. The whole file in 30 seconds](#0-the-whole-file-in-30-seconds)
- [1. Goal → Tool](#1-goal--tool)
  - [1.1 Invertibility and inverses](#11-invertibility-and-inverses)
  - [1.2 Solving systems and describing solution sets](#12-solving-systems-and-describing-solution-sets)
  - [1.3 Independence, span, basis, dimension](#13-independence-span-basis-dimension)
  - [1.4 Determinants](#14-determinants)
  - [1.5 Orthogonality, projection, least squares](#15-orthogonality-projection-least-squares)
  - [1.6 Eigenvalues, diagonalization, powers](#16-eigenvalues-diagonalization-powers)
  - [1.7 Change of basis and linear transformations](#17-change-of-basis-and-linear-transformations)
  - [1.8 Complex numbers and the DFT](#18-complex-numbers-and-the-dft)
- [2. Object → What it tells you](#2-object--what-it-tells-you)
- [3. Condition → Conclusion](#3-condition--conclusion)
- [4. Theorem-by-theorem payload](#4-theorem-by-theorem-payload)
- [5. Converse traps](#5-converse-traps)
- [6. Question → Immediate move](#6-question--immediate-move)

---

## 0. The whole file in 30 seconds

| If you have / know… | You can get… | Tool |
|---|---|---|
| $\det A$ | invertibility, singularity, area/volume scale, product of eigenvalues | determinant |
| $\operatorname{rank} A$ | independence, span, consistency, nullity, dimension of $\operatorname{Col} A$ | Rank Theorem |
| RREF of $A$ or $[A \mid \mathbf b]$ | solution set, pivots, free variables, bases | row reduction |
| eigenvalues / eigenvectors | diagonalizability, powers $A^k$, growth/decay, similarity invariants | eigen-analysis |
| a subspace $W$ and a vector $\mathbf y$ | closest point in $W$, decomposition $\mathbf y=\hat{\mathbf y}+\mathbf z$, least-squares fit | orthogonal projection |
| an orthogonal set | free linear independence, easy coordinates | dot product |
| $A=QR$ | stable least squares, orthonormal basis of $\operatorname{Col} A$ | Gram–Schmidt |
| $A=PDP^{-1}$ | fast powers, discrete dynamics | diagonalization |
| $P_{\mathcal C\leftarrow\mathcal B}$ | convert coordinates between bases | change of basis |
| $U^{\mathsf T}U=I$ | $U^{-1}=U^{\mathsf T}$ (square case), norm preservation | orthogonal matrices |
| a complex eigenvalue pair | rotation–scaling geometry | complex eigenvalues |
| the Fourier basis | DFT = change of basis | DFT |

---

## 1. Goal → Tool

Start here when you know **what you want** but not which result to use.

### 1.1 Invertibility and inverses

| Goal | Reach for | What you get |
|---|---|---|
| Decide whether a square $A$ is invertible | **Invertible Matrix Theorem** — pick the easiest of: $\det A\neq0$, RREF $=I$, $n$ pivots, $\operatorname{rank}A=n$, $N(A)=\{\mathbf 0\}$, independent columns, columns span $\mathbb R^n$, $A\mathbf x=\mathbf b$ solvable for every $\mathbf b$, $0$ not an eigenvalue, $A^{\mathsf T}$ invertible | all of these are the **same statement** |
| Compute $A^{-1}$ | row-reduce $[A \mid I]$ to $[I \mid A^{-1}]$ (Thm 2.3); $2\times2$ formula; inverse laws (Thm 2.2) | the inverse, or proof that none exists |
| Solve $A\mathbf x=\mathbf b$ when $A$ is invertible | Thm 2.1 | **unique** solution $\mathbf x=A^{-1}\mathbf b$ |
| Show a product $AB$ is invertible | Thm 2.2 | $(AB)^{-1}=B^{-1}A^{-1}$ |
| Show a matrix is **singular** | any one of: $\det A=0$, $\operatorname{rank}A<n$, $0$ is an eigenvalue, nontrivial $N(A)$, dependent rows/columns, RREF $\neq I$ | singularity (all equivalent) |
| Invert a transpose / inverse / product | Thm 2.2 | $(A^{-1})^{-1}=A$, $(A^{\mathsf T})^{-1}=(A^{-1})^{\mathsf T}$, $(AB)^{-1}=B^{-1}A^{-1}$ |
| Avoid computing $A^{-1}$ when solving many systems | LU factorization | reuse the same $L,U$; about $\tfrac13$ the flops of forming $A^{-1}$ |

> **One-line test:** for a **square** matrix, $\boxed{\det A\neq0 \iff A\text{ invertible}}$. But the determinant is *not* the only route — rank, pivots, or independence may be cheaper.

### 1.2 Solving systems and describing solution sets

| Goal | Reach for | What you get |
|---|---|---|
| Does $A\mathbf x=\mathbf b$ have a solution? | RREF of $[A \mid \mathbf b]$; or $\operatorname{rank}A=\operatorname{rank}[A \mid \mathbf b]$; or $\mathbf b\in\operatorname{Col}A$ | consistent or not |
| How many solutions? | pivot/free-variable count | $0$ (inconsistent), $1$ (no free variables), or $\infty$ (at least one free variable) |
| Describe **all** solutions | Thm 1.4 | $\mathbf x=\mathbf p+\mathbf v_h$, where $\mathbf p$ is one particular solution and $\mathbf v_h\in N(A)$ |
| Solve the homogeneous system | $N(A)$; free variables | always consistent; nontrivial solution $\iff$ free variable |
| Is $A\mathbf x=\mathbf b$ solvable **for every** $\mathbf b$? | Thm 1.2; pivot in **every row** | columns span $\mathbb R^m$ |
| Is the solution **unique** for every $\mathbf b$? | square case: IMT | $A$ invertible |
| Over-determined ($m>n$) | counting rule + least squares | cannot span $\mathbb R^m$; usually inconsistent; use projection |
| Under-determined ($m<n$) and consistent | counting rule | infinitely many solutions (free variables) |
| Solve repeatedly for different $\mathbf b$ | $LU$ (or $A^{-1}$ if small) | fast re-solves |
| Convert between system / vector / matrix form | Thm 1.1 | all three have the **same solution set** |

> **Reading RREF:** a pivot in the **augmented column** $\Rightarrow$ inconsistent. Pivots only in the coefficient columns $\Rightarrow$ consistent. If consistent, a missing pivot in a variable column makes that variable free, hence infinitely many solutions.

### 1.3 Independence, span, basis, dimension

| Goal | Reach for | What you get |
|---|---|---|
| Test whether $\{\mathbf v_1,\dots,\mathbf v_p\}$ is independent | RREF of $[\mathbf v_1\ \cdots\ \mathbf v_p]$ | independent $\iff$ pivot in **every column** $\iff$ no free variables |
| Test dependence quickly | Thm 1.5 ($p>n$), Thm 1.6 (contains $\mathbf 0$), Thm 4.4 (one vector is a combination of earlier ones) | dependent |
| Test independence of a **square** set | $\det[\mathbf v_1\ \cdots\ \mathbf v_n]\neq0$ | independent |
| Test whether a set spans $\mathbb R^m$ | Thm 1.2: pivot in **every row** | spans $\iff \operatorname{rank}=m$ |
| Show a set is a **basis** of $\mathbb R^n$ | $n$ vectors + independent (then spanning is automatic), or $n$ vectors + spanning | basis |
| Find a basis for $\operatorname{Col}A$ | Thm 4.6 | the **pivot columns of $A$ itself** (not of the RREF) |
| Find a basis for $N(A)$ | solve $A\mathbf x=\mathbf 0$, express in free variables | one basis vector per free variable |
| Find a basis for the row space | Thm 4.7 | the nonzero rows of any echelon form |
| Find a basis for $\operatorname{Span}\{\mathbf v_1,\dots,\mathbf v_p\}$ | make them columns, row-reduce, take pivot columns of the original matrix | basis of the span |
| Find a basis for $W^\perp$ | when $W=\operatorname{Col}A$: $W^\perp=N(A^{\mathsf T})$ | orthogonal complement |
| Find a dimension | rank for $\operatorname{Col}A$/row space; nullity for $N(A)$; $n-\dim W$ for $W^\perp$ | dimension count |
| Trim a spanning set to a basis | **Spanning Set Theorem** (Thm 4.5) | remove any vector that is a combination of the others |
| Produce an orthogonal/orthonormal basis | **Gram–Schmidt** (Thm 11) | orthogonal basis with the same spans |
| Check a vector is in a span | solve $A\mathbf x=\mathbf b$ | membership test |

> **Three bases, three recipes:** $\operatorname{Col}A$ $\to$ pivot columns of $A$; $\operatorname{Row}A$ $\to$ nonzero rows of REF; $N(A)$ $\to$ free-variable vectors. Do not mix them up.

### 1.4 Determinants

| Goal | Reach for | What you get |
|---|---|---|
| Test invertibility | $\det A\neq0$ | invertible |
| Compute a determinant efficiently | row-reduce to triangular, multiply the diagonal, track sign changes; cofactor expansion for small matrices | determinant |
| Area / volume | Thm 3.1 | $\lvert\det A\rvert$ = area of parallelogram (2×2) or volume of parallelepiped (3×3) spanned by the columns |
| Effect of a linear transformation on size | Thm 3.2 | area/volume multiplied by $\lvert\det A\rvert$ |
| Determinant of a product / inverse / transpose / power | determinant properties | $\det(AB)=\det A\det B$, $\det(A^{-1})=1/\det A$, $\det(A^{\mathsf T})=\det A$, $\det(A^k)=(\det A)^k$ |
| Determinant after row operations | the nine properties | swap $\to$ sign flip; scale a row $\to$ scale $\det$; add a multiple of a row $\to$ unchanged |
| Determinant of a triangular matrix | property 7 | product of the diagonal entries |
| Determinant from eigenvalues | $\det A=\prod_i\lambda_i$ | product of eigenvalues |
| Meaning of $\det A=0$ | properties + Thm 3.1 | singular; dependent rows/columns; $0$ is an eigenvalue; the transformation collapses volume |
| Build the characteristic polynomial | $\det(A-\lambda I)=0$ | eigenvalues |

> **Warning:** $\det(A+B)\neq\det A+\det B$ in general. The product rule $\det(AB)=\det A\det B$ is safe.

### 1.5 Orthogonality, projection, least squares

| Goal | Reach for | What you get |
|---|---|---|
| Test orthogonality | $\mathbf u\cdot\mathbf v=0$ | orthogonal |
| Find an angle | $\cos\theta=\dfrac{\mathbf u\cdot\mathbf v}{\lVert\mathbf u\rVert\,\lVert\mathbf v\rVert}$; Cauchy–Schwarz guarantees this is in $[-1,1]$ | angle |
| Find length / distance | $\lVert\mathbf v\rVert=\sqrt{\mathbf v\cdot\mathbf v}$; $d(\mathbf u,\mathbf v)=\lVert\mathbf u-\mathbf v\rVert$ | length / distance |
| Normalize a vector | $\mathbf u=\mathbf v/\lVert\mathbf v\rVert$ | unit vector |
| Project onto a **line** | Thm 3.3.2 | $\operatorname{proj}_{\mathbf a}\mathbf u=\dfrac{\mathbf u\cdot\mathbf a}{\mathbf a\cdot\mathbf a}\mathbf a$; the residual is orthogonal to $\mathbf a$ |
| Split a vector into $W$ + $W^\perp$ | **Orthogonal Decomposition Theorem** (Thm 5) | unique $\mathbf y=\hat{\mathbf y}+\mathbf z$, $\hat{\mathbf y}\in W$, $\mathbf z\in W^\perp$ |
| Project onto a subspace with an **orthogonal** basis | Thm 8 | $\hat{\mathbf y}=\sum_j\dfrac{\mathbf y\cdot\mathbf u_j}{\mathbf u_j\cdot\mathbf u_j}\mathbf u_j$ |
| Project onto a subspace with an **orthonormal** basis | Thm 10 | $\hat{\mathbf y}=UU^{\mathsf T}\mathbf y$ |
| Find the closest point in $W$ | **Best Approximation Theorem** (Thm 9 / 6.4.1) | the projection $\hat{\mathbf y}$; it is strictly closest |
| Find the distance from $\mathbf y$ to $W$ | projection | $\lVert\mathbf y-\hat{\mathbf y}\rVert$ |
| Orthonormalize a basis | Gram–Schmidt (Thm 11) | orthonormal basis, same nested spans |
| Factor $A=QR$ | QR theorem | $Q$ orthonormal basis of $\operatorname{Col}A$, $R$ upper triangular invertible |
| Solve a least-squares problem | normal equations or QR | $\hat{\mathbf x}$ minimizing $\lVert\mathbf b-A\mathbf x\rVert$ |
| Fit a line/polynomial/other model | design matrix + normal equations | coefficients |
| Test whether $U$ has orthonormal columns | $U^{\mathsf T}U=I$ (Thm 6) | orthonormal columns; if square, $U^{-1}=U^{\mathsf T}$ |
| Build a projection matrix | $P=UU^{\mathsf T}$ or $P=A(A^{\mathsf T}A)^{-1}A^{\mathsf T}$ | $P^2=P$, $P^{\mathsf T}=P$ |
| Project onto the orthogonal complement | $I-P$ | projection onto $W^\perp=N(A^{\mathsf T})$ when $W=\operatorname{Col}A$ |

> **Least-squares chain:** residual $\perp\operatorname{Col}A$ $\Rightarrow$ $A^{\mathsf T}(\mathbf b-A\hat{\mathbf x})=\mathbf 0$ $\Rightarrow$ **normal equations** $A^{\mathsf T}A\hat{\mathbf x}=A^{\mathsf T}\mathbf b$. If the columns of $A$ are independent, $A^{\mathsf T}A$ is invertible and $\hat{\mathbf x}$ is unique.

### 1.6 Eigenvalues, diagonalization, powers

| Goal | Reach for | What you get |
|---|---|---|
| Find eigenvalues | solve $\det(A-\lambda I)=0$ | eigenvalues (degree $n$, so $n$ over $\mathbb C$ counted with multiplicity) |
| Find eigenvalues fast | triangular/diagonal $\to$ diagonal entries; $A^k\to\lambda^k$; $A^{-1}\to1/\lambda$; $A^{\mathsf T}$ has the same eigenvalues | eigenvalues without the characteristic polynomial |
| Find eigenvectors | $N(A-\lambda I)$ | eigenspace basis |
| Test whether $\lambda$ is an eigenvalue | $\det(A-\lambda I)=0$ or nontrivial $N(A-\lambda I)$ | yes/no |
| Decide diagonalizability | Thm 9.5 / 9.6 | $n$ independent eigenvectors $\iff$ geometric = algebraic for every $\lambda$; $n$ **distinct** eigenvalues is a sufficient shortcut |
| Diagonalize | $P=[\mathbf v_1\ \cdots\ \mathbf v_n]$, $D=\operatorname{diag}(\lambda_i)$ | $A=PDP^{-1}$ |
| Compute $A^k$ | diagonalization | $A^k=PD^kP^{-1}$ |
| Solve $\mathbf x_{k+1}=A\mathbf x_k$ | diagonalization | $\mathbf x_k=A^k\mathbf x_0$; $\lvert\lambda\rvert<1$ decays, $\lvert\lambda\rvert>1$ grows |
| Show two matrices are similar | find $P$ with $A=PBP^{-1}$ | same characteristic polynomial, eigenvalues, determinant, trace |
| Analyze a transformation without a standard basis | $[T]_{\mathcal B}=P_{\mathcal B}^{-1}AP_{\mathcal B}$ | $\mathcal B$-matrix; diagonal when $\mathcal B$ is an eigenbasis |
| Relate trace/determinant to eigenvalues | 9.1 | $\operatorname{tr}A=\sum\lambda_i$, $\det A=\prod\lambda_i$ |
| Compare multiplicities | 9.2 / 9.5 | $1\le\dim E_\lambda\le$ algebraic multiplicity; equality for all $\lambda$ $\iff$ diagonalizable |
| Handle non-real eigenvalues of a real matrix | 9.11 | conjugate pair $a\pm bj$; rotation–scaling; not diagonalizable over $\mathbb R$ |

> **Diagonalizability checklist:** (1) compute eigenvalues; (2) for each, compute $\dim N(A-\lambda I)$; (3) compare with algebraic multiplicity. Distinct eigenvalues $\Rightarrow$ automatically diagonalizable, but **repeated eigenvalues do not automatically prevent it**.

### 1.7 Change of basis and linear transformations

| Goal | Reach for | What you get |
|---|---|---|
| Build the matrix of a linear $T$ | Thm 1.7 | $A=[\,T(\mathbf e_1)\ \cdots\ T(\mathbf e_n)\,]$, unique |
| Convert $\mathcal B$-coordinates to $\mathcal C$-coordinates | change of basis | $[\mathbf x]_{\mathcal C}=P_{\mathcal C\leftarrow\mathcal B}[\mathbf x]_{\mathcal B}$, with $P_{\mathcal C\leftarrow\mathcal B}=P_{\mathcal C}^{-1}P_{\mathcal B}$ |
| Convert coordinates to the standard basis | $P_{\mathcal B}=[\mathbf b_1\ \cdots\ \mathbf b_n]$ | $\mathbf x=P_{\mathcal B}[\mathbf x]_{\mathcal B}$ |
| Find the $\mathcal B$-matrix of $T$ | 9.9 | $[T]_{\mathcal B}=P_{\mathcal B}^{-1}AP_{\mathcal B}$ |
| Recognize the same transformation in two bases | similarity | similar matrices |
| Understand diagonalization | change of basis | $D=P^{-1}AP$ is $A$ in an eigenvector basis |
| Understand the DFT | change of basis | $X[k]=\langle\mathbf w_k,\mathbf x\rangle$ are Fourier-basis coordinates |

### 1.8 Complex numbers and the DFT

| Goal | Reach for | What you get |
|---|---|---|
| Add/multiply/divide complex numbers | rectangular form; multiply by conjugate to divide | result |
| Compute powers | Euler / De Moivre | $z^n=r^n(\cos n\theta+j\sin n\theta)$ |
| Find $n$-th roots | roots formula | $n$ equally spaced roots on a circle of radius $\sqrt[n]{r}$ |
| Guarantee roots exist | Fundamental Theorem of Algebra | exactly $n$ complex roots counted with multiplicity |
| Complex length / orthogonality | $\langle\mathbf a,\mathbf b\rangle=\mathbf a^{H}\mathbf b$ | norm and orthogonality; conjugate symmetry |
| Get an orthogonal basis of $\mathbb C^N$ | Fourier basis $\mathbf w_k$ | $\langle\mathbf w_k,\mathbf w_m\rangle=N\delta_{km}$ |
| Compute DFT / IDFT | DFT formulas; DFT matrix $W$ | $X[k]$, $x[n]$; $W^{-1}=\tfrac1N\overline W$ |
| Check energy or sampling limits | Parseval / aliasing | energy preserved; frequencies $k$ and $k+N$ indistinguishable |

---

## 2. Object → What it tells you

Use this when you have **already computed something** and want to know what it unlocks.

| Object you have | What it tells you | Backing result |
|---|---|---|
| RREF of $A$ | pivot positions/columns, free variables, rank, dependence relations among columns, row-space basis (nonzero rows) | row reduction; Thm 4.6–4.8 |
| RREF of $[A \mid \mathbf b]$ | consistency (no $[0\ \cdots\ 0 \mid c]$, $c\neq0$), leading/free variables, full solution set | Thm 1.1; §8.1 |
| RREF of $[A \mid I]$ | if the left block becomes $I$, the right block is $A^{-1}$; otherwise $A$ is singular | Thm 2.3 |
| number of pivots of an $n\times n$ $A$ | $n$ pivots $\iff$ invertible; fewer $\Rightarrow$ singular; rank = pivot count | IMT |
| pivot columns of $A$ | basis of $\operatorname{Col}A$ — use the columns of $A$, **not** the RREF | Thm 4.6 |
| free variables of $A\mathbf x=\mathbf 0$ | nullity; each free variable produces a basis vector of $N(A)$ | Rank Theorem |
| $\operatorname{rank}A$ | $\dim\operatorname{Col}A=\dim\operatorname{Row}A=$ number of independent columns $=$ number of independent rows; nullity $=n-\operatorname{rank}A$ | Thm 4.8 |
| $\det A$ | invertible $\iff\det A\neq0$; $\lvert\det A\rvert$ = area/volume scale; $\prod\lambda_i$; $\det A=0\Rightarrow$ singular | det properties; Thm 3.1–3.2; §9.1 |
| $\operatorname{tr}A$ | $\sum\lambda_i$ (with multiplicity) | §9.1 |
| $A^{\mathsf T}A$ | invertible $\iff$ columns of $A$ are independent; central in normal equations and projection | Thm 6.5.1 |
| $A^{\mathsf T}$ | same eigenvalues as $A$; same rank; $N(A^{\mathsf T})=(\operatorname{Col}A)^\perp$ | §9.4; §8.4 |
| $A^{-1}$ | unique solution $\mathbf x=A^{-1}\mathbf b$; $\det(A^{-1})=1/\det A$; eigenvalues $1/\lambda$ | Thm 2.1–2.2; §9.4 |
| eigenvalue $\lambda$ | $A-\lambda I$ singular; eigenvector direction is invariant; growth rate in dynamics; $\lambda=0\Rightarrow$ singular | §9.1 |
| eigenspace $E_\lambda$ | all eigenvectors for $\lambda$ plus $\mathbf 0$; its dimension is the geometric multiplicity | §9.2 |
| algebraic multiplicity | an upper bound on the geometric multiplicity; multiplicities total $n$ over $\mathbb C$ | §9.2–9.3 |
| geometric multiplicity | number of independent eigenvectors for $\lambda$; equality with algebraic multiplicity $\iff$ diagonalizable | §9.5 |
| characteristic polynomial | roots are the eigenvalues; degree $n$; similarity invariant | §9.3, §9.7 |
| eigenvector matrix $P$ | $A=PDP^{-1}$ when its columns are independent; change to an eigenbasis | §9.5 |
| diagonal $D$ | eigenvalues on the diagonal; $D^k$ is trivial to compute | §9.5, §9.8 |
| an orthogonal set (all nonzero) | automatically linearly independent; coordinates are dot-product quotients | Thm 4; Thm 5 |
| orthonormal matrix $U$ | $U^{\mathsf T}U=I$; if square, $U^{-1}=U^{\mathsf T}$; in all cases $\lVert U\mathbf x\rVert=\lVert\mathbf x\rVert$ | Thm 6 |
| projection matrix $P$ | $P^2=P$, $P^{\mathsf T}=P$; $P\mathbf b\in W$; $I-P$ projects onto $W^\perp$ | §8.4 |
| residual $\mathbf b-A\hat{\mathbf x}$ | orthogonal to $\operatorname{Col}A$; zero iff the system is exact; its length measures fit | Thm 6.5.1; §8.6 |
| $Q,R$ in $A=QR$ | $Q$ is an orthonormal basis of $\operatorname{Col}A$; $R$ is upper triangular invertible; solve $R\mathbf x=Q^{\mathsf T}\mathbf b$ | QR theorem |
| $L,U$ in $A=LU$ | solve $L\mathbf y=\mathbf b$, then $U\mathbf x=\mathbf y$; $\det A=\pm\prod u_{ii}$ | LU facts |
| row space | dimension $=\operatorname{rank}A$; unchanged by row operations; basis = nonzero rows of REF | Thm 4.7 |
| column space | dimension $=\operatorname{rank}A$; basis = pivot columns of $A$; $A\mathbf x=\mathbf b$ consistent $\iff\mathbf b\in\operatorname{Col}A$ | Thm 4.3, 4.6 |
| $N(A)$ | solution set of $A\mathbf x=\mathbf 0$; subspace of $\mathbb R^n$; dimension = nullity | Rank Theorem |
| $N(A^{\mathsf T})$ | $(\operatorname{Col}A)^\perp$; where the least-squares residual lives | §8.4 |
| $W^\perp$ | vectors orthogonal to all of $W$; $\dim W^\perp=n-\dim W$; $\mathbb R^n=W\oplus W^\perp$ | Thm 5 |
| $[\mathbf x]_{\mathcal B}$ | coordinates of $\mathbf x$ in basis $\mathcal B$; $\mathbf x=P_{\mathcal B}[\mathbf x]_{\mathcal B}$ | change of basis |
| $P_{\mathcal C\leftarrow\mathcal B}$ | converts $\mathcal B$-coordinates to $\mathcal C$-coordinates; equals $P_{\mathcal C}^{-1}P_{\mathcal B}$ | change of basis |
| Fourier coefficients $X[k]$ | coordinates of the signal in the Fourier basis; magnitude indicates frequency content | §10.5–10.6 |

---

## 3. Condition → Conclusion

### 3.1 Exact equivalences (either direction is valid)

**For an $n\times n$ matrix $A$, all of the following are the same statement:**

$$A\text{ invertible}\iff \det A\neq0\iff \operatorname{rank}A=n\iff \text{RREF}(A)=I_n\iff A\text{ has }n\text{ pivots}$$
$$\iff N(A)=\{\mathbf 0\}\iff A\mathbf x=\mathbf 0\text{ has only the trivial solution}\iff \text{columns of }A\text{ are independent}$$
$$\iff \text{columns of }A\text{ form a basis of }\mathbb R^n\iff \text{rows of }A\text{ form a basis of }\mathbb R^n$$
$$\iff A\mathbf x=\mathbf b\text{ has a unique solution for every }\mathbf b\iff 0\text{ is not an eigenvalue of }A\iff A^{\mathsf T}\text{ is invertible}.$$

**Other exact equivalences used constantly:**

| Statement A | Equivalent statement(s) |
|---|---|
| $A\mathbf x=\mathbf 0$ has a nontrivial solution | columns of $A$ are dependent $\iff$ nullity $>0$ $\iff$ some variable is free |
| $A\mathbf x=\mathbf b$ is consistent | $\mathbf b\in\operatorname{Col}A$ $\iff$ $\operatorname{rank}A=\operatorname{rank}[A \mid \mathbf b]$ $\iff$ no pivot in the augmented column |
| $A\mathbf x=\mathbf b$ is solvable for **every** $\mathbf b\in\mathbb R^m$ | every row has a pivot $\iff$ $\operatorname{Col}A=\mathbb R^m$ $\iff$ $\operatorname{rank}A=m$ $\iff$ columns span $\mathbb R^m$ |
| $\lambda$ is an eigenvalue of $A$ | $\det(A-\lambda I)=0$ $\iff$ $A-\lambda I$ is singular $\iff$ $(A-\lambda I)\mathbf x=\mathbf 0$ has a nontrivial solution |
| $A$ is diagonalizable | $A$ has $n$ linearly independent eigenvectors $\iff$ geometric = algebraic multiplicity for every eigenvalue $\iff$ $A=PDP^{-1}$ |
| $A^{\mathsf T}A$ is invertible | the columns of $A$ are linearly independent |
| $U$ has orthonormal columns | $U^{\mathsf T}U=I$ |
| $U$ is square with orthonormal columns | $U$ is orthogonal, $U^{-1}=U^{\mathsf T}$, and $\det U=\pm1$ |
| two matrices are similar | they represent the same linear transformation in two bases |

### 3.2 One-way implications (do not reverse them)

| If you know… | Then you can conclude… | Why |
|---|---|---|
| a set has more than $n$ vectors in $\mathbb R^n$ | it is linearly **dependent** | Thm 1.5 |
| a set contains $\mathbf 0$ | it is linearly **dependent** | Thm 1.6 |
| a set is **orthogonal** and all vectors are nonzero | it is linearly **independent** | Thm 4 |
| $A$ has **distinct** eigenvalues | its eigenvectors are independent, so $A$ is diagonalizable | §9.6 |
| $A$ has independent columns ($m\times n$) | $\operatorname{rank}A=n$, $A^{\mathsf T}A$ invertible, and the least-squares solution is **unique** | Rank Theorem; Thm 6.5.1 |
| $\operatorname{rank}A=m$ | the columns span $\mathbb R^m$, so $A\mathbf x=\mathbf b$ is consistent for every $\mathbf b$ | Thm 1.2 |
| $\operatorname{rank}A=n$ | the columns are independent, so a solution is unique **if it exists** | Rank Theorem |
| $m<n$ and the system is consistent | **infinitely many** solutions | free variables |
| $m>n$ | $A$ cannot span $\mathbb R^m$; the system is not solvable for every $\mathbf b$ | counting rule |
| $A$ is triangular | its eigenvalues are the diagonal entries; $\det A$ is their product | §9.4; det property 7 |
| $A$ is similar to $B$ | same characteristic polynomial, eigenvalues, determinant, and trace | §9.7 |
| $A$ is invertible (hence square) | $A^{\mathsf T}A$ is invertible | $\det(A^{\mathsf T}A)=(\det A)^2\neq0$ |
| $\mathbf b\in\operatorname{Col}A$ | the least-squares residual is $\mathbf 0$; the LS solution is exact | §8.6 |
| $\lambda=0$ is an eigenvalue | $A$ is singular | §9.1 |
| $A$ is real and has a non-real eigenvalue | it also has the conjugate eigenvalue; geometry is rotation–scaling | §9.11 |
| $U$ is orthogonal | lengths and dot products are preserved; $\det U=\pm1$ | Thm 6 |
| $P$ is a projection matrix | $I-P$ is the projection onto the orthogonal complement | §8.4 |
| $A=QR$ with independent columns | $R$ is invertible, so the LS solution is unique | QR theorem |
| row operations are applied to $A$ | the **row space** and **null space** are unchanged; the **column space is not** | Thm 4.7 |

### 3.3 "Enough" vs "not enough"

| You might think… | Reality |
|---|---|
| "independent $\Rightarrow$ orthogonal" | **False.** Independence says nothing about angles. Orthogonal $\Rightarrow$ independent only when no vector is $\mathbf 0$. |
| "$p\le n$ $\Rightarrow$ independent" | **False.** You need an actual pivot in every column. |
| "$\operatorname{rank}=n$ $\Rightarrow$ invertible" | Only if the matrix is **square**. For $m\times n$, rank $n$ means independent columns, not invertibility. |
| "$\operatorname{rank}=m$ $\Rightarrow$ independent columns" | Only if $m=n$. Rank $m$ means the columns span $\mathbb R^m$. |
| "repeated eigenvalue $\Rightarrow$ not diagonalizable" | **False.** Check whether geometric = algebraic multiplicity. |
| "diagonalizable $\Rightarrow$ distinct eigenvalues" | **False.** $I$ is diagonalizable with one repeated eigenvalue. |
| "similar matrices have the same eigenvectors" | **False.** Eigenvectors transform by $P$: $\mathbf v\mapsto P\mathbf v$. |
| "eigenvalues of $A+B$ are $\lambda_A+\lambda_B$" | **False** in general. |
| "eigenvalues of $AB$ are $\lambda_A\lambda_B$" | **False** in general. |
| "$\det(A+B)=\det A+\det B$" | **False** in general. |
| "row reduction preserves the column space" | **False.** It preserves the **row space** and **null space**; use pivot columns of the original $A$ for $\operatorname{Col}A$. |
| "least-squares solutions are always unique" | **False.** They always exist, but are unique only when the columns of $A$ are independent. |

---

## 4. Theorem-by-theorem payload

The compact version of every named result: **what you supply $\to$ what you get $\to$ what it is for**.

### Part I–II — Vector and matrix algebra

| Theorem | If you have… | You get… | Use it for… |
|---|---|---|---|
| Vector operation laws | vectors in $\mathbb R^n$, scalars | commutativity, associativity, distributivity, identities, inverses | rearranging vector expressions |
| Zero/scalar laws | $\mathbf v$, $k$ | $0\mathbf v=\mathbf 0$, $k\mathbf 0=\mathbf 0$, $(-1)\mathbf v=-\mathbf v$ | simplifying expressions |
| Norm properties (3.2.1) | $\mathbf v$, $k$ | $\lVert\mathbf v\rVert\ge0$; $\lVert\mathbf v\rVert=0\iff\mathbf v=\mathbf 0$; $\lVert k\mathbf v\rVert=\lvert k\rvert\lVert\mathbf v\rVert$ | lengths, unit vectors, distance |
| Dot-product properties (3.2.3) | $\mathbf u,\mathbf v,\mathbf w$, $k$ | symmetry, distributivity, homogeneity, positivity, $\mathbf v\cdot\mathbf v=\lVert\mathbf v\rVert^2$ | expanding dot products; deriving norms |
| Cauchy–Schwarz (3.2.4) | $\mathbf u,\mathbf v$ | $\lvert\mathbf u\cdot\mathbf v\rvert\le\lVert\mathbf u\rVert\lVert\mathbf v\rVert$ | bounding dot products; defining angles; proving the triangle inequality |
| Triangle inequality (3.2.5) | $\mathbf u,\mathbf v$ | $\lVert\mathbf u+\mathbf v\rVert\le\lVert\mathbf u\rVert+\lVert\mathbf v\rVert$; distance version | distance bounds |
| Matrix algebra | conformable matrices | associativity, distributivity, non-commutativity, $(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}$ | manipulating matrix expressions |
| Matrix–vector product | $A$, $\mathbf x$ | $A\mathbf x$ is a linear combination of the columns of $A$ | converting system $\leftrightarrow$ vector equation; columns of $AB$ |

### Part III–V — Systems, matrix algebra, determinants

| Theorem | If you have… | You get… | Use it for… |
|---|---|---|---|
| **1.1** Three forms | $A$, $\mathbf b$ | $A\mathbf x=\mathbf b$ $\iff$ vector equation $\iff$ augmented matrix; same solution set | switching representations freely |
| **1.2** Four equivalents | $m\times n$ $A$ | solvable for all $\mathbf b$ $\iff$ every $\mathbf b$ is a column combination $\iff$ columns span $\mathbb R^m$ $\iff$ pivot in every row | consistency-for-all test; spanning test |
| **1.3** Linearity of $A\mathbf x$ | $A$, $\mathbf u,\mathbf v$, $c$ | $A(\mathbf u+\mathbf v)=A\mathbf u+A\mathbf v$; $A(c\mathbf u)=cA\mathbf u$ | proving linearity; superposing solutions |
| **1.4** Solution-set structure | consistent $A\mathbf x=\mathbf b$, one particular $\mathbf p$ | solution set $=\mathbf p+N(A)$ | writing the general solution; separating particular and homogeneous parts |
| **1.5** Too many vectors | $p$ vectors in $\mathbb R^n$ with $p>n$ | linearly dependent | instant dependence test |
| **1.6** Zero vector | a set containing $\mathbf 0$ | linearly dependent | instant dependence test |
| **1.7** Standard matrix | linear $T$ | unique $A=[\,T(\mathbf e_1)\ \cdots\ T(\mathbf e_n)\,]$ with $T(\mathbf x)=A\mathbf x$ | building rotation/projection/etc. matrices |
| **2.1** Unique solution | invertible $A$ | $\mathbf x=A^{-1}\mathbf b$ is the unique solution | solving systems; deriving formulas |
| **2.2** Inverse laws | invertible $A,B$ | $(A^{-1})^{-1}=A$, $(AB)^{-1}=B^{-1}A^{-1}$, $(A^{\mathsf T})^{-1}=(A^{-1})^{\mathsf T}$ | solving and simplifying matrix equations |
| **2.3** Invertible $\iff$ RREF $=I$ | $n\times n$ $A$ | $[A \mid I]\to[I \mid A^{-1}]$ | computing inverses; testing invertibility |
| **2.4** IMT | $n\times n$ $A$ | ten statements all equivalent | replacing a hard test by the easiest equivalent one |
| LU facts | $A$ reducible without swaps (or any $A$ with a permutation $P$) | $A=LU$, or $PA=LU$ | repeated solves; determinant from $U$ |
| **3.1** Determinant as area/volume | $2\times2$ or $3\times3$ $A$ | $\lvert\det A\rvert$ = area/volume determined by the columns | geometry of determinants |
| **3.2** Scaling area/volume | linear $T_A$, region $S$ | area/volume of $T(S)=\lvert\det A\rvert\times$ area/volume of $S$ | transformation geometry |
| Determinant properties | square $A$ | row-operation effects, triangular product, $\det(AB)=\det A\det B$, singular $\iff\det=0$ | efficient computation; singularity tests |

### Part VI — Vector spaces

| Theorem | If you have… | You get… | Use it for… |
|---|---|---|---|
| **4.1** Span is a subspace | vectors in $V$ | $\operatorname{Span}\{\mathbf v_i\}$ is a subspace | proving a set is a subspace by exhibiting it as a span |
| Null space is a subspace | $m\times n$ $A$ | $N(A)$ is a subspace of $\mathbb R^n$ | structure of homogeneous solution sets |
| **4.3** Column space is a subspace | $A$ | $\operatorname{Col}A$ is a subspace of $\mathbb R^m$; $\operatorname{Col}A=\mathbb R^m\iff$ consistent for all $\mathbf b$ | consistency geometry |
| **4.4** Dependence characterization | $\mathbf v_1,\dots,\mathbf v_p$, $\mathbf v_1\neq\mathbf 0$ | dependent $\iff$ some $\mathbf v_j$ is a combination of the preceding vectors | detecting redundancy; building a basis incrementally |
| **4.5** Spanning Set Theorem | $S$ spans $H$ | removing a vector that is a combination of the others still spans $H$; some subset of $S$ is a basis | trimming a spanning set to a basis |
| **4.6** Pivot columns | $A$ | pivot columns of $A$ form a basis for $\operatorname{Col}A$ | finding a column-space basis without guessing |
| **4.7** Row equivalence | $A$ row-equivalent to $B$ | same row space; nonzero rows of an echelon form give a basis | row-space basis; rank |
| **4.8** Rank Theorem | $A$ with $n$ columns | $\operatorname{rank}A+\dim N(A)=n$ | getting nullity from rank; dimension counting |
| IMT continued | invertible $n\times n$ $A$ | $\operatorname{rank}A=n$, $N(A)=\{\mathbf 0\}$ | confirming full rank |
| Change of basis | bases $\mathcal B,\mathcal C$ | unique $P_{\mathcal C\leftarrow\mathcal B}$ with $[\mathbf x]_{\mathcal C}=P_{\mathcal C\leftarrow\mathcal B}[\mathbf x]_{\mathcal B}$ | coordinate conversion; similarity |

### Part VII — Orthogonality

| Theorem | If you have… | You get… | Use it for… |
|---|---|---|---|
| **3.3.1** Point–normal form | point $P_0$, normal $\mathbf n$ | $\mathbf n\cdot\overrightarrow{P_0P}=0$; coefficients of the variables are the normal components | writing line/plane equations; reading off a normal |
| **Thm 4** Orthogonal $\Rightarrow$ independent | orthogonal set of nonzero vectors | linearly independent; $p\le n$ | free independence; orthogonal bases |
| **3.3.2** Projection theorem | $\mathbf u$, $\mathbf a\neq\mathbf 0$ | unique $\mathbf u=\operatorname{proj}_{\mathbf a}\mathbf u+\mathbf e$ with $\mathbf e\perp\mathbf a$; formula $\dfrac{\mathbf u\cdot\mathbf a}{\mathbf a\cdot\mathbf a}\mathbf a$ | component along a direction; decomposing a vector |
| **Thm 5** Orthogonal decomposition | subspace $W$, vector $\mathbf y$ | unique $\mathbf y=\hat{\mathbf y}+\mathbf z$, $\hat{\mathbf y}\in W$, $\mathbf z\in W^\perp$ | splitting a vector; defining orthogonal complements |
| **Thm 8** Projection, orthogonal basis | orthogonal basis $\{\mathbf u_j\}$ of $W$ | $\hat{\mathbf y}=\sum_j\dfrac{\mathbf y\cdot\mathbf u_j}{\mathbf u_j\cdot\mathbf u_j}\mathbf u_j$ | computing projections without solving a system |
| **Thm 9** Best approximation | $W$, $\mathbf y$, projection $\hat{\mathbf y}$ | $\hat{\mathbf y}$ is the unique closest point; strict inequality for all other $\mathbf v\in W$ | distance to a subspace; justification of least squares |
| **Thm 10** Projection, orthonormal basis | orthonormal basis of $W$ | $\operatorname{proj}_W\mathbf y=UU^{\mathsf T}\mathbf y$ | fast projection; projection matrices |
| **Thm 6** $U^{\mathsf T}U=I$ | $m\times n$ $U$ | orthonormal columns $\iff U^{\mathsf T}U=I$; square $\Rightarrow U^{-1}=U^{\mathsf T}$; always $\lVert U\mathbf x\rVert=\lVert\mathbf x\rVert$ | testing orthonormality; inverting orthogonal matrices |
| **Thm 11** Gram–Schmidt | basis $\mathbf x_1,\dots,\mathbf x_p$ | orthogonal basis $\mathbf v_1,\dots,\mathbf v_p$ with the same nested spans; normalize for orthonormal | orthonormalization; QR |
| QR theorem | $A$ with independent columns | $A=QR$, $Q$ orthonormal columns, $R$ upper triangular invertible | stable least squares; column-space basis |

### Part VIII — Least squares

| Theorem | If you have… | You get… | Use it for… |
|---|---|---|---|
| Consistency criteria | $A$, $\mathbf b$ | consistent $\iff\mathbf b\in\operatorname{Col}A\iff\operatorname{rank}A=\operatorname{rank}[A \mid \mathbf b]\iff$ no pivot in the augmented column | classifying systems |
| **6.4.1** Best approximation | $W$, $\mathbf y$ | projection is the closest point; residual orthogonal to $W$ | deriving least squares geometrically |
| **6.5.1** Normal equations | $A$, $\mathbf b$ | LS solutions $=$ solutions of $A^{\mathsf T}A\hat{\mathbf x}=A^{\mathsf T}\mathbf b$; if columns independent, $\hat{\mathbf x}=(A^{\mathsf T}A)^{-1}A^{\mathsf T}\mathbf b$ | computing least-squares fits |
| Projection-matrix properties | $P=A(A^{\mathsf T}A)^{-1}A^{\mathsf T}$ | $P^2=P$, $P^{\mathsf T}=P$, $P\mathbf b\in\operatorname{Col}A$, $\mathbf b-P\mathbf b\perp\operatorname{Col}A$, $I-P$ projects onto $N(A^{\mathsf T})$ | verifying and using projections |
| Three solution routes | over-determined $A\mathbf x=\mathbf b$ | normal equations, QR, and projection give the same $\hat{\mathbf x}$ | choosing a method |
| Residual/error | $\mathbf r=\mathbf b-A\hat{\mathbf x}$ | $A^{\mathsf T}\mathbf r=\mathbf 0$; $\lVert\mathbf b\rVert^2=\lVert\hat{\mathbf b}\rVert^2+\lVert\mathbf r\rVert^2$ | measuring fit; exact solution when $\mathbf b\in\operatorname{Col}A$ |
| Linear models | data points $(x_i,y_i)$ | design matrix $A$; coefficients solve $A^{\mathsf T}A\boldsymbol\beta=A^{\mathsf T}\mathbf y$ | fitting lines, polynomials, and other linear-in-parameters models |

### Part IX — Eigenvalues and eigenvectors

| Theorem | If you have… | You get… | Use it for… |
|---|---|---|---|
| **9.1** Eigenvalue equation | square $A$, scalar $\lambda$ | $\lambda$ eigenvalue $\iff\det(A-\lambda I)=0\iff A-\lambda I$ singular $\iff$ nontrivial nullspace | finding eigenvalues; singularity tests |
| **9.2** Eigenspaces | eigenvalue $\lambda$ | $E_\lambda=N(A-\lambda I)$ is a subspace; $1\le\dim E_\lambda\le$ algebraic multiplicity; different eigenvalues give independent eigenvectors | building an eigenvector basis |
| **9.3** Characteristic equation | $A$ | degree-$n$ polynomial; $n$ eigenvalues over $\mathbb C$; triangular $\Rightarrow$ diagonal entries; zero eigenvalue $\Rightarrow$ singular | counting and finding eigenvalues |
| **9.4** Eigenvalue shortcuts | $A$ | triangular/diagonal $\to$ diagonal; $A^k\to\lambda^k$; $A^{-1}\to1/\lambda$; $A^{\mathsf T}$ same | avoiding the characteristic polynomial |
| **9.5** Diagonalization | $A$ | diagonalizable $\iff n$ independent eigenvectors $\iff$ geometric $=$ algebraic; $A=PDP^{-1}$ | powers, dynamics, simplification |
| **9.6** Distinct eigenvalues | eigenvectors for distinct $\lambda$ | linearly independent; $n$ distinct $\Rightarrow$ diagonalizable | quick diagonalizability test |
| **9.7** Similarity | $A=PBP^{-1}$ | same characteristic polynomial, eigenvalues, determinant, trace | identifying basis-independent invariants |
| **9.8** Powers | $A=PDP^{-1}$ | $A^k=PD^kP^{-1}$ | discrete dynamical systems, long-run behavior |
| **9.9** Eigenvalues of $T$ | linear $T$, basis $\mathcal B$ | $[T]_{\mathcal B}=P_{\mathcal B}^{-1}AP_{\mathcal B}$; diagonal iff $\mathcal B$ is an eigenbasis | basis-free transformation analysis |
| **9.10** Change of basis | bases $\mathcal B,\mathcal C$ | coordinate conversion; similarity $=$ same transformation | converting representations |
| **9.11** Complex eigenvalues | real $A$ | conjugate pairs $a\pm bj$; rotation–scaling; diagonalizable only over $\mathbb C$ | 2×2 rotation/oscillation analysis |

### Part X — Complex numbers and the DFT

| Theorem | If you have… | You get… | Use it for… |
|---|---|---|---|
| Complex arithmetic | $z_1,z_2$ | $z\bar z=\lvert z\rvert^2$, $1/z=\bar z/\lvert z\rvert^2$, conjugate/modulus laws | computation and division |
| Fundamental Theorem of Algebra | polynomial of degree $n$ | exactly $n$ complex roots counted with multiplicity | guaranteeing eigenvalues exist over $\mathbb C$ |
| Euler / De Moivre | $z=r\angle\theta$ | $e^{j\theta}=\cos\theta+j\sin\theta$; $z^n=r^n\angle n\theta$ | powers, roots, trigonometric identities |
| Roots theorem | $z^n=r\angle\theta$ | $n$ equally spaced roots of radius $\sqrt[n]{r}$ | solving $z^n=w$ |
| Complex inner product | $\mathbf a,\mathbf b$ | conjugate symmetry, linearity, positivity; $\lVert\mathbf a\rVert^2=\mathbf a^{H}\mathbf a$ | complex norms, orthogonality, projection |
| Fourier-basis orthogonality | $\mathbf w_k$ | $\langle\mathbf w_k,\mathbf w_m\rangle=N\delta_{km}$ | orthogonal basis of $\mathbb C^N$; DFT interpretation |
| DFT/IDFT | signal $\mathbf x$ | $X[k]=\langle\mathbf w_k,\mathbf x\rangle$; inverse formula; $W^{-1}=\tfrac1N\overline W$ | frequency analysis; change of basis |
| Parseval / aliasing | $\mathbf x$, $X$ | energy equality; frequencies $k$ and $k+N$ indistinguishable | checking transforms; sampling limits |

---

## 5. Converse traps

These are the mistakes that cost the most marks. Every entry is a **false converse** or a **misapplied theorem**.

| Trap | Correction |
|---|---|
| Independent $\Rightarrow$ orthogonal | **No.** Independent vectors can be at any angle. Orthogonal nonzero $\Rightarrow$ independent, not the reverse. |
| Orthogonal set may contain $\mathbf 0$ | **No.** A zero vector is orthogonal to everything and makes the set dependent. State "orthogonal **nonzero** vectors" for the independence conclusion. |
| $p\le n$ $\Rightarrow$ independent | **No.** You need a pivot in every column. |
| $\operatorname{rank}=n$ $\Rightarrow$ $A$ invertible | Only for **square** $A$. For rectangular $A$, rank $n$ means independent columns. |
| $\operatorname{rank}=m$ $\Rightarrow$ independent columns | Only if $m=n$. Rank $m$ means the columns span $\mathbb R^m$. |
| Repeated eigenvalue $\Rightarrow$ not diagonalizable | **No.** Check geometric vs algebraic multiplicity. |
| Diagonalizable $\Rightarrow$ distinct eigenvalues | **No.** $I_n$ is diagonalizable with a single repeated eigenvalue. |
| Similar matrices share eigenvectors | **No.** They share eigenvalues, determinant, trace, and characteristic polynomial; eigenvectors map by $P$. |
| $\lambda(A+B)=\lambda(A)+\lambda(B)$ | **No** in general. |
| $\lambda(AB)=\lambda(A)\lambda(B)$ | **No** in general. |
| $\det(A+B)=\det A+\det B$ | **No** in general. |
| Row operations preserve $\operatorname{Col}A$ | **No.** They preserve the row space and null space. Use the pivot columns of the **original** $A$ for a column-space basis. |
| Pivot columns of the RREF give a basis for $\operatorname{Col}A$ | **No.** They tell you *which* columns of $A$ to take; the basis vectors are those columns of $A$. |
| Least-squares solutions are always unique | **No.** They always exist; uniqueness requires independent columns. |
| $A^{\mathsf T}A$ invertible requires $A$ invertible | **No.** It is equivalent to **independent columns**; a tall matrix can have this property without being invertible. |
| Projection matrix $P$ is invertible | **No** unless $P=I$. $P^2=P$ forces eigenvalues $0$ and $1$; a proper projection has a nontrivial null space. |
| Orthogonal matrix means "entries are orthogonal" | **No.** It means the columns (and rows) are **orthonormal**. |
| Cauchy–Schwarz can be equality for any vectors | Equality holds only when $\mathbf u,\mathbf v$ are parallel (one is a scalar multiple of the other). |
| Gram–Schmidt can start from any spanning set | It is stated for a **basis**; for a spanning set, first discard dependent vectors. |

---

## 6. Question → Immediate move

A last-pass translation table for exams.

| The question says… | Do this first |
|---|---|
| "for every $\mathbf b$" | pivot in every row $\leftrightarrow$ columns span $\mathbb R^m$ $\leftrightarrow \operatorname{rank}=m$ (Thm 1.2) |
| "only the trivial solution" | columns independent $\leftrightarrow$ pivot in every column $\leftrightarrow$ nullity $0$ |
| "unique solution" | square: IMT; general: independent columns + consistency |
| "infinitely many solutions" | find a free variable; write $\mathbf p+N(A)$ (Thm 1.4) |
| "no solution" | show a pivot in the augmented column, or $\operatorname{rank}[A \mid \mathbf b]>\operatorname{rank}A$ |
| "find a basis" | $\operatorname{Col}A$: pivot columns; $\operatorname{Row}A$: nonzero REF rows; $N(A)$: free-variable vectors; $W=\operatorname{Span}\{\mathbf v_i\}$: pivot columns of the matrix with those vectors as columns |
| "find the dimension" | $\operatorname{rank}$ for column/row space; nullity for $N(A)$; $n-\dim W$ for $W^\perp$ |
| "closest point", "best approximation", "least squares" | project onto $W$ (Thm 9); solve normal equations or $R\mathbf x=Q^{\mathsf T}\mathbf b$ |
| "orthogonal" or "orthonormal" | dot products; Gram–Schmidt; $U^{\mathsf T}U=I$ |
| "area" or "volume" | determinant (Thm 3.1/3.2) |
| "diagonalizable" | count independent eigenvectors; compare geometric/algebraic multiplicities |
| "compute $A^k$" | diagonalize: $A^k=PD^kP^{-1}$ |
| "similar" | change of basis; same characteristic polynomial/eigenvalues/det/trace |
| "change of basis" | $P_{\mathcal C\leftarrow\mathcal B}=P_{\mathcal C}^{-1}P_{\mathcal B}$ |
| "complex eigenvalues of a real matrix" | conjugate pair; rotation–scaling; not diagonalizable over $\mathbb R$ |
| "frequency content", "DFT" | coordinates in the Fourier basis; $X[k]=\langle\mathbf w_k,\mathbf x\rangle$ |

---

*Companion files: [theorems.md](theorems.md) for full statements and proofs · [definitions.md](definitions.md) for terminology · [practice_problems.md](practice_problems.md) for drills.*
