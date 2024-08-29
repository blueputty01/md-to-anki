
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