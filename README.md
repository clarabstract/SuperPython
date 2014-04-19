SuperPython
===========

Adds tab-completion to Python's somewhat verbose `super()` construct. Just hit `tab` after a `super` keyword and a snippet will be inserted contained the likely current class and method name, with the existing arguments already filled.

Example:
```python
class AHappyClass(JustSwellBase):
	def __init__(self, required_arg, and_another, *anything_else, **enough_already):
		super#<tab>

# Becomes:

class AHappyClass(JustSwellBase):
	def __init__(self, required_arg, and_another, *anything_else, **enough_already):
		super(AHappyClass, self).__init__(required_arg, and_another, *anything_else, **enough_already)

```

SubleText's own parsing is used to guess the "current" class name, method name and arguments, which should be fine almost all the time, but may in rare cases pick up the wrong thing, say, if there's an innter class or method definition between the call to `super` and the real method signature. 

Installation
------------

You know the drill. To install this plugin, you have two options:

1. **Package Control** (recommended). If you have [Sublime Package
   Control](https://sublime.wbond.net/) installed, simply search for
   `SuperPython` to install.

2. **Manual**. Clone source code to Sublime Text `Packages` folder:
```bash
$ git clone https://github.com/rubyruy/SuperPython
```