# Battery Guardian

Battery Guardian is a Windows desktop application built with Python to monitor laptop battery status, charging state, estimated remaining time, and local battery history.

## Version

**Version 2.0**

Version 2 evolves the original battery-monitoring script into a modular application with:

* Battery status monitoring
* Charger connection and disconnection detection
* Low and critical battery notifications
* Full-charge notification
* Estimated remaining battery time
* SQLite-based battery logging
* CustomTkinter graphical dashboard
* Centralized monitoring configuration
* Graceful application shutdown
* Basic automated tests

## Features

### Battery Monitoring

The application reads battery information through `psutil`, including:

* Current battery percentage
* Charging state
* Estimated remaining time

Unavailable or invalid remaining-time values are handled safely and displayed as `Unknown`.

### Battery Notifications

Battery Guardian generates Windows notifications for important events:

| Event                | Default Threshold / Condition                         |
| -------------------- | ----------------------------------------------------- |
| Low battery          | 30% or below while not charging                       |
| Critical battery     | 15% or below while not charging                       |
| Full battery         | 100% while charging                                   |
| Charger connected    | Charging state changes from disconnected to connected |
| Charger disconnected | Charging state changes from connected to disconnected |

Critical battery notifications have priority over low-battery notifications, preventing both alerts from being sent for the same reading.

Thresholds are configurable through `config.py`.

### Local Battery History

Battery readings are stored in a local SQLite database.

Each record contains:

* Timestamp
* Battery percentage
* Charging state
* Estimated remaining time in seconds

The database directory is created automatically when the application starts if it does not already exist.

The database file is excluded from Git so local battery history is not uploaded to the repository.

### Graphical Dashboard

The application uses CustomTkinter to display:

* Current battery percentage
* Battery progress bar
* Charging or discharging status
* Estimated remaining battery time

The dashboard refresh interval is controlled centrally through `CHECK_INTERVAL` in `config.py`.

When the application closes, the scheduled dashboard callback is cancelled and the SQLite connection is closed cleanly.

## Project Structure

```text
Battery-Guardian/
|
|-- main.py
|-- config.py
|-- requirements.txt
|-- .gitignore
|
|-- core/
|   |-- __init__.py
|   |-- battery.py
|   |-- monitor.py
|   |-- notifier.py
|
|-- database/
|   |-- __init__.py
|   |-- db.py
|
|-- gui/
|   |-- __init__.py
|   |-- dashboard.py
|
|-- tests/
|   |-- test_battery.py
|
|-- data/
    |-- battery.db
```

The `data/battery.db` file is generated locally and ignored by Git.

## Architecture

The project separates responsibilities across several modules.

### `main.py`

Application entry point.

It initializes the database, creates the battery monitor, creates the dashboard, and starts the CustomTkinter event loop.

### `config.py`

Contains centralized application configuration:

```python
CHECK_INTERVAL = 60

LOW_BATTERY = 30
CRITICAL_BATTERY = 15
FULL_BATTERY = 100

APP_NAME = "Battery Guardian"
```

`CHECK_INTERVAL` is used by the dashboard to determine how often battery information is refreshed.

### `core/battery.py`

Provides an abstraction around `psutil.sensors_battery()`.

It returns:

* Battery percentage
* Charging state
* Estimated remaining time

The time formatter safely handles unavailable values such as `None` or non-positive values.

### `core/monitor.py`

Contains the main monitoring logic.

It:

1. Reads the current battery state.
2. Stores the reading in SQLite.
3. Detects charger state changes.
4. Checks battery thresholds.
5. Gives critical battery alerts priority over low-battery alerts.
6. Triggers notifications when required.
7. Prevents repeated notifications while the same condition remains active.

### `core/notifier.py`

Provides a small notification layer around Winotify for Windows desktop notifications.

### `database/db.py`

Manages the SQLite database and the `battery_logs` table.

It provides methods for:

* Creating the database table
* Adding battery readings
* Retrieving recent readings
* Closing the database connection

The required `data` directory is created automatically during initialization.

### `gui/dashboard.py`

Implements the desktop interface using CustomTkinter.

The dashboard refreshes according to `CHECK_INTERVAL` and updates:

* Battery percentage
* Progress bar
* Charging or discharging status
* Estimated remaining time

It also handles clean application shutdown.

### `tests/test_battery.py`

Contains basic automated tests using Python's built-in `unittest` framework.

The current tests cover:

* Battery remaining-time formatting
* Unavailable remaining-time values

## Technology Stack

* **Python 3.11+**
* **psutil** — battery and system information
* **CustomTkinter** — graphical user interface
* **Winotify** — Windows desktop notifications
* **SQLite** — local battery history storage
* **unittest** — automated testing

## Requirements

* Windows
* Python 3.11 or newer
* pip

## Installation

Clone the repository:

```bash
git clone https://github.com/mostafasoliman-cloud/Battery-Guardian.git
```

Enter the project directory:

```bash
cd Battery-Guardian
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Configuration

Battery thresholds and the monitoring interval can be configured in `config.py`.

For example:

```python
CHECK_INTERVAL = 60

LOW_BATTERY = 25
CRITICAL_BATTERY = 10
FULL_BATTERY = 100
```

Changing `CHECK_INTERVAL` changes how frequently the application checks the battery and refreshes the dashboard.

Changing the battery thresholds changes when notifications are triggered.

## Testing

The project includes basic automated tests using Python's built-in `unittest` framework.

Run the tests with:

```bash
python -m unittest discover -s tests
```

The current tests cover:

* Remaining-time formatting
* Unavailable remaining-time values

Additional tests can be added as the monitoring logic expands.

## Data Storage

The application uses SQLite for local persistence.

Database location:

```text
data/battery.db
```

The database stores:

* Timestamp
* Battery percentage
* Charging state
* Estimated remaining time

No external database server is required.

The database file is excluded from version control through `.gitignore`.

## Current Implementation

The current Version 2 implementation performs the monitoring cycle through the CustomTkinter GUI event loop.

Each monitoring cycle:

1. Reads the battery state.
2. Logs the reading to SQLite.
3. Checks charger-state changes.
4. Evaluates notification thresholds.
5. Updates the dashboard.
6. Schedules the next check using `CHECK_INTERVAL`.

The application also performs clean shutdown by:

1. Cancelling the scheduled dashboard callback.
2. Closing the SQLite connection.
3. Destroying the application window.

## Roadmap

### Version 3

* Battery usage charts
* Historical battery statistics
* Battery drain-rate calculation
* Daily and session-based usage summaries
* Improved dashboard
* Battery history visualization
* Expanded automated test coverage

### Version 4

* Machine Learning-based battery consumption prediction
* Estimated time-to-empty based on historical usage
* Abnormal consumption detection
* Usage pattern analysis

### Future Improvements

* Process-level resource monitoring
* Windows startup support
* User-configurable notification settings
* Exportable battery reports
* More comprehensive automated tests
* Packaging as a standalone Windows executable

## Contributing

Issues, suggestions, and pull requests are welcome.

Before submitting changes, please keep the modular project structure and avoid committing:

* Local database files
* Python cache files
* Virtual environments
* IDE-specific files
* Log files

## Author

**Mostafa Mousa**

GitHub: https://github.com/mostafasoliman-cloud

## License

No license has been specified for this repository yet.
