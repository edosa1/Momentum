from datetime import date, timedelta
from habit_tracker.streaks import calculate_current_streak, calculate_longest_streak

TODAY = date.today()


def days_ago(n):
    return TODAY - timedelta(days=n)


def test_current_streak_empty():
    assert calculate_current_streak(set()) == 0


def test_current_streak_active_today():
    dates = {days_ago(0), days_ago(1), days_ago(2)}
    assert calculate_current_streak(dates) == 3


def test_current_streak_still_alive_if_yesterday_done():
    # Haven't logged today yet, but yesterday and the day before were done.
    dates = {days_ago(1), days_ago(2)}
    assert calculate_current_streak(dates) == 2


def test_current_streak_broken_if_two_days_missed():
    dates = {days_ago(2), days_ago(3)}
    assert calculate_current_streak(dates) == 0


def test_longest_streak_finds_past_run():
    # A 4-day run in the past, then a gap, then today alone.
    dates = {
        days_ago(10), days_ago(9), days_ago(8), days_ago(7),
        days_ago(0),
    }
    assert calculate_longest_streak(dates) == 4


def test_longest_streak_empty():
    assert calculate_longest_streak(set()) == 0
