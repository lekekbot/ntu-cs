# SC1004 Linear Algebra — Definitions Glossary (One-Page)

> Quick-scan reference of every key term from the course. For the full theory + theorems + proofs, see `theorems.md`.

---

## Vectors

| Term | Definition |
|---|---|
| **Scalar** | A quantity with magnitude only (a number). |
| **Vector** | A quantity with magnitude **and** direction; written $\mathbf v$ / $\vec v$. |
| **Equal / equivalent vectors** | Same length and same direction ($\mathbf v = \mathbf w$); position is irrelevant. |
| **Zero vector $\mathbf 0$** | The vector with zero length (initial = terminal point). |
| **Negative $-\mathbf v$** | Same length as $\mathbf v$, opposite direction. |
| **Vector addition** | Parallelogram rule or triangle rule; $\mathbf u + \mathbf v = \mathbf v + \mathbf u$. |
| **Vector subtraction** | $\mathbf w - \mathbf v = \mathbf w + (-\mathbf v)$. |
| **Scalar multiplication $k\mathbf v$** | Length $|k|\|\mathbf v\|$; direction same/opposite if $k>0$/$k<0$. |
| **Parallel / collinear** | One vector is a scalar multiple of the other. |
| **Components** | $\mathbf v = (v_1, v_2, \dots, v_n)$ relative to the coordinate axes. |
| **$\mathbb{R}^n$** | The set of all ordered $n$-tuples of real numbers. |
| **Linear combination** | $\mathbf w = c_1\mathbf v_1 + \cdots + c_p\mathbf v_p$; the $c_i$ are **weights**. |
| **Norm / length** | $\|\mathbf v\| = \sqrt{v_1^2 + \cdots + v_n^2}$. |
| **Unit vector** | A vector of norm 1; $\hat{\mathbf u} = \mathbf v/\|\mathbf v\|$. |
| **Normalizing** | Dividing a nonzero vector by its norm to get a unit vector. |
| **Standard unit vectors** | $\mathbf i=(1,0,0)$, $\mathbf j=(0,1,0)$, $\mathbf k=(0,0,1)$; in ℝⁿ: $\mathbf e_1,\dots,\mathbf e_n$. |
| **Distance** | $d(\mathbf u,\mathbf v) = \|\mathbf u - \mathbf v\|$. |
| **Dot product** | $\mathbf u\cdot\mathbf v = \|\mathbf u\|\|\mathbf v\|\cos\theta = \sum u_iv_i$ (a scalar). |
| **Orthogonal vectors** | $\mathbf u\cdot\mathbf v = 0$. |
| **Orthogonal set** | Every pair of distinct vectors is orthogonal. |
| **Normal vector** | A nonzero vector orthogonal to a line/plane (used in point-normal form). |
| **Span** | $\operatorname{Span}\{\mathbf v_1,\dots,\mathbf v_p\}$ = all linear combinations. |

## Matrices

| Term | Definition |
|---|---|
| **Matrix** | Rectangular array of numbers, $m$ rows × $n$ columns (size $m\times n$). |
| **Element $a_{ij}$** | Entry in row $i$, column $j$. |
| **Row / column vector** | A matrix with one row / one column. |
| **Square matrix (order $n$)** | $m = n$; diagonal entries $a_{11}, a_{22}, \dots, a_{nn}$. |
| **Main / leading diagonal** | The entries $a_{11}, a_{22}, \dots, a_{nn}$. |
| **Trace** | $\operatorname{tr}(A) = a_{11} + a_{22} + \cdots + a_{nn}$. |
| **Diagonal matrix** | Non-zero entries only on the leading diagonal. |
| **Unit / identity matrix $I$** | Diagonal matrix with all diagonal entries $1$; $IA = AI = A$. |
| **Transpose $A^T$** | Interchange rows and columns; $(A^T)^T = A$. |
| **Symmetric matrix** | $A^T = A$ (i.e. $a_{ij} = a_{ji}$). |
| **Skew-symmetric matrix** | $A^T = -A$ (i.e. $a_{ij} = -a_{ji}$). |
| **Matrix equality** | Same size and $a_{ij} = b_{ij}$ for all $i,j$. |
| **Addition / subtraction** | Element-wise (same size required). |
| **Scalar multiplication** | $(sA)_{ij} = s a_{ij}$. |
| **Matrix product $AB$** | $(AB)_{ij} = \sum_k a_{ik}b_{kj}$; needs #cols($A$) = #rows($B$). |
| **Coefficient matrix** | The matrix of coefficients $A$ of a linear system. |
| **Augmented matrix** | $[A \mid \mathbf b]$ = coefficient matrix with the right-hand side attached. |
| **Determinant (2×2)** | $\det\begin{bmatrix}a&b\\c&d\end{bmatrix} = ad - bc$. |
| **Inverse $A^{-1}$** | Satisfies $AA^{-1} = A^{-1}A = I$; exists iff $\det A \neq 0$. |
| **Invertible / singular** | Has an inverse / does not have an inverse ($\det = 0$). |

