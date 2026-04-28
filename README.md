# ISports API Python SDK

A comprehensive Python SDK for the [iSports API](https://www.isportsapi.com), providing easy access to football and basketball data.

## Features

- **Football API**: Organized into 5 categories
  - `live_data` — Live scores, schedules, events, lineups, live text
  - `profile` — League, team, player, referee, transfer info
  - `stats` — Standings, top scorers, match analysis, player stats
  - `odds` — Pre-match, in-play, historical odds (Asian, 1x2, OU, European, corners, etc.)
  - `common` — Utility endpoints (country, bookmaker, ID modifications, FIFA ranking)
- **Basketball API**: Organized into 5 categories
  - `live_data` — Live scores, schedules, lineups, live text
  - `profile` — League, team, player, transfer info
  - `stats` — Standings, match stats, quarter stats, analysis
  - `odds` — Full-time, half-time, quarter, in-play, European odds
  - `common` — Utility endpoints (country, bookmaker, schedule modifications)
- **Type Hints**: Full type annotation support
- **Async Support**: Both synchronous (`ISportsClient`) and asynchronous (`ISportsAsyncClient`) interfaces
- **Error Handling**: Comprehensive exception hierarchy (`ISportsError`, `AuthenticationError`, `RateLimitError`, `NotFoundError`, `ValidationError`, `ServerError`, `NetworkError`)
- **Rate Limit Error Handling**: Detects and raises `RateLimitError` when API quota is exceeded

## Requirements

- Python >= 3.8
- Optional: `aiohttp>=3.8.0` (for async client)

## Installation

### From PyPI (when published)

```bash
pip install isports-sdk
```

For async support, install with the `async` extra:

```bash
pip install isports-sdk[async]
```

### From Source

```bash
git clone https://github.com/isportsapiofficial/isports-sdk.git
cd isports-sdk-python
pip install -e .
```

## Quick Start

### Synchronous Client

```python
from isports import ISportsClient

# Initialize client
client = ISportsClient(api_key="your_api_key")

# Get today's football livescores
livescores = client.football.live_data.livescores()

# Get basketball schedule
schedule = client.basketball.live_data.schedule(date="2026-04-25")
```

### Asynchronous Client

```python
import asyncio
from isports import ISportsAsyncClient

async def main():
    async with ISportsAsyncClient(api_key="your_api_key") as client:
        # Get today's football livescores
        scores = await client.football.live_data.livescores()
        
        # Get basketball schedule
        schedule = await client.basketball.live_data.schedule(date="2024-01-15")
        
        print(scores)

asyncio.run(main())
```
## API Coverage

### Football

| Category | Methods |
|----------|---------|
| `live_data` | 10 |
| `profile` | 10 |
| `stats` | 9 |
| `odds` | 39 |
| `common` | 8 |

### Basketball

| Category | Methods |
|----------|---------|
| `live_data` | 8 |
| `profile` | 9 |
| `stats` | 5 |
| `odds` | 7 |
| `common` | 3 |

Use Python's built-in introspection to discover all available methods:

```python
from isports import ISportsClient
client = ISportsClient(api_key="your_api_key")

# List all football live_data methods
print(dir(client.football.live_data))
# List all basketball odds methods
print(dir(client.basketball.odds))
```

## Exception Handling

```python
from isports import (
    ISportsClient,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    ServerError,
    NetworkError
)

try:
    response = client.football.live_data.livescores()
except AuthenticationError as e:
    # Invalid API key (code=2 in response body)
    print(f"Auth failed: {e.message}")
except RateLimitError as e:
    # Too many requests
    print(f"Rate limited: {e.message}")
except ValidationError as e:
    # Missing or invalid parameters
    print(f"Bad request: {e.message}")
except NotFoundError as e:
    # Resource not found
    print(f"Not found: {e.message}")
except ServerError as e:
    # API server error (5xx)
    print(f"Server error: {e.message}")
except NetworkError as e:
    # Timeout, DNS, connection issues
    print(f"Network error: {e.message}")
```

## Parameter Filtering

Optional parameters with `None` values are automatically excluded from API requests:

```python
# Only 'date' is sent; league_id and match_id are filtered out
schedule = client.football.live_data.schedule_basic(
    date="2024-01-15",
    league_id=None,   # excluded
    match_id=None     # excluded
)
```

## Building from Source

```bash
git clone https://github.com/isportsapiofficial/isports-sdk.git
cd isports-sdk
pip install -e ".[dev]"
```

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_client.py -v
pytest tests/test_football.py -v
pytest tests/test_basketball.py -v
```

## Project Structure

```
isports-sdk/
├── src/isports/
│   ├── __init__.py          # Package entry (clients + exceptions)
│   ├── client.py            # ISportsClient / ISportsAsyncClient
│   ├── http.py              # HTTP layer (urllib / aiohttp)
│   ├── exceptions.py        # Exception hierarchy
│   ├── football/
│   │   └── __init__.py      # Football API (~76 endpoints)
│   └── basketball/
│       └── __init__.py      # Basketball API (~32 endpoints)
├── tests/
│   ├── test_client.py       # Client initialization + endpoint coverage
│   ├── test_http.py         # HTTP error handling + request methods
│   ├── test_football.py     # Football endpoint verification
│   └── test_basketball.py   # Basketball endpoint verification
├── pyproject.toml
├── setup.py
└── README.md
```

## Documentation

See the [API Documentation](https://www.isportsapi.com/en/docs.html) for detailed endpoint information.

## Links

- Homepage: https://github.com/isportsapiofficial/isports-sdk
- Repository: https://github.com/isportsapiofficial/isports-sdk
- Issues: https://github.com/isportsapiofficial/isports-sdk/issues

## License

MIT License
