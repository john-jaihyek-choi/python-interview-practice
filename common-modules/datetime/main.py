from datetime import datetime, timedelta


def get_current_time() -> None:
    now = datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))


def get_time_difference() -> None:
    now = datetime.now()
    delta = now + timedelta(hours=3600)
    difference = delta - now
    print(f"difference between now and delta = {difference.days}")


get_current_time()
get_time_difference()
