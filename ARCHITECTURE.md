Bus Charging Scheduler Architecture

Overview



This project implements a scalable and extensible bus charging scheduler for electric buses operating between Bengaluru and Kochi.



The scheduler is responsible for:



Determining charging stations used by each bus

Determining charging order at each station

Calculating waiting times

Computing final arrival times

Respecting all hard constraints

Supporting configurable optimization priorities through weights



The solution is implemented using Python and Streamlit and is intentionally designed to be data-driven and extensible.



Scheduling Framework

Chosen Approach



I implemented an Event-Driven Scheduling Framework with a Rule-Based Scoring Engine.



The scheduler works in four stages:



Scenario Loading

Path Generation

Charging Schedule Evaluation

Charger Reservation Simulation



Each bus is simulated independently while sharing charger resources through station queues.



Why Event-Driven Scheduling?



Several approaches were considered:



Brute Force Search



Pros:



Potentially finds optimal schedules



Cons:



Search space grows exponentially

Difficult to scale

Difficult to modify when new rules are introduced

Constraint Solver (OR-Tools)



Pros:



Strong optimization capabilities



Cons:



More complex than required

Harder to explain and extend quickly

Higher implementation complexity

Event-Driven Simulation (Chosen)



Pros:



Easy to understand

Easy to extend

Supports additional rules naturally

Scales better as operational complexity grows

Closely models real-world charging behavior



For these reasons, an event-driven scheduling framework was selected.



System Components

Scenario Layer



Responsible for loading scenario data from JSON files.



Contains:



Route definition

Station configuration

Charging configuration

Optimization weights

Bus schedules



This allows behavior changes without modifying application code.



Scheduling Engine



Responsible for:



Bus movement simulation

Charging decisions

Queue management

Resource allocation



The scheduling engine is independent from the UI.



Rule Engine



The scheduler evaluates candidate charging decisions using pluggable rules.



Current rules:



Wait Time Rule



Goal:



Minimize excessive waiting by individual buses.



Operator Balance Rule



Goal:



Prevent one operator from consistently receiving worse schedules than others.



Network Efficiency Rule



Goal:



Reduce overall congestion across charging stations.



Each rule contributes a weighted score.



Scoring Engine



Every charging decision receives a score:



Score =

(Individual Weight × Wait Time)

\+

(Operator Weight × Operator Penalty)

\+

(Overall Weight × Network Penalty)



The decision with the lowest score is selected.



This allows business priorities to change without changing scheduling logic.



Data Model Design

Station



Represents a charging location.



Fields:



{

&#x20; "name": "B",

&#x20; "distance\_from\_start": 220,

&#x20; "chargers": 1

}



Supports:



Additional stations

Multiple chargers

Station-specific metadata

Bus



Represents an individual trip.



Fields:



{

&#x20; "id": "bus-BK-01",

&#x20; "operator": "kpn",

&#x20; "direction": "forward",

&#x20; "departure\_time": "19:00"

}



Supports:



Additional operators

Different battery sizes

Priority vehicles

Scenario



Represents a complete simulation environment.



Contains:



Route

Stations

Buses

Configuration

Weights



Scenarios are entirely data-driven.



Hard Constraints



The scheduler enforces:



Battery Constraint



Maximum travel distance between charges:



240 km



Charger Capacity Constraint



Only one bus can occupy a charger at a time.



Charging Duration Constraint



Every charging session lasts exactly 25 minutes.



Route Order Constraint



Buses may only travel forward along their route.



No backtracking is allowed.



Scalability Design



The architecture was intentionally designed to support future growth.



Future Change 1: More Charging Stations



Example:



A → B → C → D → E → F



Support:



No code changes required.



Only scenario data changes.



Future Change 2: Multiple Chargers Per Station



Example:



{

&#x20; "name": "B",

&#x20; "chargers": 4

}



Support:



No engine redesign required.



Only configuration changes.



Future Change 3: Additional Operators



Example:



KPN

Freshbus

Flixbus

KSRTC



Support:



No code changes required.



Future Change 4: Multiple Routes



Example:



Bengaluru → Kochi

Bengaluru → Chennai



Support:



Route is represented as scenario data.



Additional routes can be added through configuration.



Future Change 5: Different Battery Capacities



Example:



{

&#x20; "battery\_range\_km": 300

}



Support:



Already supported through configuration.



Future Change 6: Priority Buses



Example:



Emergency or VIP vehicles.



Support:



Add a PriorityRule.



No scheduling engine rewrite required.



Future Change 7: Electricity Pricing



Example:



Different charging costs at different times.



Support:



Add ElectricityCostRule.



No engine redesign required.



Future Change 8: Driver Shift Constraints



Example:



Maximum driving hours.



Support:



Add DriverShiftRule.



No engine redesign required.



Future Change 9: Charger Outages



Example:



Station temporarily loses chargers.



Support:



Modify charger count in scenario configuration.



Weight Modification



Weights are stored inside scenario configuration.



Example:



{

&#x20; "weights": {

&#x20;   "individual": 1.0,

&#x20;   "operator": 2.0,

&#x20;   "overall": 1.0

&#x20; }

}



Changing optimization priorities requires updating only these values.



No code changes are required.



Adding a New Rule



New rules can be added by implementing BaseRule.



Example:



class PeakHourRule(BaseRule):



&#x20;   def evaluate(self, context):



&#x20;       if context\["hour"] in \[18, 19, 20]:

&#x20;           return 10



&#x20;       return 0



Then register:



rules.append(PeakHourRule())



No scheduling engine changes are required.



Assumptions



The following assumptions were made:



All buses travel at a constant speed.

Traffic conditions are ignored.

Charging always restores a full battery.

Charging duration is fixed at 25 minutes.

Chargers never fail during simulation.

Buses follow predefined routes.

Stations operate continuously.

Departure schedules are fixed.



These assumptions simplify simulation while preserving scheduling complexity.



Conclusion



The solution prioritizes:



Extensibility

Scalability

Maintainability

Clear separation of concerns



The architecture allows new rules, new stations, new routes, and new operational constraints to be added with minimal changes, ensuring the scheduler can evolve as business requirements grow.



