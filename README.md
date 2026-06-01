Bus Charging Scheduler

Overview



This project implements a scalable and extensible Bus Charging Scheduler for electric buses operating between Bengaluru and Kochi.



The scheduler determines:



Which charging stations each bus should use

The charging order at each station

Waiting times caused by charger contention

Final arrival times for all buses



The application is built using Python and Streamlit and is designed to support future operational requirements without major code changes.



Problem Statement



Electric buses travel along the following route:



Bengaluru → A → B → C → D → Kochi



Each bus:



Starts with a full battery

Has a maximum range of 240 km

Charges only at stations A, B, C and D

Requires 25 minutes for a full charge



Each station has limited charger capacity.



The scheduler must determine:



Charging plans

Charging priorities

Waiting times



while respecting all hard constraints.



Features

Scheduler

Event-driven scheduling engine

Dynamic charging station selection

Charger reservation system

Battery range validation

Wait time calculation

Final arrival time calculation

Optimization



Supports configurable optimization weights:



Individual Bus Priority

Operator Fairness

Overall Network Efficiency

Extensibility



Supports future changes including:



Additional stations

Multiple chargers

New operators

Priority buses

Electricity pricing

Driver constraints

Multiple routes

UI



Built using Streamlit.



Provides:



Scenario Selection

Scenario Input View

Per Bus Timetable

Per Station Charging Queue

Scheduler Metrics

Technology Stack

Backend

Python 3.11+

UI

Streamlit

Data Processing

Pandas

Data Storage

JSON

Project Structure

bus-charging-scheduler/

│

├── app.py

├── requirements.txt

├── README.md

├── ARCHITECTURE.md

│

├── scenarios/

│   ├── scenario\_1.json

│   ├── scenario\_2.json

│   ├── scenario\_3.json

│   ├── scenario\_4.json

│   └── scenario\_5.json

│

└── scheduler/

&#x20;   ├── \_\_init\_\_.py

&#x20;   ├── models.py

&#x20;   ├── utils.py

&#x20;   ├── validators.py

&#x20;   ├── scoring.py

&#x20;   ├── rules.py

&#x20;   └── engine.py

Installation

Clone Repository

git clone <repository-url>

cd bus-charging-scheduler

Create Virtual Environment



Windows:



python -m venv venv



Activate:



venv\\Scripts\\activate



Linux / Mac:



python3 -m venv venv

source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

Running The Application



Start Streamlit:



streamlit run app.py



Application will open at:



http://localhost:8501

Scenario Configuration



Scenarios are stored inside:



scenarios/



Each scenario contains:



Route configuration

Station configuration

Bus schedules

Optimization weights



Example:



{

&#x20; "weights": {

&#x20;   "individual": 1.0,

&#x20;   "operator": 1.0,

&#x20;   "overall": 1.0

&#x20; }

}

How To Change Optimization Weights



Modify the scenario JSON file.



Example:



{

&#x20; "weights": {

&#x20;   "individual": 1.0,

&#x20;   "operator": 2.0,

&#x20;   "overall": 1.0

&#x20; }

}



No code changes are required.



The scheduler automatically uses the updated values.



How To Add A New Rule



Create a new rule class in:



scheduler/rules.py



Example:



class PeakHourRule(BaseRule):



&#x20;   def evaluate(self, context):



&#x20;       if context\["hour"] in \[18, 19, 20]:

&#x20;           return 10



&#x20;       return 0



Register the rule:



rules.append(PeakHourRule())



No changes to the scheduling engine are required.



How To Add A New Station



Example:



{

&#x20; "name": "E",

&#x20; "distance\_from\_start": 520,

&#x20; "chargers": 2

}



Add the station to the scenario file.



No engine modifications are required.



How To Add Additional Chargers



Example:



{

&#x20; "name": "B",

&#x20; "chargers": 4

}



Only the configuration changes.



The scheduler automatically uses the new charger capacity.



Assumptions



The following assumptions were made:



All buses travel at a constant speed

Traffic conditions are ignored

Charging always restores a full battery

Charging duration is fixed at 25 minutes

Chargers do not fail

Routes are predefined

Stations operate continuously

Departure schedules are fixed

Validation Rules



The scheduler validates:



Battery Range



A bus cannot travel more than 240 km between charges.



Charger Capacity



Only available chargers may be assigned.



Station Order



Buses must move forward along the route.



Charging Duration



Each charging session lasts exactly 25 minutes.



Scheduler Design



The solution uses:



Event-Driven Scheduling



Buses are simulated as events moving through the network.



Rule-Based Scoring



Each charging decision is evaluated using weighted rules.



Resource Reservation



Charging stations maintain reservation queues to prevent charger conflicts.



Future Improvements



Potential future enhancements include:



Multiple routes

Dynamic traffic conditions

Variable charging durations

Dynamic electricity pricing

Driver shift optimization

Real-time dispatch adjustments

Charger maintenance schedules

Priority vehicle support

Deployment



This application can be deployed directly using Streamlit Community Cloud.



Steps:



Push repository to GitHub

Open Streamlit Community Cloud

Connect GitHub repository

Select app.py

Deploy

Author



Amal Saju



Bus Charging Scheduler – Take Home Assignment



Built using Python and Streamlit.

