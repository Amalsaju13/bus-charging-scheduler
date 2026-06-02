import os
import pandas as pd
import streamlit as st

from scheduler.engine import SchedulerEngine
from scheduler.utils import (
    load_scenario,
    minutes_to_time
)

SCENARIO_DIR = "scenarios"

st.set_page_config(
    page_title="Bus Charging Scheduler",
    page_icon="🚌",
    layout="wide"
)

st.title("⚡🔋🚍 Bus Charging Scheduler")

# -----------------------------
# Scenario Selection
# -----------------------------

scenario_files = sorted(
    [
        file
        for file in os.listdir(SCENARIO_DIR)
        if file.endswith(".json")
    ]
)

selected_scenario = st.selectbox(
    "Select Scenario",
    scenario_files
)

# -----------------------------
# Load Scenario
# -----------------------------

try:

    scenario_path = os.path.join(
        SCENARIO_DIR,
        selected_scenario
    )

    scenario = load_scenario(
        scenario_path
    )

except Exception as e:

    st.error(
        f"Failed to load scenario: {e}"
    )

    st.stop()

# -----------------------------
# Tabs
# -----------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Scenario Input",
        "Bus Timetable",
        "Station Queues",
        "Metrics"
    ]
)

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader("Scenario Details")

    st.write(
        f"Scenario: {scenario['scenario_name']}"
    )

    st.subheader("Weights")

    st.json(
        scenario["weights"]
    )

    st.subheader("Stations")

    station_df = pd.DataFrame(
        scenario["route"]["stations"]
    )

    st.dataframe(
        station_df,
        use_container_width=True
    )

    st.subheader("Buses")

    bus_df = pd.DataFrame(
        scenario["buses"]
    )

    st.dataframe(
        bus_df,
        use_container_width=True
    )

# =====================================================
# RUN ENGINE
# =====================================================

engine = SchedulerEngine(
    scenario
)

results = engine.run()

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader(
        "Per Bus Timetable"
    )

    rows = []

    for schedule in results:

        if not schedule.charge_events:

            rows.append(
                {
                    "Bus": schedule.bus_id,
                    "Operator": schedule.operator,
                    "Direction": schedule.direction,
                    "Station": "N/A",
                    "Arrival": "",
                    "Wait": 0,
                    "Charge Start": "",
                    "Charge End": "",
                    "Final Arrival":
                        minutes_to_time(
                            schedule.final_arrival
                        ),
                }
            )

        for event in schedule.charge_events:

            rows.append(
                {
                    "Bus": schedule.bus_id,
                    "Operator": schedule.operator,
                    "Direction": schedule.direction,
                    "Station": event.station,
                    "Arrival":
                        minutes_to_time(
                            event.arrival_time
                        ),
                    "Wait":
                        event.wait_time,
                    "Charge Start":
                        minutes_to_time(
                            event.charge_start
                        ),
                    "Charge End":
                        minutes_to_time(
                            event.charge_end
                        ),
                    "Final Arrival":
                        minutes_to_time(
                            schedule.final_arrival
                        ),
                }
            )

    bus_table = pd.DataFrame(
        rows
    )

    st.dataframe(
        bus_table,
        use_container_width=True
    )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader(
        "Station Charging Order"
    )

    station_rows = []

    for station_name, queue in engine.station_queues.items():

        queue = sorted(
            queue,
            key=lambda x: x["start"]
        )

        for position, item in enumerate(
            queue,
            start=1
        ):

            station_rows.append(
                {
                    "Station":
                        station_name,
                    "Order":
                        position,
                    "Bus":
                        item["bus_id"],
                    "Start":
                        minutes_to_time(
                            item["start"]
                        ),
                    "End":
                        minutes_to_time(
                            item["end"]
                        )
                }
            )

    station_df = pd.DataFrame(
        station_rows
    )

    st.dataframe(
        station_df,
        use_container_width=True
    )

# =====================================================
# TAB 4
# =====================================================

with tab4:

    st.subheader(
        "Network Metrics"
    )

    total_wait = sum(
        schedule.total_wait
        for schedule in results
    )

    bus_count = len(
        results
    )

    avg_wait = (
        total_wait / bus_count
        if bus_count
        else 0
    )

    max_wait = max(
        (
            schedule.total_wait
            for schedule in results
        ),
        default=0
    )

    total_charge_events = sum(
        len(schedule.charge_events)
        for schedule in results
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Buses",
            bus_count
        )

        st.metric(
            "Average Wait (mins)",
            round(avg_wait, 2)
        )

    with col2:

        st.metric(
            "Maximum Wait (mins)",
            max_wait
        )

        st.metric(
            "Charging Sessions",
            total_charge_events
        )

    st.subheader(
        "Operator Utilization"
    )

    operator_counts = {}

    for bus in scenario["buses"]:

        op = bus["operator"]

        operator_counts[op] = (
            operator_counts.get(op, 0)
            + 1
        )

    op_df = pd.DataFrame(
        [
            {
                "Operator": k,
                "Buses": v
            }
            for k, v in operator_counts.items()
        ]
    )

    st.dataframe(
        op_df,
        use_container_width=True
    )