## Systems of Linear Equations

| Term | Definition |
|---|---|
| **Linear equation** | $a_1x_1 + \cdots + a_nx_n = b$, not all $a_i = 0$. |
| **Linear system** | $m$ linear equations in $n$ unknowns. |
| **Solution** | A tuple making every equation true. |
| **Solution set** | The set of all solutions. |
| **Consistent / inconsistent** | Has ≥ 1 solution / has no solution. |
| **Homogeneous / nonhomogeneous** | $A\mathbf x = \mathbf 0$ / $A\mathbf x = \mathbf b$, $\mathbf b \neq \mathbf 0$. |
| **Trivial / nontrivial solution** | $\mathbf x = \mathbf 0$ / a nonzero $\mathbf x$ (homogeneous case). |
| **Elementary Row Operation (ERO)** | ① multiply a row by nonzero constant; ② interchange rows; ③ add a multiple of one row to another. |
| **Row equivalent** | Reachable from each other by a sequence of EROs. |
| **Row Echelon Form (REF)** | Zero rows at bottom; each pivot to the right of the pivot above. |
| **Reduced Row Echelon Form (RREF)** | REF + pivots are 1 with zeros elsewhere in their column. |
| **Pivot / pivot position / pivot column** | First nonzero entry of a row / its location / its column. |
| **Leading variable / free variable** | Variable with a pivot / variable without a pivot (arbitrary). |
| **Gaussian elimination** | EROs to REF (forward phase; not unique). |
| **Gauss–Jordan elimination** | EROs to RREF (forward + backward; unique). |
| **Matrix equation $A\mathbf x = \mathbf b$** | $A\mathbf x = x_1\mathbf a_1 + \cdots + x_n\mathbf a_n$ (linear combination of columns). |
| **Spans $\mathbb{R}^m$** | $\operatorname{Span}\{\mathbf v_1,\dots,\mathbf v_p\} = \mathbb{R}^m$. |
| **Linearly independent set** | $c_1\mathbf v_1+\cdots+c_p\mathbf v_p = \mathbf 0$ only when all $c_i = 0$. |
| **Linearly dependent set** | Some $c_i \neq 0$ satisfies $c_1\mathbf v_1+\cdots+c_p\mathbf v_p = \mathbf 0$. |
| **Linear transformation $T$** | $T: \mathbb{R}^n \to \mathbb{R}^m$ with $T(\mathbf u+\mathbf v)=T(\mathbf u)+T(\mathbf v)$ and $T(c\mathbf u)=cT(\mathbf u)$. |
| **Domain / codomain** | $\mathbb{R}^n$ / $\mathbb{R}^m$ of $T:\mathbb{R}^n\to\mathbb{R}^m$. |
| **Image** | $T(\mathbf x)$, the output for input $\mathbf x$. |
| **Range** | The set of all images $T(\mathbf x)$. |
| **Standard matrix** | $A = [\,T(\mathbf e_1)\ \cdots\ T(\mathbf e_n)\,]$, so $T(\mathbf x) = A\mathbf x$. |

## Matrix Algebra (Chapter 2)

| Term | Definition |
|---|---|
| **Composition of transformations** | $A(B\mathbf x) = (AB)\mathbf x$: the product $AB$ means apply $B$ first, then $A$. |
| **Elementary matrix** | A matrix from performing **one** ERO on the identity; $EA$ performs that ERO on $A$. |
| **Inverse of an elementary matrix** | The elementary matrix of the same type that turns $E$ back into $I$. |
| **Permutation matrix** | Identity matrix with rows interchanged (used when row swaps are needed). |
| **Unit lower triangular matrix $L$** | Lower triangular with 1's on the main diagonal. |
| **Upper triangular matrix $U$** | Matrix with zeros below the main diagonal (echelon form). |
| **LU factorization** | Writing $A = LU$ ($L$ unit lower triangular, $U$ upper triangular). |
| **Forward substitution** | Solving $L\mathbf y = \mathbf b$ (top to bottom; $L$ is lower triangular). |
| **Backward substitution** | Solving $U\mathbf x = \mathbf y$ (bottom to top; $U$ is upper triangular). |

