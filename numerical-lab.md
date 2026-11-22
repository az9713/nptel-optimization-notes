# Interactive laboratory

## A resource limit changes the optimum and its marginal value

Choose nonnegative production amounts $x,y$. Maximize profit $3x+2y$ subject to $x+y\le b$, $x\le2$ and $y\le3$, where $b\ge0$ is total resource availability. All values are dimensionless teaching units. The objective values one unit of $x$ more highly, so an optimal policy fills $x$ before $y$.

For $0\le b\le2$, the solution is $(x,y)=(b,0)$ with value $3b$. For $2\le b\le5$, it is $(2,b-2)$ with value $2b+2$. For $b\ge5$, it is $(2,3)$ with value 12. This follows by shifting any available resource from $y$ to an unfilled $x$: profit increases by one until $x=2$. Once both bounds are full, further resource has no value.

The marginal value of resource is therefore 3, then 2, then 0. At $b=2$ and $b=5$ the value function has a corner and there is no unique derivative. Optimal dual multipliers span the adjacent slopes at those breakpoints. A shadow price belongs to a region of validity; extending it beyond a basis change gives an incorrect prediction. Chapter 3 derives that statement from LP duality.

<div class="lab-controls"><label for="capacity">Resource b: <output id="capacity-value">4</output><input id="capacity" type="range" min="0" max="7" step="0.05" value="4"></label><div><p id="lp-result" aria-live="polite"></p><p id="lp-price"></p></div></div>
<canvas id="lp-plot" width="900" height="480" role="img" aria-label="Production feasible region and optimal point"></canvas>
<p class="meta">The shaded polygon is the feasible region. The gold point is the optimum. Dashed lines show the variable limits; the sloping line is the resource constraint.</p>

## Conditioning changes the pace of gradient descent

For a vector $z=(z_1,z_2)$, minimize $f(z)=\tfrac12(z_1^2+\kappa z_2^2)$, where the condition parameter $\kappa\ge1$ is the ratio of the two Hessian eigenvalues. The unique minimizer is the origin. With a constant step $\alpha$, gradient descent satisfies $z_{1,k+1}=(1-\alpha)z_{1,k}$ and $z_{2,k+1}=(1-\alpha\kappa)z_{2,k}$.

The display uses $\alpha=1/\kappa$ and initial point $(1,1)$. It zeros the second coordinate in one step, but the first coordinate contracts by $1-1/\kappa$. Its remaining objective after $k\ge1$ iterations is $\tfrac12(1-1/\kappa)^{2k}$. Large condition numbers therefore slow this safe step even on a convex quadratic. Newton’s exact quadratic step reaches the optimum in one iteration, at the cost of solving a linear system; that statement does not transfer unchanged to a general nonlinear objective.

<div class="lab-controls"><label for="conditioning">Condition parameter κ: <output id="conditioning-value">10</output><input id="conditioning" type="range" min="1" max="100" step="1" value="10"></label><label for="iterations">Iterations: <output id="iterations-value">20</output><input id="iterations" type="range" min="1" max="80" step="1" value="20"></label></div>
<p id="gradient-result" aria-live="polite"></p>
<canvas id="gradient-plot" width="900" height="420" role="img" aria-label="Logarithm of relative quadratic objective over gradient iterations"></canvas>

Both experiments run locally in your browser and have no network or storage effects. They illustrate exact small models, not solver benchmarks. The laboratory checks behind the chapters use Python and independent reference calculations.
