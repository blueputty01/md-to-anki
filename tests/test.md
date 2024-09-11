A **vector-valued** function consists of two parts: a **domain**, which is a collection of numbers, and a **2::rule**, which assigns to each number in the domain one and only one vector.
$\mathbf{F}(t)=f_{1}(t)\mathbf{i}+f_{2}(t)\mathbf{j}+f_{3}(t)\mathbf{k}$

Suppose we have two functions $f(x)$ and $g(x)$ such that $\lim_{x \rightarrow \infty}f(x)$ and $\lim_{x \rightarrow \infty}g(x)$  exist (may be $\infty$). Then:
$**\lim_{x \rightarrow \infty} \frac{f(x)}{g(x)} \neq \infty \implies f(x)** = O(g(x))$
$**\lim_{x \rightarrow \infty} \frac{f(x)}{g(x)} \neq 0 \implies f(x)** = \Omega(g(x))$
$**\lim_{x \rightarrow \infty} \frac{f(x)}{g(x)} \neq 0, \infty \implies f(x)** = \theta(g(x))$


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