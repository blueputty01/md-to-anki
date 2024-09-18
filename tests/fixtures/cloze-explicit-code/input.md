Depth first tree traversal implementation (general tree):
{{c1::
```python
def fooHelper(localRoot): 
	visit localRoot.data
	for child in localRoot.children:
		fooHelper(child)
```
}}