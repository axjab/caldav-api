#!/bin/bash
set -e
cd $HOME/src/caldav-api/app
uv run fastapi dev
