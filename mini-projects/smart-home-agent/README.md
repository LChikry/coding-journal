# 🏠 Smart Home Agent Simulation

This project simulates a **rule-based intelligent agent** that manages a smart home environment. The agent monitors sensor inputs like motion, light, temperature, and presence, and then makes decisions such as turning on/off lights, opening/closing windows, or activating heating.

## Features

-   Simulates an environment with multiple rooms
-   Dynamically changes room states over simulation cycles
-   Applies predefined rules to make logical decisions
-   Demonstrates a clear **sense → reason → act** agent cycle
-   Fully documented with PascalCase naming conventions

## Agent Rules

The agent uses the following rules for decision-making:

1. **Motion & Darkness** → Turn on the light.
2. **No Motion & Light On** → Turn off the light.
3. **Cold, Person Present & Windows Open** → Close the windows (simulate heater activation).
4. **Hot, Person Present & Windows Closed** → Open the windows.
5. **Not Hot & Windows Open** → Close the windows.
6. **Light On & Not Dark** → Turn off the light.

## File Structure

```bash
.
├── src
├──── main.py               # Entry point to run the simulation
├──── SmartHomeAgent.py     # Contains the SmartHomeAgent class and logic
└── README.md             # Project documentation
```

## How to Run

1. Clone the repo or download the source files:

```bash
git clone https://github.com/your-username/smart-home-agent.git
cd smart-home-agent
```

2. Run the simulation:

```bash
python3 main.py
```

3. Watch how the agent senses, reasons, and acts over 5 simulation cycles!

## Requirements

-   Python 3.6+
-   No external libraries required (pure Python)

## Learning Outcomes

-   Practice writing rule-based intelligent agents
-   Understand how to simulate dynamic environments
-   Learn and apply structured coding conventions and documentation practices
