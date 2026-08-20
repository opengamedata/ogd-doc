# Python Tips & Tricks

A list of various little niceties in Python that you can use when writing your Python code:

* Index dictionaries with `d.get('key', default_val)` instead of `d['key']`
* Loop lists of objects with `enumerate(container_ob)` to get an index with each object
* Convert `for` loops with list appends into list comprehensions
* Use `match-case` blocks instead of large `if-elif-else` blocks.
  * The type of a variable can be checked with the faux-constructor syntax in cases:

    ```python
    match var:
      case int():
        print("I'm an int!")
      case str():
        print("I'm a str!")
      case bool():
        print("I'm a bool!")
    ```
