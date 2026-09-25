from dataclasses import dataclass

@dataclass
class DayEntry:
    """Represents a single day cell in the calendar grid with its metadata and content.

    Encapsulates all necessary date properties, state flags, and markdown content
    required by the frontend calendar view and backend storage layer.

    Attributes:
        year (int): The 4-digit year (e.g., 2026).
        month (int): The month of the year (1-12).
        day (int): The day of the month (1-31).
        dayNumber (int): Explicit day number for frontend grid rendering.
        weekday (int): The day of the week (0 for Monday through 6 for Sunday).
        isCurrentMonth (bool): True if the day belongs to the actively viewed month,
            false if it is a padding day from an adjacent month.
        isToday (bool): True if this day matches the current system date.
        fileKey (str): Unique string identifier in YYMMDD format used for file paths
            and lookup keys.
        content (str): The raw markdown text of the journal entry for this day.
    """
    year: int
    month: int
    day: int          # The day of the month (1-31)
    dayNumber: int    # Alias/explicit field for day number if preferred
    weekday: int      # 0 (Monday) to 6 (Sunday)
    isCurrentMonth: bool
    isToday: bool
    fileKey: str      # e.g., "260925" for easy identification/keys
    content: str      # Markdown content loaded from disk
