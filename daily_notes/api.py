import calendar
from dataclasses import asdict
from datetime import datetime, date

from .day_entry import DayEntry

class Api:
    def __init__(self, storage):
        self.storage = storage

    def ping(self):
        """Health check endpoint to verify backend is responsive."""
        return {
            "status": "ok",
            "timestamp": datetime.now().isoformat()
        }

    def get_month_data(self, year: int, month: int):
        print(f"get_month_data for {year}, {month}")
        month_entries = self.storage.get_month_entries(year, month)
        cal = calendar.Calendar(firstweekday=6) # Sunday start, adjust if Monday start (0)

        today = date.today()
        month_days = []

        for day_info in cal.itermonthdays4(year, month):
            y, m, d, wd = day_info
            is_current = (m == month)

            # If it's outside the current month (padding days), d is still part of the grid
            # but we can handle content and keys appropriately.
            content = month_entries.get(d, "") if is_current else ""

            # Construct fileKey (YYMMDD format) for current month days
            yy_str = f"{y % 100:02d}"
            mm_str = f"{m:02d}"
            dd_str = f"{d:02d}"
            file_key = f"{yy_str}{mm_str}{dd_str}" if is_current else ""

            is_today = (y == today.year and m == today.month and d == today.day) if is_current else False

            day_obj = DayEntry(
                year=y,
                month=m,
                day=d,
                dayNumber=d,
                weekday=wd,
                isCurrentMonth=is_current,
                isToday=is_today,
                fileKey=file_key,
                content=content
            )

            month_days.append(asdict(day_obj))

        print(month_days)
        return month_days

    def save_entry(self, year: int, month: int, day: int, content: str):
        self.storage.write_entry(year, month, day, content)
        return {"status": "saved"}