## Determinants (Chapter 3)

| Term | Definition |
|---|---|
| **Determinant $\det(A)$ / $\|A\|$** | A scalar attached to a square matrix; $2\times2$: $ad - bc$. |
| **Permutation matrix (det sign)** | Identity with rows interchanged; $\|P\| = (-1)^r$ for $r$ exchanges. |
| **Singular matrix** | Not invertible; a zero row appears under elimination ⇒ $\|A\| = 0$. |
| **Area as determinant** (Thm 3.1) | Area of parallelogram (columns of a $2\times2$ $A$) $= \|A\|$. |
| **Volume as determinant** (Thm 3.1) | Volume of parallelepiped (columns of a $3\times3$ $A$) $= \|A\|$. |
| **Area/volume scaling** (Thm 3.2) | $T$ given by $A$ scales area/volume by $\text{abs}(\|A\|)$; works for any shape. |

## Vector Spaces (Chapter 4)

| Term | Definition |
|---|---|
| **Vector space $V$** | Nonempty set of "vectors" with addition & scalar multiplication obeying the 10 axioms. |
| **Subspace $H$** | Subset of $V$ containing $\mathbf 0$, closed under + and scalar multiplication; itself a vector space. |
| **Span (subspace)** (Thm 4.1) | $\operatorname{Span}\{\mathbf v_1,\dots,\mathbf v_p\}$ = all linear combinations — a subspace. |
| **Null space $N(A)$** | All solutions of $A\mathbf x=\mathbf 0$; subspace of $\mathbb{R}^n$. |
| **Column space $C(A)$** | Span of the columns of $A$; subspace of $\mathbb{R}^m$ (Thm 4.3). |
| **Row space $C(A^T)$** | Span of the rows of $A$; subspace of $\mathbb{R}^n$. |
| **Kernel / range** | For $T(\mathbf x)=A\mathbf x$: kernel $=N(A)$, range $=C(A)$. |
| **Basis** | Linearly independent spanning set. |
| **Standard basis** | $\{\mathbf e_1,\dots,\mathbf e_n\}$ for $\mathbb{R}^n$; $\{1,t,\dots,t^n\}$ for $P_n$. |
| **Dimension** | $\dim V$ = number of vectors in a basis; $\dim\{\mathbf 0\}=0$; $\dim\mathbb{R}^n=n$; $\dim P_n=n+1$. |
| **Rank** | $\operatorname{rank} A = \dim C(A)$ = number of pivots (Rank Theorem: $\operatorname{rank}A+\dim N(A)=n$). |
| **Coordinate vector $[\mathbf x]_{\mathcal B}$** | The weights of $\mathbf x$ as a combination of basis vectors $\mathcal B$. |
| **Change-of-basis matrix** | $[\mathbf x]_{\mathcal C} = \mathop{P}\limits_{\mathcal C\leftarrow\mathcal B}[\mathbf x]_{\mathcal B}$; columns are $[\mathbf b_i]_{\mathcal C}$. |

## Orthogonality (Chapter 6)

