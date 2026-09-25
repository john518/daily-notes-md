import calendar
from datetime import date

class Api:
    def get_month_data(self, year: int, month: int):
        """
        Generates a flat list of day objects for the given year and month,
        including padding days from adjacent months to fill out the grid.
        """
        print("Enter get_month_data()")
        cal = calendar.Calendar(firstweekday=6) # 6 = Sunday start
        month_days = []

        today_str = date.today().isoformat()

        # cal.itermonthdates(year, month) yields datetime.date objects
        # for the entire grid, including padding days.
        for d in cal.itermonthdates(year, month):
            is_current = (d.month == month)
            is_today = (d.isoformat() == today_str)

            # Format YYMMDD string for filename lookup later (e.g., '260924.md')
            # d.strftime('%y%m%d') will give us e.g. '260924'
            file_key = d.strftime('%y%m%d')

            # TODO: Later this is where you'll check if ~/.local/share/daily-notes-md/{file_key}.md exists
            # and read its content preview. For now, we'll leave it empty.
            content = ""
            if d.isoformat() == "2026-09-24":
                content = "a rat in Tom's house may eat Tom's ice cream" # Mock data check

            month_days.append({
                'date': d.isoformat(),
                'dayNumber': d.day,
                'isCurrentMonth': is_current,
                'isToday': is_today,
                'fileKey': file_key,
                'content': content
            })

        print("Exit get_month_data()")
        return month_days
