A **vector-valued** function consists of two parts: a **domain**, which is a collection of numbers, and a **2::rule**, which assigns to each number in the domain one and only one vector.
$\mathbf{F}(t)=f_{1}(t)\mathbf{i}+f_{2}(t)\mathbf{j}+f_{3}(t)\mathbf{k}$

Suppose we have two functions $f(x)$ and $g(x)$ such that $\lim_{x \rightarrow \infty}f(x)$ and $\lim_{x \rightarrow \infty}g(x)$  exist (may be $\infty$). Then:
$**\lim_{x \rightarrow \infty} \frac{f(x)}{g(x)} \neq \infty \implies f(x)** = O(g(x))$
$**\lim_{x \rightarrow \infty} \frac{f(x)}{g(x)} \neq 0 \implies f(x)** = \Omega(g(x))$
$**\lim_{x \rightarrow \infty} \frac{f(x)}{g(x)} \neq 0, \infty \implies f(x)** = \theta(g(x))$

$\operatorname*{lim}_{t\to t_{0}}(\mathbf{F}+\mathbf{G})(t)=**\operatorname*{lim}_{t\to t_{0}}\mathbf{F}(t)+\operatorname*{lim}_{t\to t_{0}}\mathbf{G}(t)**$
$\operatorname*{lim}_{t\rightarrow t_{0}}f F(t)=**\operatorname*{lim}_{t\rightarrow t_{0}}f(t)\operatorname*{lim}_{t\rightarrow t_{0}}\operatorname{F}(t)**$
$\operatorname*{lim}_{t\rightarrow t_{0}}\left(\mathbf{F}\cdot\mathbf{G}\right)(t)=**\operatorname*{lim}_{t\rightarrow t_{0}}\mathbf{F}(t)\cdot\operatorname*{lim}_{t\rightarrow t_{0}}\mathbf{G}(t)**$
$\operatorname*{lim}_{t\rightarrow t_{0}}\left({\bf F}\times{\bf G}\right)(t)=**\operatorname*{lim}_{t\rightarrow t_{0}}{\bf F}(t)\times\operatorname*{lim}_{t\rightarrow t_{\alpha}}{\bf G}(t)**$
$\operatorname*{lim}_{s\to s_{0}}(\mathbf{F}\circ g)(s)=**\operatorname*{lim}_{t\to t_{0}}\mathbf{F}(t)**$ if $g(s) \neq t_0$ for all $s$ in an open interval about $s_0$

Depth first tree traversal implementation (general tree):
{{c1::
```python
def fooHelper(localRoot): 
	visit localRoot.data
	for child in localRoot.children:
		fooHelper(child)
```
}}

Post-order traversal:
**4 5 2 6 7 3 1**

---

```python
visit node.data
recurse(left)
recurse(right)
```

---