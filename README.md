# RUI Tracking SDK Python Wrapper

A Python wrapper for the RUI SDK that enables event tracking and campaign management using .NET interoperability.

## Overview

This package provides a Python interface to the RUI SDK (DotNet) allowing applications to:
- Track user events
- Manage tracking sessions
- Retrieve campaign information through ReachOut functionality

## Prerequisites

- Python 3.7+
- .NET 6 Runtime
- RUI SDK DLL files (version 5.6.0/5.6.1)

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Ensure the RUI SDK DLL files are in the correct location:
   - `lib/ruiSDKDotNet_5.6.1.dll`
   - `lib/ruiSDK_5.6.0.x64.dll`

## Configuration

The default configuration can be modified by updating the `DEFAULT_CONFIG` dictionary in `rui.py`:

```python
DEFAULT_CONFIG = {
    "rui_product_id": "2399118365",
    "rui_app_name": "RUI_Demo_App",
    "rui_url": "36368.tbnet1.com",
    "rui_key": "18864666411186DADA2DF73E91457D51"
}
```

This config information can be retrieved at: [Revenera: Usage Intelligence Getting Started Guide .NET](https://docs.revenera.com/ui561/netmultiplatform/Content/helplibrary/Basic_Integration_Steps.htm#quick-start-guide_1045877444_1078085)

Application information can also be customized via the `APP_INFO` dictionary:

```python
APP_INFO = {
    "product_edition": "Professional",
    "language": "English",
    "product_version": "5.0.0",
    "build_number": "17393"
}
```

## Usage

### Starting RUI Tracking

```python
from rui import start_rui_tracking, stop_rui_tracking, track_event

# Start tracking with default configuration
start_rui_tracking()

# Or start with session tracking
start_rui_tracking(use_session=True)

# Or use custom configuration
custom_config = {
    "rui_product_id": "YOUR_PRODUCT_ID",
    "rui_app_name": "YOUR_APP_NAME",
    "rui_url": "YOUR_URL",
    "rui_key": "YOUR_KEY"
}
start_rui_tracking(config=custom_config)
```

### Tracking Events

```python
# Track a simple event
track_event("Feature_Used", "calculator")

# Track an event with text
track_event("Feature_Request", "survey-feedback", "User feedback text")

# Track an event with numeric value
from rui import track_event_numeric
track_event_numeric("Performance", "Load_Time", 1.25)
```

### Retrieving ReachOut Campaigns

```python
from rui import manually_get_all_reachouts

# Get all available campaigns
campaigns = manually_get_all_reachouts()
for campaign in campaigns:
    if campaign["type"] == "text":
        print(f"Text message: {campaign['message']}")
    elif campaign["type"] == "url":
        print(f"URL to open: {campaign['message']}")
```

### Stopping RUI Tracking

```python
# Stop tracking and clean up resources
stop_rui_tracking()
```

## Session Management

Sessions allow for grouping related events. When using sessions:

```python
# Start with session tracking
start_rui_tracking(use_session=True)

# Events will be automatically associated with the current session
track_event("App_Flow", "main-screen")

# When finished, stop tracking to clean up
stop_rui_tracking()  # Also ends the current session
```

## Troubleshooting

- Ensure .NET 6 runtime is installed
- Check that DLL files are in the correct path
- Verify network connectivity to the RUI server
- Log files are stored in the `./logs` directory

## License

MIT License

Copyright (c) 2025 allblackpanda

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
