# caldav-api
An HTTP API to your CalDAV server. In reality, a RESTful wrapper for Python's `caldav` library. Manage calendar events with standard GET, POST, PUT, and DELETE via JSON. No XML, no WebDAV verbs, no protocol complexity. Built for scripts and services that need simple calendar integration.

**Test**: `bin/test*` _NOT READY_

**Run**: `bin/run*`

**Build**: `bin/build*`

**Push**: `bin/push*`

## Issues

**OBJECTIVE**: Calculate and track the number of hours scheduled per activity, per week, per month, and per year.

- [ ] docker compose up fails, exits with 0
- [ ] ungraceful stop, exit 143
- [ ] Get calendars
- [ ] List all events
- [ ] Create event
- [ ] Update event
- [ ] Delete event
- [ ] docker push fails

Once the above issues are resolved, a CLI could query the API to perform analysis.

## Deploy

(see compose)
```
sudo docker compose up -d
```
