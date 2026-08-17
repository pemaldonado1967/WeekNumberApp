# Week Number App

A small Windows desktop application that displays the current ISO week number together with the current and next month calendars.

The application is built with Python and Tkinter. It can run directly from Python or be packaged as a Windows executable with PyInstaller. Classic Outlook can launch it from a custom ribbon button or automatically when Outlook starts.

## Features

- Displays the current ISO week number.
- Shows the current month and the next month.
- Highlights every day belonging to the current ISO week.
- Highlights today separately.
- Supports ISO weeks that cross a month boundary.
- Refreshes automatically at midnight.
- Provides a manual **Refresh now** button.
- Supports `Ctrl + R` for manual refresh.
- Uses a dark, card-based desktop interface.
- Can be launched from a desktop shortcut or Classic Outlook.

## Project structure

```text
WeekNumberApp/
├── week_number_app.py       # Main Tkinter application
├── README.md                # Project documentation
├── .gitignore               # Excludes local and build artifacts
├── docs/
│   └── OUTLOOK_INTEGRATION.md
└── week_number.ico          # Optional application icon
```

The `build/`, `dist/`, virtual environment, cache files, and PyInstaller specification file are intentionally excluded from source control.

## Requirements

- Windows
- Python 3.11 or later
- Tkinter, normally included with the standard Windows Python installation
- PyInstaller for creating the executable

The application itself uses only Python standard-library modules:

- `calendar`
- `datetime`
- `tkinter`
- `ttk`

## Run from source

Open PowerShell in the project folder and run:

```powershell
py week_number_app.py
```

## Build the Windows executable

Install PyInstaller if it is not already installed:

```powershell
py -m pip install pyinstaller
```

Build the fast-starting directory version:

```powershell
py -m PyInstaller --noconfirm --clean --windowed --onedir --name WeekNumber week_number_app.py
```

The executable is created here:

```text
dist\WeekNumber\WeekNumber.exe
```

### Build options

- `--windowed`: does not open a console window.
- `--onedir`: creates a folder containing the executable and its supporting files. This normally starts faster than a one-file executable.
- `--clean`: removes cached build information before building.
- `--noconfirm`: replaces existing build output without asking for confirmation.
- `--name WeekNumber`: sets the application name.

If an icon is available, include it with:

```powershell
py -m PyInstaller --noconfirm --clean --windowed --onedir --name WeekNumber --icon week_number.ico week_number_app.py
```

Do not copy only the executable from an `--onedir` build. Keep the complete `dist\WeekNumber` folder together.

## Desktop shortcut

A shortcut can be created by right-clicking `dist\WeekNumber\WeekNumber.exe` and choosing:

```text
Show more options > Send to > Desktop (create shortcut)
```

The shortcut can then be renamed to `Week #`, pinned to the taskbar, or moved to another approved location.

## Outlook integration

Classic Outlook supports adding a VBA macro to a custom ribbon group. The relevant VBA code is documented in:

```text
docs\OUTLOOK_INTEGRATION.md
```

The integration uses two procedures:

1. `OpenWeekNumber` in a standard VBA module. This launches the packaged executable.
2. `Application_Startup` in `ThisOutlookSession`. This launches the application automatically when Outlook starts.

The VBA code must contain the correct local path to `WeekNumber.exe`. Paths are computer-specific and should not be copied unchanged to another computer.

## Updating the application

1. Edit `week_number_app.py`.
2. Test the source version:

   ```powershell
   py week_number_app.py
   ```

3. Rebuild the executable with PyInstaller.
4. Close any running Week Number instance.
5. Replace or recreate the desktop shortcut if the output location changes.
6. Test the Outlook ribbon button and the automatic Outlook startup behavior.

## Public repository safety

Before publishing this repository:

- Do not commit the packaged executable unless there is a specific reason to distribute binaries through GitHub.
- Do not commit `.venv/`, `build/`, `dist/`, `__pycache__/`, or `*.spec` files.
- Do not publish personal Windows usernames or local company paths.
- Replace local paths in examples with a generic path such as:

  ```text
  C:\Path\To\WeekNumberApp\dist\WeekNumber\WeekNumber.exe
  ```

- Review all files before making the repository public.
- Do not include passwords, tokens, certificates, private keys, or internal company information.

## License

No license has been selected for this project yet. Without a license, other people can view the public repository but do not automatically receive permission to reuse, modify, or redistribute the code.
