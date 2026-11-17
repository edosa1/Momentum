from datetime import date, timedelta


def calculate_current_streak(completion_dates):
    """
    completion_dates: a set of date objects the habit was marked done on.
    Returns how many consecutive days (ending today or yesterday) are unbroken.
    """
    if not completion_dates:
        return 0

    today = date.today()

    # If today isn't done, the streak might still be "alive" if yesterday was done
    # (you haven't broken it yet, just haven't logged today).
    if today in completion_dates:
        cursor = today
    elif (today - timedelta(days=1)) in completion_dates:
        cursor = today - timedelta(days=1)
    else:
        return 0  # neither today nor yesterday done — streak is broken

    streak = 0
    while cursor in completion_dates:
        streak += 1
        cursor -= timedelta(days=1)

    return streak


def calculate_longest_streak(completion_dates):
    """
    Finds the longest run of consecutive days anywhere in history,
    not just the current one.
    """
    if not completion_dates:
        return 0

    sorted_dates = sorted(completion_dates)
    longest = 1
    current = 1

    for i in range(1, len(sorted_dates)):
        gap = (sorted_dates[i] - sorted_dates[i - 1]).days
        if gap == 1:
            current += 1
            longest = max(longest, current)
        elif gap > 1:
            current = 1  # streak broken, restart counting from this day

    return longest
