# caldav-api
An HTTP API to your CalDAV server. In reality, a RESTful wrapper for Python's `caldav` library. Manage calendar events with standard GET, POST, PUT, and DELETE via JSON. No XML, no WebDAV verbs, no protocol complexity. Built for scripts and services that need simple calendar integration.

## Run Instructions

```bash
cd caldav-api/app
uv init
uv add caldav "fastapi[standard]"
```
