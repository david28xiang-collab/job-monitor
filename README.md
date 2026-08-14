# Job Monitor

Monitor company career pages and send a Discord notification when new jobs are
listed in the configured target locations.

## Project layout

```text
config/                 Company configuration
data/current/           Most recently fetched job listings
data/baseline/          Listings used to detect new jobs
scripts/                Local command wrappers
src/job_monitor/        Application code
src/job_monitor/scrapers/  ATS and company-specific scrapers
tests/                  Automated tests
```

## Setup

Python 3.8 or newer is required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## Run

Run the complete fetch, comparison, notification, and baseline update:

```bash
job-monitor
```

The original command continues to work from the repository root:

```bash
python daily_run.py
```

The repository-local shell wrapper is also available:

```bash
./scripts/run_daily.sh
```

Run tests with:

```bash
pytest
```
