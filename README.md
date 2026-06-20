# ⚡ Bus Charging Scheduler

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge\&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=for-the-badge\&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green?style=for-the-badge\&logo=pandas)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

</p>

<p align="center">
<b>Electric Bus Charging Optimization Platform</b><br>
Built using Python & Streamlit
</p>

---

# 🚍 Overview

The **Bus Charging Scheduler** is a scalable and extensible scheduling system designed for electric buses operating between:

### 📍 Route

```text
Bengaluru → A → B → C → D → Kochi
```

The scheduler intelligently determines:

✅ Charging Stations

✅ Charging Order

✅ Waiting Times

✅ Final Arrival Times

while satisfying all operational constraints.

---

# 🎯 Problem Statement

Each electric bus:

| Parameter         | Value      |
| ----------------- | ---------- |
| Initial Battery   | Full       |
| Maximum Range     | 240 km     |
| Charging Time     | 25 minutes |
| Charging Stations | A, B, C, D |

The scheduler must:

* Select charging stations
* Resolve charger contention
* Calculate waiting times
* Optimize charging decisions

---

# ✨ Key Features

## 🧠 Smart Scheduling Engine

* Event-Driven Simulation
* Dynamic Charging Decisions
* Resource Reservation
* Wait-Time Management
* Arrival-Time Prediction

---

## ⚙️ Optimization Support

Supports configurable optimization goals:

| Optimization Factor | Description             |
| ------------------- | ----------------------- |
| Individual Priority | Best outcome per bus    |
| Operator Fairness   | Fair charger allocation |
| Network Efficiency  | Reduce overall delays   |

---

## 🔮 Future-Proof Architecture

Supports:

* ➕ Additional Stations
* 🔌 Multiple Chargers
* 🚦 Priority Vehicles
* 💰 Electricity Pricing
* 👨‍✈️ Driver Constraints
* 🛣 Multiple Routes
* 📊 Advanced Policies

without changing the scheduling engine.

---

# 🖥️ User Interface

Built with **Streamlit**

### Dashboard Features

* 📋 Scenario Selection
* 🚌 Bus Timetables
* ⚡ Charging Queue Visualization
* 📈 Scheduler Metrics
* 📊 Performance Summary

---

# 🏗️ Technology Stack

| Layer           | Technology   |
| --------------- | ------------ |
| Backend         | Python 3.11+ |
| UI              | Streamlit    |
| Data Processing | Pandas       |
| Storage         | JSON         |

---

# 📂 Project Structure

```text
bus-charging-scheduler/
│
├── app.py
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
│
├── scenarios/
│   ├── scenario_1.json
│   ├── scenario_2.json
│   ├── scenario_3.json
│   ├── scenario_4.json
│   └── scenario_5.json
│
└── scheduler/
    ├── __init__.py
    ├── models.py
    ├── utils.py
    ├── validators.py
    ├── scoring.py
    ├── rules.py
    └── engine.py
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone <repository-url>

cd bus-charging-scheduler
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

Start Streamlit:

```bash
streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

# ⚙️ Scenario Configuration

All scenarios are stored in:

```text
scenarios/
```

Each scenario contains:

* Route Configuration
* Station Configuration
* Bus Schedules
* Optimization Weights

Example:

```json
{
  "weights": {
    "individual": 1.0,
    "operator": 1.0,
    "overall": 1.0
  }
}
```

---

# 🎚️ Change Optimization Weights

Simply modify the scenario file.

```json
{
  "weights": {
    "individual": 1.0,
    "operator": 2.0,
    "overall": 1.0
  }
}
```

✅ No code changes required.

The scheduler automatically picks up the new values.

---

# 🧩 Add New Scheduling Rules

Create a new rule in:

```text
scheduler/rules.py
```

Example:

```python
class PeakHourRule(BaseRule):

    def evaluate(self, context):

        if context["hour"] in [18, 19, 20]:
            return 10

        return 0
```

Register:

```python
rules.append(PeakHourRule())
```

✅ No changes required in the engine.

---

# ⚡ Add A New Charging Station

Example:

```json
{
  "name": "E",
  "distance_from_start": 520,
  "chargers": 2
}
```

Add it to the scenario configuration.

The scheduler automatically includes it.

---

# 🔌 Add Additional Chargers

Example:

```json
{
  "name": "B",
  "chargers": 4
}
```

No engine modification required.

The scheduler dynamically adjusts capacity.

---

# 📏 Validation Rules

The system validates:

### 🔋 Battery Range

Maximum travel distance between charges:

```text
240 km
```

---

### ⚡ Charger Capacity

Only available chargers may be assigned.

---

### ➡️ Station Order

Buses can only move forward along the route.

---

### ⏱ Charging Duration

Each charging session:

```text
25 Minutes
```

---

# 🏛️ Scheduler Architecture

The solution follows three major principles:

## Event-Driven Scheduling

Buses are simulated as events moving through the route network.

## Rule-Based Scoring

Every charging decision is evaluated using configurable weighted rules.

## Resource Reservation

Charging stations maintain reservation queues to avoid conflicts.

---

# 📌 Assumptions

The scheduler assumes:

* Constant bus speed
* No traffic delays
* Fixed charging duration
* Full battery after charging
* No charger failures
* Predefined routes
* Continuous station operation
* Fixed departure schedules

---

# 🔮 Future Enhancements

Planned improvements include:

* 🌍 Multiple Routes
* 🚦 Dynamic Traffic
* ⚡ Variable Charging Duration
* 💰 Real-Time Electricity Pricing
* 👨‍✈️ Driver Shift Planning
* 🔧 Charger Maintenance
* 🚍 Priority Vehicle Support
* 📡 Real-Time Dispatch Optimization

---

# ☁️ Deployment

Deploy easily using Streamlit Community Cloud.

### Steps

```text
1. Push project to GitHub
2. Open Streamlit Community Cloud
3. Connect GitHub Repository
4. Select app.py
5. Deploy
```

---

# 👨‍💻 Author

### Amal Saju

**Bus Charging Scheduler**
Take-Home Assignment

Built with ❤️ using Python and Streamlit

---

<p align="center">
⚡ Smart Charging • Fair Scheduling • Efficient Operations ⚡
</p>
