#!/usr/bin/env bash

# this file gets a brand-new clone of this application running with a single command.
# it creates the backend .venv if it doesn't already exist, it installs python dependencies.
# It also creates the backend/.env from the template if it doesn't already exist, then it installs
# our frontend dependencies.

# must be run from a Git Bash terminal
# command to run this file:
# cd into cash-cow
# bash bin/setup.sh

set -e

echo "== Cash Cow Setup =="

cd backend

# create our .venv if it doesn't already exist
if [! -d ".venv"]; then
    echo "Creating Virtual Environment..."
    python -m venv .venv
fi

source .venv/Scripts/activate
pip install -r requirements.txt

# create .env file if it doesn't exist already
if [! -f ".env"]; then 
    echo "No .env found - copying from .env.example."
    echo "Fill in real values in backend/.env before running the app."
    cp .env.example .env
fi

# Frontend setup
cd ../frontend
npm install

echo "Setup complete"