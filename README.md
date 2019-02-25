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

SublimeText's own parsing is used to guess the "current" class name, method name and arguments. Also snippet checks indent of current line to find appropriate class and method more accurately in cases if there's an inner class or method definition between the call to `super` and the real method signature. 

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

## Config

You can add some settings in your Sublime's project file:

* `superpython.prefix` - any string which will be trigger for completion. Default is `super`
* `superpython.style` - support only two values: `full` and `short`. Default is `short`. "Short"-style is Python 3's style: `super().func(*args, **kwargs)`

Example:
```json
{
    "settings":
    {
        "superpython.prefix": "foo",
        "superpython.style": "full",
    }
}
```
