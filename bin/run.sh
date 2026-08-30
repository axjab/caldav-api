#!/bin/bash
set -e
cd $HOME/src/caldav-api
uv run fastapi dev