| Term | Definition |
|---|---|
| **Norm $\|\mathbf v\|$** | Length / magnitude: $\sqrt{v_1^2+\cdots+v_n^2}$. |
| **Unit vector** | A vector of norm 1; obtain by **normalising**: $\mathbf u = \mathbf v/\|\mathbf v\|$. |
| **Distance** | $d(\mathbf u,\mathbf v) = \|\mathbf u-\mathbf v\|$ (Euclidean distance). |
| **Dot product $\mathbf u\cdot\mathbf v$** | $\|\mathbf u\|\,\|\mathbf v\|\cos\theta = u_1v_1+\cdots+u_nv_n$; also $\mathbf u^{\mathsf T}\mathbf v$. A **scalar**. |
| **Orthogonal vectors** | $\mathbf u\cdot\mathbf v = 0$; the zero vector is orthogonal to everything. |
| **Orthogonal set** | $\mathbf u_i\cdot\mathbf u_j = 0$ for every $i\ne j$. |
| **Orthonormal set** | An orthogonal set of **unit** vectors: $\mathbf u_i\cdot\mathbf u_j = \delta_{ij}$. |
| **Orthogonal basis / orthonormal basis** | A basis whose vectors are pairwise orthogonal / orthonormal. |
| **Normal vector** | Nonzero vector orthogonal to a line or plane: $\mathbf n = (a,b)$ (line), $\mathbf n = (a,b,c)$ (plane). |
| **Point–normal form** | $a(x-x_0)+b(y-y_0)+c(z-z_0) = 0$, i.e. $ax+by+cz = d$ (Thm 3.3.1). |
| **Orthogonal complement $W^{\perp}$** | All vectors orthogonal to **every** vector of the subspace $W$. |
| **Vector component of $\mathbf u$ along $\mathbf a$** | $\operatorname{proj}_{\mathbf a}\mathbf u = \dfrac{\mathbf u\cdot\mathbf a}{\|\mathbf a\|^2}\mathbf a$ (10). |
| **Orthogonal component** | $\mathbf u - \operatorname{proj}_{\mathbf a}\mathbf u$ (11). |
| **Orthogonal projection onto $W$** | $\operatorname{proj}_W\mathbf y = \hat{\mathbf y}$ — the closest point of $W$ to $\mathbf y$; $\mathbf y-\hat{\mathbf y}\in W^{\perp}$. |
| **Best approximation** | $\hat{\mathbf y}$ is the closest point in $W$ to $\mathbf y$ (Thm 9). |
| **Orthogonal matrix** | A **square** matrix with orthonormal columns: $U^{\mathsf T}U = UU^{\mathsf T} = I$, so $U^{-1} = U^{\mathsf T}$. |
| **Projection matrix** | $P = QQ^{\mathsf T}$ with $Q$ having orthonormal columns: symmetric and idempotent ($P^2 = P$). |
| **Gram–Schmidt process** | Turns a basis into an **orthogonal basis**: $\mathbf v_j = \mathbf x_j - \sum_{i<j}\frac{\mathbf x_j\cdot\mathbf v_i}{\mathbf v_i\cdot\mathbf v_i}\mathbf v_i$ (Thm 11). |
| **QR factorisation** | $A = QR$: $Q$ has orthonormal columns spanning $\operatorname{Col} A$, $R$ is upper triangular (unique with $r_{jj}>0$). |
| **Economy vs full QR** | Economy: $Q$ is $m\times n$, $R$ is $n\times n$; full: $Q$ is $m\times m$ and $R$ has $m-n$ zero rows at the bottom. |

## Least Squares (Chapter 7)

| Term | Definition |
|---|---|
| **Over-determined** | $A$ is $m\times n$ with $m>n$ (tall and thin); the system may be inconsistent. |
| **Under-determined** | $m<n$ (short and fat); infinitely many solutions. |
| **Consistency** | $\mathbf b\in\operatorname{Col} A$ $\iff$ $\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf b])$. |
| **Noise model** | $\mathbf b = A\mathbf x + \boldsymbol\epsilon$, with $\boldsymbol\epsilon$ modelling error/noise. |
| **Least-squares solution $\hat{\mathbf x}$** | The $\mathbf x$ minimising $\|\mathbf b-A\mathbf x\|$ (equivalently the sum of squares of the residual components). |
| **Residual / error** | $\mathbf b - A\hat{\mathbf x}$; orthogonal to $\operatorname{Col} A$. |
| **Normal equation** | $A^{\mathsf T}A\hat{\mathbf x} = A^{\mathsf T}\mathbf b$. |
| **Fitted values** | $\hat{\mathbf b} = A\hat{\mathbf x} = P\mathbf b$, the projection of $\mathbf b$ onto $\operatorname{Col} A$. |
| **Projection matrix** | $P = A(A^{\mathsf T}A)^{-1}A^{\mathsf T}$; square, symmetric ($P^{\mathsf T}=P$) and idempotent ($P^2=P$). |
| **Least-squares error** | $\|\mathbf b - A\hat{\mathbf x}\|$ — the smallest possible distance from $\mathbf b$ to $\operatorname{Col} A$. |
| **Pseudoinverse** | $(A^{\mathsf T}A)^{-1}A^{\mathsf T}$ (Moore–Penrose when $A^{\mathsf T}A$ is singular). |
| **Least-squares line** | $y=\beta_0+\beta_1x$ fitted to data; residuals $y_j-\hat y_j$. |
| **Linear-in-parameters model** | $y=\beta_0+\beta_1x+\beta_2x^2+\cdots$ — linear in the parameters $\beta_i$, so least squares applies. |

