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