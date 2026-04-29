# SpaceOps ISS Query Script

## Setup

Set the following environment variables in your terminal before running:

```bash
export DBHOST='ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com'
export DBUSER='your_computing_id'
export DBPASS='your_computing_id'
export REPORTER_ID='your_reporter_id'
```

## Running the Script

Run the script in interactive mode to call any function directly:

```bash
python3 -i spaceops_query.py
```

## Available Functions

**`get_latest_location()`** — returns the most recent ISS position recorded by SpaceOps.

**`get_last_n_locations(n)`** — returns the last N recorded positions. Defaults to 10 if no argument is passed.

**`get_location_at_time(target_timestamp)`** — returns the stored position closest to a given timestamp. Pass the timestamp as a string in `YYYY-MM-DD HH:MM:SS` format.

**`get_location_near(target_lat, target_lon, n)`** — returns the N closest recorded positions to a given latitude and longitude. Defaults to 5 results.

## Example Usage

```python
>>> get_latest_location()
>>> get_last_n_locations(20)
>>> get_location_at_time("2026-04-15 10:00:00")
>>> get_location_near(32.99, 170.03, 3)
```