## Eigenvalues and Eigenvectors (Chapter 8)

| Term | Definition |
|---|---|
| **Eigenvalue / eigenvector** | $A\mathbf x=\lambda\mathbf x$ with $\mathbf x\ne\mathbf 0$. |
| **Eigenspace $E_\lambda$** | $N(A-\lambda I)$ — all eigenvectors for $\lambda$ plus the zero vector; a subspace. |
| **Characteristic equation** | $\det(A-\lambda I)=0$; the characteristic polynomial has degree $n$. |
| **Algebraic multiplicity** | Multiplicity of $\lambda$ as a root of the characteristic polynomial. |
| **Geometric multiplicity** | $\dim N(A-\lambda I)$ — the number of independent eigenvectors for $\lambda$. |
| **Similar matrices** | $A = PBP^{-1}$ for some invertible $P$; same eigenvalues, determinant, trace. |
| **Diagonalizable** | $A = PDP^{-1}$ with $D$ diagonal: $A$ has $n$ linearly independent eigenvectors. |
| **Defective matrix** | Not diagonalizable: some eigenvalue has geometric multiplicity < algebraic multiplicity. |
| **$\mathcal B$-coordinates** | $[\mathbf x]_{\mathcal B}$ — the weights of $\mathbf x$ in the basis $\mathcal B$. |
| **Change-of-basis matrix** | $[\mathbf x]_{\mathcal C} = \mathop{P}\limits_{\mathcal C\leftarrow\mathcal B}[\mathbf x]_{\mathcal B}$; diagonalisation is a change of basis to an eigenvector basis. |
| **$\mathcal B$-matrix of a transformation** | $[T]_{\mathcal B} = P_{\mathcal B}^{-1}AP_{\mathcal B}$ — similar to $A$. |
| **Complex eigenvalues** | Non-real eigenvalues of a real matrix occur in conjugate pairs $a\pm bj$ (a scaled rotation). |

## Complex Numbers and the DFT (Chapter 8A)

| Term | Definition |
|---|---|
| **Imaginary unit** | $j$ with $j^2=-1$; $z=a+bj$ is the **rectangular form**. |
| **Conjugate / modulus** | $\bar z = a-bj$; $\lvert z\rvert = \sqrt{a^2+b^2}$; $z\bar z = \lvert z\rvert^2$. |
| **Polar form** | $z = r(\cos\theta + j\sin\theta) = r\angle\theta$. |
| **Euler's formula** | $e^{j\theta} = \cos\theta+j\sin\theta$; $z = re^{j\theta}$ (exponential form). |
| **De Moivre's theorem** | $z^n = r^n(\cos n\theta + j\sin n\theta)$. |
| **Roots** | $z^{1/n} = \sqrt[n]{r}\,\angle\frac{\theta+2\pi k}{n}$, $k=0,\dots,n-1$: $n$ equally spaced roots. |
| **Complex vector** | $\mathbf z\in\mathbb{C}^N$; conjugate transpose $\mathbf z^{H}=\bar{\mathbf z}^{\mathsf T}$. |
| **Complex inner product** | $\langle\mathbf a,\mathbf b\rangle = \sum_n \overline{a_n}b_n = \mathbf a^{H}\mathbf b$; $\|\mathbf b\| = \sqrt{\mathbf b^{H}\mathbf b}\ge 0$. |
| **Fourier basis** | $\mathbf w_k$ with entries $e^{j(2\pi/N)kn}$ — orthogonal in the complex inner product. |
| **DFT / IDFT** | $X[k]=\sum_n x[n]e^{-j\frac{2\pi}{N}kn}$; $x[n]=\frac1N\sum_k X[k]e^{j\frac{2\pi}{N}kn}$. |
| **DFT as change of basis** | The DFT gives the coordinates of $\mathbf x$ in the Fourier (complex exponential) basis. |
| **Aliasing** | Frequencies $k$ and $k+N$ are indistinguishable from samples ($N$ = length). |

*End of glossary.*
