# Battery Guardian

Battery Guardian is a Windows desktop application built with Python for monitoring laptop battery status, tracking charging state, storing battery readings locally, and displaying battery information through a graphical dashboard.

## Version

**Version 2.0**

Version 2 evolves the original battery-monitoring script into a modular application with:

- Battery status monitoring
- Charger connection and disconnection detection
- Low and critical battery notifications
- Full-charge notification
- Estimated remaining battery time
- SQLite-based battery logging
- CustomTkinter graphical dashboard
- Configurable monitoring thresholds

## Features

### Battery Monitoring

The application reads battery information through `psutil`, including:

- Current battery percentage
- Charging state
- Estimated remaining time

### Battery Notifications

Battery Guardian generates Windows notifications for important events:

| Event | Default Threshold / Condition |
|---|---|
| Low battery | 30% or below while not charging |
| Critical battery | 15% or below while not charging |
| Full battery | 100% while charging |
| Charger connected | Charging state changes from disconnected to connected |
| Charger disconnected | Charging state changes from connected to disconnected |

Thresholds are configurable through `config.py`.

### Local Battery History

Battery readings are stored in a local SQLite database.

Each record contains:

- Timestamp
- Battery percentage
- Charging state
- Estimated remaining time in seconds

The database is intentionally excluded from Git so local battery history is not uploaded to the repository.

### Graphical Dashboard

The application uses CustomTkinter to display:

- Current battery percentage
- Battery progress bar
- Charging or discharging status
- Estimated remaining battery time

## Project Structure

```
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
|-- data/
    |-- battery.db
```

The `data/battery.db` file is generated locally when the application runs and is ignored by Git.

## Architecture

The project separates responsibilities across several modules.

### `main.py`

Application entry point.

It initializes the database, creates the battery monitor, creates the dashboard, and starts the CustomTkinter event loop.

### `config.py`

Contains application configuration:

```python
CHECK_INTERVAL = 60

LOW_BATTERY = 30
CRITICAL_BATTERY = 15
FULL_BATTERY = 100

APP_NAME = "Battery Guardian"
```

### `core/battery.py`

Provides an abstraction around `psutil.sensors_battery()`.

It returns battery percentage, charging state, and estimated remaining time and also formats the remaining time for the dashboard.

### `core/monitor.py`

Contains the main monitoring logic.

It:

1. Reads the current battery state.
2. Stores the reading in SQLite.
3. Detects charger state changes.
4. Checks battery thresholds.
5. Triggers notifications when required.
6. Prevents repeated notifications for the same active condition.

### `core/notifier.py`

Provides a small notification layer around Winotify.

### `database/db.py`

Manages the SQLite database and the `battery_logs` table.

It currently provides methods for:

- Creating the database table
- Adding battery readings
- Retrieving recent readings

### `gui/dashboard.py`

Implements the desktop interface using CustomTkinter.

The dashboard refreshes the battery state periodically and updates the displayed percentage, progress bar, charging state, and remaining time.

## Technology Stack

- **Python 3.11+**
- **psutil** — battery and system information
- **CustomTkinter** — graphical user interface
- **Winotify** — Windows desktop notifications
- **SQLite** — local battery history storage

## Requirements

- Windows
- Python 3.11 or newer
- pip

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

Battery thresholds and the intended monitoring interval can be configured in `config.py`.

For example:

```python
LOW_BATTERY = 25
CRITICAL_BATTERY = 10
```

This changes the low and critical battery notification thresholds.

## Data Storage

The application uses SQLite for local persistence.

Database location:

```
data/battery.db
```

The database is excluded from version control through `.gitignore`.

No external database server is required.

## Current Implementation Notes

The current Version 2 implementation performs the monitoring cycle through the GUI event loop. Battery data is checked when the dashboard refreshes.

The project is intentionally kept modular so that additional analytics and prediction functionality can be added without replacing the existing battery, notification, database, and GUI layers.

## Roadmap

### Version 3

- Battery usage charts
- Historical battery statistics
- Battery drain-rate calculation
- Daily and session-based usage summaries
- Improved dashboard
- Battery history visualization

### Version 4

- Machine Learning-based battery consumption prediction
- Estimated time-to-empty based on historical usage
- Abnormal consumption detection
- Usage pattern analysis

### Future Improvements

- Process-level resource monitoring
- Windows startup support
- User-configurable notification settings
- Exportable battery reports
- Improved error handling
- Automated tests
- Packaging as a standalone Windows executable

## Known Improvement Areas

The current Version 2 codebase is functional, but there are a few areas planned for refinement:

- The configured `CHECK_INTERVAL` value should be used directly by the dashboard instead of duplicating the interval value.
- The unused `time` import in `core/monitor.py` can be removed.
- Database initialization can be improved to create the `data` directory automatically on a fresh installation.
- Automated tests can be added for battery-state and notification logic.
- Database connection lifecycle management can be improved for cleaner application shutdown.

These are implementation improvements for future iterations and do not change the core purpose of Version 2.

## Contributing

Issues, suggestions, and pull requests are welcome.

Before submitting changes, please keep the modular project structure and avoid committing local database files or environment-specific files.

## Author

**Mostafa Mousa**

GitHub: https://github.com/mostafasoliman-cloud

## License

No license has been specified for this repository yet.
