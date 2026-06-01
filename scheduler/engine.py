from collections import defaultdict

from scheduler.models import ChargeEvent, BusSchedule
from scheduler.utils import (
    time_to_minutes,
    travel_time,
)
from scheduler.scoring import compute_score


class SchedulerEngine:
    def __init__(self, scenario):
        self.scenario = scenario
        self.weights = scenario["weights"]
        self.battery_range = scenario["battery_range_km"]
        self.charge_time = scenario["charge_time_minutes"]
        self.speed = scenario["speed_kmph"]

        self.stations = scenario["route"]["stations"]

        self.station_lookup = {
            s["name"]: s for s in self.stations
        }

        self.station_queues = defaultdict(list)
        self.operator_usage = defaultdict(int)

    def run(self):
        schedules = []

        buses = sorted(
            self.scenario["buses"],
            key=lambda x: time_to_minutes(x["departure_time"])
        )

        for bus in buses:
            schedule = self.schedule_bus(bus)
            schedules.append(schedule)

        return schedules

    def schedule_bus(self, bus):
        direction = bus["direction"]

        if direction == "forward":
            route = self.stations
        else:
            route = list(reversed(self.stations))

        current_time = time_to_minutes(bus["departure_time"])
        current_index = 0

        battery_remaining = self.battery_range

        schedule = BusSchedule(
            bus_id=bus["id"],
            operator=bus["operator"],
            direction=direction,
        )

        while current_index < len(route) - 1:

            best_station = None
            best_score = float("inf")
            best_data = None

            possible_paths = self.generate_possible_stops(
                route,
                current_index,
                battery_remaining,
            )

            for station_index in possible_paths:

                station = route[station_index]

                if station["chargers"] == 0:
                    continue

                distance = (
                    abs(
                        route[station_index]["distance_from_start"]
                        - route[current_index]["distance_from_start"]
                    )
                )

                travel_minutes = travel_time(distance, self.speed)

                arrival_time = current_time + travel_minutes

                queue = self.station_queues[station["name"]]

                available_time = arrival_time

                if queue:
                    latest_end = max(q["end"] for q in queue)
                    available_time = max(arrival_time, latest_end)

                wait_time = available_time - arrival_time

                operator_penalty = self.operator_usage[
                    bus["operator"]
                ]

                network_penalty = len(queue)

                score = compute_score(
                    wait_time,
                    operator_penalty,
                    network_penalty,
                    self.weights,
                )

                if score < best_score:
                    best_score = score
                    best_station = station
                    best_data = {
                        "arrival_time": arrival_time,
                        "wait_time": wait_time,
                        "charge_start": available_time,
                        "charge_end": available_time + self.charge_time,
                        "station_index": station_index,
                    }

            if best_station is None:
                break

            charge_event = ChargeEvent(
                station=best_station["name"],
                arrival_time=best_data["arrival_time"],
                wait_time=best_data["wait_time"],
                charge_start=best_data["charge_start"],
                charge_end=best_data["charge_end"],
                departure_time=best_data["charge_end"],
            )

            schedule.charge_events.append(charge_event)

            self.station_queues[best_station["name"]].append(
                {
                    "bus_id": bus["id"],
                    "start": best_data["charge_start"],
                    "end": best_data["charge_end"],
                }
            )

            self.operator_usage[bus["operator"]] += 1

            current_time = best_data["charge_end"]
            current_index = best_data["station_index"]
            battery_remaining = self.battery_range

            remaining_distance = abs(
                route[-1]["distance_from_start"]
                - route[current_index]["distance_from_start"]
            )

            if remaining_distance <= self.battery_range:
                final_travel = travel_time(
                    remaining_distance,
                    self.speed,
                )

                schedule.final_arrival = current_time + final_travel
                break

        schedule.total_wait = sum(
            event.wait_time
            for event in schedule.charge_events
        )

        return schedule

    def generate_possible_stops(
        self,
        route,
        current_index,
        battery_remaining,
    ):

        current_distance = route[current_index][
            "distance_from_start"
        ]

        possible = []

        for i in range(current_index + 1, len(route)):

            distance = abs(
                route[i]["distance_from_start"]
                - current_distance
            )

            if distance <= battery_remaining:
                possible.append(i)

        return possible