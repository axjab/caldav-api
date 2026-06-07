# app/core/logger.py
import logging


class _Logger:
    _COLORS = {
        "magenta": "\033[35m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "cyan": "\033[36m",
        "red": "\033[31m",
    }
    _RESET = "\033[0m"

    def __init__(self):
        """
        A lightweight singleton logger wrapping Python's stdlib `logging.Logger`.

        Instantiated once at module level as `Logger`. Import and call it directly:

            from app.core.logger import Logger

            Logger("app started")                       # default level
            Logger("something broke", level="error")    # one-off override

        All imports share the same instance -- settings configured on first use
        (name, color, level) persist across the entire application.

        Args:
            name  (str): Logger channel name. Defaults to "caldav-gateway".
            color (str): ANSI output color. One of: magenta, green, yellow, cyan, red.
            level (str): Default log level. Defaults to "info".
        """
        self._name = "uvicorn"
        self._level = logging.INFO
        self._color = ""
        self._logger = logging.getLogger(self._name)
        self._logger.propagate = False

    # COMPATIBLE WITH logging's loggers
    def __call__(self, msg: str = None, name=None, level=None, color=None):
        if name:  self._name = name
        if level: self._level = getattr(logging, level.upper())
        if color: self._color = self._COLORS.get(color, "")
        if msg:
            out = f"{self._color}{msg}{self._RESET}" if self._color else msg
            self._logger.log(self._level, out)
        return self


# MODULE-LEVEL SINGLETON *********************
Logger = _Logger()
log = Logger # alias, makes log() usable at import
