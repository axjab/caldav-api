# `caldav` reference

## get_calendars

```python
def get_calendars(
    client_class: type,
    calendar_url: Any | None = None,
    calendar_name: Any | None = None,
    check_config_file: bool = True,
    config_file: str | None = None,
    config_section: str | None = None,
    testconfig: bool = False,
    environment: bool = True,
    name: str | None = None,
    raise_errors: bool = False,
    **config_data,
) -> CalendarCollection:
    """
    Get calendars from one or more CalDAV servers.

    Configuration is read from multiple sources in priority order:

    1. Explicit keyword arguments (``url``, ``username``, ``password``, …)
    2. Test server (``testconfig=True`` or ``PYTHON_CALDAV_USE_TEST_SERVER``)
    3. Environment variables (``CALDAV_URL``, …)
    4. Config file — supports meta-sections so a single ``config_section``
       can expand to multiple servers (see below)

    **Multi-server / meta-sections**

    Sources 1–3 always produce a single connection.  When the config file is
    used (source 4) the ``config_section`` value is passed through
    ``expand_config_section``, which supports:

    * ``"*"`` – every non-disabled section in the file
    * ``"all"`` – a meta-section defined as ``{"contains": ["work", "personal"]}``
    * Glob patterns such as ``"work_*"``
    * A plain section name (normal single-server behaviour)

    Each expanded leaf section can carry its own ``calendar_name`` or
    ``calendar_url`` to filter which calendars are returned for that server.
    Function-level ``calendar_name`` / ``calendar_url`` arguments override
    per-section values when provided.

    The returned :class:`CalendarCollection` is a list that can be used as a
    context manager; on exit **all** underlying connections are closed.

    Args:
        client_class: The client class to use (``DAVClient`` or ``AsyncDAVClient``).
        calendar_url: URL(s) or ID(s) of specific calendars to fetch.
        calendar_name: Name(s) of specific calendars to fetch by display name.
        check_config_file: Whether to look for config files (default: True).
        config_file: Explicit path to config file.
        config_section: Section name in config file (default: ``"default"``).
            Supports ``*``, meta-sections, and glob patterns.
        testconfig: Whether to use test server configuration.
        environment: Whether to read from environment variables (default: True).
        name: Name of test server to use (for testconfig).
        raise_errors: If True, raise exceptions on errors; if False, log and skip.
        **config_data: Explicit connection parameters (url, username, password, …).

    Returns:
        :class:`CalendarCollection` of matching calendars (may be empty).

    Example — single server::

        from caldav import get_calendars

        with get_calendars(url="https://...", username="...", password="...") as cals:
            for cal in cals:
                print(cal.get_display_name())

    Example — all sections in config file::

        with get_calendars(config_section="*") as cals:
            for cal in cals:
                print(cal.get_display_name())
    """
```