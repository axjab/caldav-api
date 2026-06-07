# Utils

## Logger

**Question**:
> I know, what if I pass a flag in Logger() to tell the constructor wether I want the GLOBAL logger used in 90% of the app, or a new LOCAL logger. What do yuo think of this pattern?
>
> Is the following achievable?
> 
> main.py:
> log = Logger(name="uvicorn", color="green")   # GLOBAL SETTINGS
> log("message")  ---> green

> component_a.py:
> log = Logger()
> log("message") ---> green, thanks to main.py

> component_b.py:
> log = Logger("new")
> OR
> log = Logger(local:True)
> OR else
> log("message") --> white, main and component a remains UNCHANGED

---

The pattern is solid and totally achievable. My only design note: a `local=True` flag is the cleanest of your three options -- it's explicit and doesn't repurpose the positional arg in an ambiguous way.

Here's how I'd implement it:

```python
# logger.py

class _LoggerMeta(type):
    _instance = None

    def __call__(cls, name=None, color=None, local=False):
        # LOCAL: always return a fresh, independent instance
        if local:
            return _LoggerInstance(
                name=name or "app",
                color=color or "white"
            )

        # GLOBAL: create singleton on first call, configure if args passed
        if cls._instance is None:
            cls._instance = _LoggerInstance(
                name=name or "app",
                color=color or "white"
            )
        else:
            if name is not None:
                cls._instance.name = name
            if color is not None:
                cls._instance.color = color

        return cls._instance


class Logger(metaclass=_LoggerMeta):
    pass


class _LoggerInstance:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __call__(self, message):
        print(f"[{self.color}][{self.name}] {message}")
```

```python
# main.py
from logger import Logger

log = Logger(name="uvicorn", color="green")
log("started")                    # [green][uvicorn]
```

```python
# component_a.py
from logger import Logger

log = Logger()
log("hello from A")               # [green][uvicorn]  -- inherits global
```

```python
# component_b.py
from logger import Logger

log = Logger(local=True)          # fresh, no side effects
log("hello from B")               # [white][app]

log2 = Logger(local=True, name="worker", color="cyan")
log2("spawned worker")            # [cyan][worker]

# Global is untouched:
Logger()("still green?")          # [green][uvicorn]  -- yes
```

---

The flow in plain terms:

- `Logger()` -- returns the global, no changes
- `Logger(name=..., color=...)` -- returns the global, updates it
- `Logger(local=True)` -- returns a brand new `_LoggerInstance`, global never touched
- `Logger(local=True, name=..., color=...)` -- same, but with custom settings

The metaclass handles all of this in one `__call__`, keeping `Logger` itself clean with no visible `__init__` or `__new__` clutter.
