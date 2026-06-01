import json


def time_to_minutes(time_str: str) -> int:
    h, m = map(int, time_str.split(":"))
    return h * 60 + m



def minutes_to_time(minutes: int) -> str:
    minutes = minutes % (24 * 60)

    h = minutes // 60
    m = minutes % 60

    return f"{h:02d}:{m:02d}"



def load_scenario(path: str):
    with open(path, "r") as f:
        return json.load(f)



def travel_time(distance_km: int, speed_kmph: int):
    return int((distance_km / speed_kmph) * 60)