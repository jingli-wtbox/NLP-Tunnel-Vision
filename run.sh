#!/bin/bash
uvicorn serve:app --app-dir src --host 0.0.0.0 --port 8080