import calendar
import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import ttk


class WeekNumberApp:
    COLORS = {
        "background": "#0B1120",
        "surface": "#111827",
        "surface_alt": "#172033",
        "surface_muted": "#0F172A",
        "border": "#263449",
        "text": "#F8FAFC",
        "text_muted": "#94A3B8",
        "text_faint": "#64748B",
        "accent": "#38BDF8",
        "accent_dark": "#0C4A6E",
        "accent_soft": "#164E63",
        "today": "#F59E0B",
        "today_text": "#1C1917",
        "button": "#0284C7",
        "button_active": "#0369A1",
    }

    def __init__(self):
        self.root = tk.Tk()

        self.refresh_job = None
        self.countdown_job = None
        self.next_refresh_time = None
        self.today = date.today()
        self.view_offset = 0

        self.setup_window()
        self.setup_styles()
        self.build_ui()

        self.refresh_display()
        self.update_countdown()

    def setup_window(self):
        iso_week = self.today.isocalendar().week

        self.root.title(f"W{iso_week:02d}")
        self.root.geometry("1120x560")
        self.root.minsize(940, 500)
        self.root.configure(bg=self.COLORS["background"])

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind("<Control-r>", lambda event: self.manual_refresh())

    def setup_styles(self):
        style = ttk.Style(self.root)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "App.TFrame",
            background=self.COLORS["background"]
        )

        style.configure(
            "Sidebar.TFrame",
            background=self.COLORS["surface"],
            relief="flat"
        )

        style.configure(
            "Card.TFrame",
            background=self.COLORS["surface"],
            relief="flat"
        )

        style.configure(
            "Eyebrow.TLabel",
            background=self.COLORS["surface"],
            foreground=self.COLORS["accent"],
            font=("Inter", 10, "bold")
        )

        style.configure(
            "Week.TLabel",
            background=self.COLORS["surface"],
            foreground=self.COLORS["text"],
            font=("Inter", 62, "bold")
        )

        style.configure(
            "Date.TLabel",
            background=self.COLORS["surface"],
            foreground=self.COLORS["text"],
            font=("Inter", 13)
        )

        style.configure(
            "Muted.TLabel",
            background=self.COLORS["surface"],
            foreground=self.COLORS["text_muted"],
            font=("Inter", 10)
        )

        style.configure(
            "SmallMuted.TLabel",
            background=self.COLORS["surface"],
            foreground=self.COLORS["text_faint"],
            font=("Inter", 9)
        )

        style.configure(
            "CalendarTitle.TLabel",
            background=self.COLORS["surface"],
            foreground=self.COLORS["text"],
            font=("Inter", 17, "bold")
        )

        style.configure(
            "CalendarSubtitle.TLabel",
            background=self.COLORS["surface"],
            foreground=self.COLORS["text_muted"],
            font=("Inter", 9)
        )

        style.configure(
            "Countdown.TLabel",
            background=self.COLORS["surface_alt"],
            foreground=self.COLORS["text"],
            font=("Inter", 11, "bold"),
            justify="center"
        )

        style.configure(
            "Modern.TButton",
            background=self.COLORS["button"],
            foreground="white",
            borderwidth=0,
            focusthickness=0,
            padding=(16, 9),
            font=("Inter", 10, "bold")
        )

        style.map(
            "Modern.TButton",
            background=[
                ("active", self.COLORS["button_active"]),
                ("pressed", self.COLORS["button_active"])
            ],
            foreground=[
                ("disabled", self.COLORS["text_faint"])
            ]
        )

    def build_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        main_frame = ttk.Frame(
            self.root,
            style="App.TFrame",
            padding=24
        )

        main_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        self.build_sidebar(main_frame)
        self.build_calendar_area(main_frame)

    def build_sidebar(self, parent):
        sidebar = ttk.Frame(
            parent,
            style="Sidebar.TFrame",
            padding=26,
            width=275
        )

        sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 20)
        )

        sidebar.grid_propagate(False)

        ttk.Label(
            sidebar,
            text="ISO CALENDAR",
            style="Eyebrow.TLabel"
        ).pack(
            anchor="w",
            pady=(4, 20)
        )

        ttk.Label(
            sidebar,
            text="Current week",
            style="Muted.TLabel"
        ).pack(
            anchor="w"
        )

        self.week_label = ttk.Label(
            sidebar,
            text="",
            style="Week.TLabel"
        )

        self.week_label.pack(
            anchor="w",
            pady=(0, 8)
        )

        self.today_label = ttk.Label(
            sidebar,
            text="",
            style="Date.TLabel"
        )

        self.today_label.pack(
            anchor="w",
            pady=(0, 5)
        )

        ttk.Label(
            sidebar,
            text="Monday to Sunday",
            style="SmallMuted.TLabel"
        ).pack(
            anchor="w"
        )

        separator = ttk.Separator(sidebar)

        separator.pack(
            fill="x",
            pady=24
        )

        countdown_card = ttk.Frame(
            sidebar,
            style="Card.TFrame",
            padding=14
        )

        countdown_card.pack(
            fill="x",
            pady=(0, 18)
        )

        ttk.Label(
            countdown_card,
            text="NEXT DAY CHECK",
            style="Eyebrow.TLabel"
        ).pack(
            pady=(0, 8)
        )

        self.countdown_label = ttk.Label(
            countdown_card,
            text="",
            style="Countdown.TLabel"
        )

        self.countdown_label.pack()

        ttk.Button(
            sidebar,
            text="Refresh now",
            style="Modern.TButton",
            command=self.manual_refresh
        ).pack(
            anchor="w",
            pady=(0, 18)
        )

        ttk.Label(
            sidebar,
            text="Shortcut: Ctrl + R",
            style="SmallMuted.TLabel"
        ).pack(
            anchor="w"
        )

        legend = ttk.Frame(
            sidebar,
            style="Sidebar.TFrame"
        )

        legend.pack(
            anchor="w",
            side="bottom"
        )

        self.create_legend_item(
            legend,
            self.COLORS["accent_dark"],
            "Current ISO week"
        )

        self.create_legend_item(
            legend,
            self.COLORS["today"],
            "Today"
        )

    def create_legend_item(self, parent, color, text):
        item = ttk.Frame(
            parent,
            style="Sidebar.TFrame"
        )

        item.pack(
            anchor="w",
            pady=3
        )

        marker = tk.Frame(
            item,
            width=12,
            height=12,
            bg=color
        )

        marker.pack(
            side="left",
            padx=(0, 8)
        )

        marker.pack_propagate(False)

        ttk.Label(
            item,
            text=text,
            style="SmallMuted.TLabel"
        ).pack(
            side="left"
        )

    def build_calendar_area(self, parent):
        calendar_area = ttk.Frame(
            parent,
            style="App.TFrame"
        )

        calendar_area.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        calendar_area.grid_rowconfigure(0, weight=0)
        calendar_area.grid_rowconfigure(1, weight=1)
        calendar_area.grid_columnconfigure(0, weight=1)
        calendar_area.grid_columnconfigure(1, weight=1)

        nav_frame = tk.Frame(
            calendar_area,
            bg=self.COLORS["background"]
        )

        nav_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 10)
        )

        nav_btn_kw = dict(
            bg=self.COLORS["surface_alt"],
            fg=self.COLORS["text"],
            activebackground=self.COLORS["button"],
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Inter", 11),
            cursor="hand2",
            padx=12,
            pady=5,
        )

        tk.Button(
            nav_frame,
            text="<",
            command=self.go_prev_month,
            **nav_btn_kw
        ).pack(side="left")

        self.now_button = tk.Button(
            nav_frame,
            text="now",
            command=self.go_to_now,
            **nav_btn_kw
        )

        self.now_button.pack(side="left", padx=6)

        tk.Button(
            nav_frame,
            text=">",
            command=self.go_next_month,
            **nav_btn_kw
        ).pack(side="left")

        self.current_calendar_frame = ttk.Frame(
            calendar_area,
            style="Card.TFrame",
            padding=16
        )

        self.current_calendar_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        self.next_calendar_frame = ttk.Frame(
            calendar_area,
            style="Card.TFrame",
            padding=16
        )

        self.next_calendar_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

    def get_current_iso_week_key(self):
        iso = self.today.isocalendar()
        return iso.year, iso.week

    def is_current_iso_week(self, calendar_date):
        current_year, current_week = self.get_current_iso_week_key()
        iso = calendar_date.isocalendar()

        return (
            iso.year == current_year
            and iso.week == current_week
        )

    def rebuild_calendar(self, frame_container, year, month, subtitle):
        for widget in frame_container.winfo_children():
            widget.destroy()

        for column in range(8):
            frame_container.grid_columnconfigure(
                column,
                weight=1,
                uniform="calendar_columns"
            )

        header = ttk.Frame(
            frame_container,
            style="Card.TFrame"
        )

        header.grid(
            row=0,
            column=0,
            columnspan=8,
            sticky="ew",
            pady=(0, 14)
        )

        ttk.Label(
            header,
            text=f"{calendar.month_name[month]} {year}",
            style="CalendarTitle.TLabel"
        ).pack(
            side="left"
        )

        ttk.Label(
            header,
            text=subtitle,
            style="CalendarSubtitle.TLabel"
        ).pack(
            side="right",
            pady=(4, 0)
        )

        headers = [
            "WK",
            "MON",
            "TUE",
            "WED",
            "THU",
            "FRI",
            "SAT",
            "SUN"
        ]

        for column, header_text in enumerate(headers):
            header_bg = self.COLORS["surface_alt"]

            tk.Label(
                frame_container,
                text=header_text,
                bg=header_bg,
                fg=(
                    self.COLORS["accent"]
                    if column == 0
                    else self.COLORS["text_muted"]
                ),
                font=("Inter", 9, "bold"),
                padx=4,
                pady=6
            ).grid(
                row=1,
                column=column,
                sticky="ew",
                padx=2,
                pady=(0, 5)
            )

        month_calendar = calendar.Calendar(
            firstweekday=calendar.MONDAY
        )

        weeks = month_calendar.monthdatescalendar(year, month)

        for week_row, week in enumerate(weeks, start=2):
            week_is_current = self.is_current_iso_week(week[0])
            week_number = week[0].isocalendar().week

            week_bg = (
                self.COLORS["accent_dark"]
                if week_is_current
                else self.COLORS["surface_alt"]
            )

            week_fg = (
                self.COLORS["text"]
                if week_is_current
                else self.COLORS["text_muted"]
            )

            tk.Label(
                frame_container,
                text=f"{week_number:02d}",
                bg=week_bg,
                fg=week_fg,
                font=("Inter", 10, "bold"),
                width=3,
                pady=5
            ).grid(
                row=week_row,
                column=0,
                sticky="nsew",
                padx=2,
                pady=2
            )

            for day_column, calendar_date in enumerate(week, start=1):
                is_current_month = calendar_date.month == month
                is_current_week = self.is_current_iso_week(calendar_date)
                is_today = calendar_date == self.today

                if is_today:
                    background = self.COLORS["today"]
                    foreground = self.COLORS["today_text"]
                    border_color = self.COLORS["today"]
                    font = ("Inter", 10, "bold")
                elif is_current_week:
                    background = self.COLORS["accent_dark"]
                    foreground = self.COLORS["text"]
                    border_color = self.COLORS["accent"]
                    font = ("Inter", 10, "bold")
                elif not is_current_month:
                    background = self.COLORS["surface_muted"]
                    foreground = self.COLORS["text_faint"]
                    border_color = self.COLORS["surface_muted"]
                    font = ("Inter", 10)
                else:
                    background = self.COLORS["surface_alt"]
                    foreground = self.COLORS["text"]
                    border_color = self.COLORS["surface_alt"]
                    font = ("Inter", 10)

                cell = tk.Frame(
                    frame_container,
                    bg=background,
                    width=42,
                    height=36,
                    highlightthickness=(
                        2 if is_today else 1 if is_current_week else 0
                    ),
                    highlightbackground=border_color,
                    highlightcolor=border_color
                )

                cell.grid(
                    row=week_row,
                    column=day_column,
                    sticky="nsew",
                    padx=2,
                    pady=2
                )

                cell.grid_propagate(False)

                day_label = tk.Label(
                    cell,
                    text=str(calendar_date.day),
                    bg=background,
                    fg=foreground,
                    font=font
                )

                day_label.place(
                    relx=0.5,
                    rely=0.5,
                    anchor="center"
                )

    def rebuild_calendars(self):
        left_month = self.today.month + self.view_offset
        left_year = self.today.year

        while left_month > 12:
            left_month -= 12
            left_year += 1
        while left_month < 1:
            left_month += 12
            left_year -= 1

        right_month = left_month + 1
        right_year = left_year

        if right_month > 12:
            right_month = 1
            right_year += 1

        left_subtitle = "Current month" if self.view_offset == 0 else ""
        right_subtitle = "Next month" if self.view_offset == 0 else ""

        self.rebuild_calendar(
            self.current_calendar_frame,
            left_year,
            left_month,
            left_subtitle
        )

        self.rebuild_calendar(
            self.next_calendar_frame,
            right_year,
            right_month,
            right_subtitle
        )

        self._update_now_button()

    def _update_now_button(self):
        if not hasattr(self, "now_button"):
            return

        if self.view_offset == 0:
            self.now_button.config(fg=self.COLORS["text_faint"])
        else:
            self.now_button.config(fg=self.COLORS["text"])

    def go_prev_month(self):
        self.view_offset -= 1
        self.rebuild_calendars()

    def go_next_month(self):
        self.view_offset += 1
        self.rebuild_calendars()

    def go_to_now(self):
        self.view_offset = 0
        self.rebuild_calendars()

    def refresh_display(self):
        self.today = date.today()
        self.view_offset = 0

        iso_week = self.today.isocalendar().week

        self.root.title(f"W{iso_week:02d}")

        self.week_label.configure(
            text=f"W{iso_week:02d}"
        )

        self.today_label.configure(
            text=self.today.strftime("%A, %d %B %Y")
        )

        self.rebuild_calendars()
        self.schedule_next_refresh()
        self.render_countdown()

    def manual_refresh(self):
        self.refresh_display()

    def schedule_next_refresh(self):
        if self.refresh_job is not None:
            try:
                self.root.after_cancel(self.refresh_job)
            except tk.TclError:
                pass

        now = datetime.now()

        next_midnight = (
            now.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
            + timedelta(days=1)
        )

        self.next_refresh_time = next_midnight

        milliseconds_until_refresh = max(
            100,
            int(
                (
                    self.next_refresh_time - now
                ).total_seconds() * 1000
            )
        )

        self.refresh_job = self.root.after(
            milliseconds_until_refresh,
            self.refresh_display
        )

    def render_countdown(self):
        if self.next_refresh_time is None:
            return

        remaining = self.next_refresh_time - datetime.now()

        if remaining.total_seconds() < 0:
            remaining = timedelta(seconds=0)

        total_seconds = int(remaining.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        self.countdown_label.configure(
            text=(
                "Week display refreshes in\n"
                f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
            )
        )

    def update_countdown(self):
        self.render_countdown()

        if self.countdown_job is not None:
            try:
                self.root.after_cancel(self.countdown_job)
            except tk.TclError:
                pass

        self.countdown_job = self.root.after(
            1000,
            self.update_countdown
        )

    def close(self):
        if self.refresh_job is not None:
            try:
                self.root.after_cancel(self.refresh_job)
            except tk.TclError:
                pass

        if self.countdown_job is not None:
            try:
                self.root.after_cancel(self.countdown_job)
            except tk.TclError:
                pass

        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = WeekNumberApp()
    app.run()
