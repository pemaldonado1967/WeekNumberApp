\# Classic Outlook Integration



This document explains how to connect the Week Number application to Classic Outlook using VBA.



\## What the integration does



The integration provides two ways to open the application:



1\. A custom Outlook ribbon button named `Week #`.

2\. Automatic launch when Classic Outlook starts.



\## Prerequisites



\- Classic Outlook for Windows.

\- The Week Number executable built with PyInstaller.

\- Outlook VBA macros enabled.

\- The correct local path to `WeekNumber.exe`.



Example executable path:

```text

C:\\Path\\To\\WeekNumberApp\\dist\\WeekNumber\\WeekNumber.exe

```

## VBA launcher macro

The following macro belongs in a standard VBA module, such as `Module1`:
```vb
Public Sub OpenWeekNumber()
    Dim appPath As String

    appPath = "C:\Path\To\WeekNumberApp\dist\WeekNumber\WeekNumber.exe"

    Shell """" & appPath & """", vbNormalFocus
End Sub
```

## Add the launcher macro

1. Open Classic Outlook.
2. Press `Alt + F11`.
3. Select the Outlook VBA project.
4. Open a standard module, such as `Module1`.
5. Paste the `OpenWeekNumber` macro.
6. Replace the example path with the actual path to `WeekNumber.exe`.
7. Select **Debug > Compile Project**.
8. Save the VBA project with `Ctrl + S`.


## Add the macro to the Outlook ribbon

1. Close the VBA editor.
2. Right-click the Outlook ribbon.
3. Select **Customize the Ribbon**.
4. Select **Home (Mail)**.
5. Select the custom group where the button should appear.
6. Under **Choose commands from**, select **Macros**.
7. Add `Project1.Module1.OpenWeekNumber`.
8. Rename the button to `Week #`.
9. Choose a calendar or date icon.
10. Click **OK**.

## Automatic startup

In `ThisOutlookSession`, add:
```vb
Private Sub Application_Startup()
    OpenWeekNumber
End Sub
```

## Test automatic startup

1. Save the Outlook VBA project with `Ctrl + S`.
2. Close the VBA editor.
3. Close Outlook completely.
4. Reopen Classic Outlook.
5. Confirm that Week Number starts automatically.

## Troubleshooting

### The ribbon button does nothing

Check that:

- The path to `WeekNumber.exe` is correct.
- `WeekNumber.exe` opens by double-clicking it.
- The complete `dist\WeekNumber` folder still exists.
- Outlook macros are enabled.
- The VBA project compiles without errors.

### Automatic startup does not work

Check that:

- `Application_Startup` is in `ThisOutlookSession`.
- The VBA project was saved.
- Outlook was fully closed and restarted.
- Macros are enabled.
