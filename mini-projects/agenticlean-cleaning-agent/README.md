# AgentiClean: Cleaning Agent

An agent program that act on N number of rooms and clean them based on its utility functions that aims to conserving power while cleaning as much rooms as possible.

## Project Requirements

> ### Objective:
>
> Develop a Python-based intelligent agent that operates in a linear environment of configurable size, cleaning rooms with varying dirtiness levels while managing a limited, scaled energy budget efficiently.
>
> ### Environment Description:
>
> The environment contains N rooms, indexed from 0 to N-1. Each room may be:
> Clean, or
> Dirty with a dirtiness level between 1 and 5.
> The agent starts in room 0.
>
> ### Energy Constraints:
>
> The agent is assigned an initial energy of:
> Initial Energy = 2.5×N (e.g., for 10 rooms → 25 units).
>
> #### Energy costs:
>
> -   Suck (cleaning): costs equal to the room's dirtiness level (1–5).
> -   MoveLeft or MoveRight: cost = 2 units per move.
>
> The agent cannot take an action if it lacks the energy required for it.
>
> ### Agent Capabilities:
>
> #### Percepts:
>
> -   Current room index.
> -   Room state (clean or dirty).
> -   Dirtiness level (if dirty).
> -   Remaining energy.
>
> #### Actuators / Actions:
>
> -   Suck: Clean the current room.
> -   MoveLeft: Move to the previous room.
> -   MoveRight: Move to the next room.
>
> ### Simulation Rules:
>
> -   The agent operates in discreet timesteps, up to a max of T which is Parameter to be specified by the user (ex. 100).
> -   At each time step, any clean room has a 10% chance to become dirty again with a random dirtiness level.
> -   The simulation ends when either:
>     -   All rooms are clean, and the agent has no meaningful actions left (i.e., nothing to clean and no reason to move).
>     -   The agent runs out of usable energy, and cannot afford any further actions (Suck, MoveLeft, or MoveRight).
>     -   A maximum number of steps T (e.g., 100) is reached to prevent infinite loops.
>
> ### Basic Agent Behavior (Baseline):
>
> 1. If the current room is dirty and energy allows → Suck.
> 2. Else, move right (or left at the boundary) if enough energy.
> 3. Stop if no further action is possible.
>
> Advanced students can implement planning or heuristics to optimize energy use.
>
> ### Output Requirements:
>
> -   Final state of each room.
> -   Number of rooms cleaned.
> -   Total energy consumed.
> -   Final remaining energy.
> -   Sequence of actions taken.

## Project Report

### 1. Introduction

This report details the design, behavior, and performance observations of an intelligent agent developed to clean rooms within a linear environment. The agent's primary objective is to efficiently clean as many rooms as possible, given a limited energy budget and dynamic environmental conditions, by optimizing its actions through a planning mechanism. This document will cover the architectural design choices, summarize the agent's decision-making process, and discuss its observed performance.

### 2. Explanation of Design Decisions

The agent's design is modular, separating concerns into distinct Python files: `agenticlean.py`, `agent_lang.py`, `agent_utils.py`, and `environment.py`. This modularity enhances readability, maintainability, and scalability.

#### 2.1. Modular Structure

**`environment.py`**: This file encapsulates all environmental logic. It manages the state of rooms (cleanliness and dirtiness levels), handles the random re-dirtification of clean rooms, and provides methods for the agent to perceive the environment. This separation ensures the agent operates without direct knowledge of the environment's internal mechanics, only its perceived state.

**`agent_lang.py`**: This file defines enumerations for various states and actions that exposed to external files (main and environment), such as `RoomStatus`, `RunningState`, `AgentAction`, and `ActionCost`. Using enums provides type safety, improves code readability by replacing "magic numbers" with descriptive names, and makes the system's states and actions explicit.

**`agent_utils.py`**: This file defines data structures used for communication between the agent and the environment or within the agent's processing logic. `RoomState`, `PerceivedState`, and `DecisionMade` act as clear contracts for data flow, ensuring that information is consistently structured and easily interpretable.

**`agenticlean.py`**: This is the core of the intelligent agent. It contains the agent's internal state, its perception, processing, and action logic. The clear separation of `_perceive`, `_process`, and `_act` methods follows the traditional "sense-plan-act" agent architecture.

#### 2.2. Agent Architecture (AgentiClean)

The `AgentiClean` class is designed as a stateful agent. It maintains its `current_location`, `energy_level`, `num_rooms_cleaned`, and a memory of the last optimized environment state (`_last_optimized_env`).

**`_perceive()`**: This method gathers information from the Environment to construct a `PerceivedState` object. It includes the current room's state and a snapshot of all rooms' statuses. This full environmental snapshot is crucial for the agent's global planning.

**`_process()`**: This is the intelligent core, where the agent decides its next action. The key design decision here is the implementation of a dynamic programming approach for optimal action planning, specifically within the `_find_optimal_actions_rev` method.

**Optimal Planning (`_find_optimal_actions_rev`)**: This method uses recursion with memoization (via the `cases` dictionary) to find the sequence of actions that will maximize the number of cleaned rooms given the current energy budget and environmental state. It explores all possible valid "Suck," "MoveLeft," and "MoveRight" actions from the current state, calculating the maximum rooms it can clean from each path. The function returns the maximum cleaned rooms and the reversed list of optimal actions. This allows the agent to construct a proactive plan rather than making greedy, short-sighted decisions.

**Environmental Change Detection**: The agent recalculates its optimal plan (`_optimal_actions_rev`) only if the environment state (`state.environment_state`) has changed since the last optimization. This is an important optimization to avoid redundant, computationally expensive replanning.

**Optimistic Waiting Strategy**: A notable design decision is the agent's ability to `TURN_IDLE`. If the current room or an adjacent room is clean, and there's sufficient "running time" left (`self._max_running_time - current_time`), the agent will opt to wait rather than immediately execute a planned action. This heuristic is designed to exploit the 10% chance of a clean room becoming dirty, potentially allowing the agent to clean more rooms in the long run if a previously clean room re-dirtifies. The `_max_cleaned_room` check also helps decide if waiting is beneficial (if all cleanable rooms are already accounted for in the plan, it executes).

**`_act()`**: This method executes the chosen `AgentAction`. It updates the agent's internal state (location, energy, rooms cleaned) and modifies the environment by calling `environment.suck_room()` when `SUCK` is performed.

### 3. Agent Behavior Summary

The AgentiClean operates in discrete timesteps, following a "perceive-process-act" cycle.

#### 3.1. Percepts

At each timestep, the agent perceives the following information:

-   Its current room index.
-   The state of the current room (clean or dirty).
-   The dirtiness level of the current room (if dirty).
-   Its remaining energy.
-   The complete state of all rooms in the environment. This global view is crucial for its planning algorithm.

#### 3.2. Decision-Making Process

The agent's decision-making is driven by its optimal planning algorithm (`_find_optimal_actions_rev`), combined with an adaptive waiting strategy.

**Environment Check**: The agent first checks if the global environment state (the cleanliness of all rooms) has changed since its last plan was computed.

**Optimal Plan Computation (if needed)**:

If the environment has changed, the agent recalculates an optimal plan. This plan is a sequence of Suck, MoveLeft, or MoveRight actions designed to maximize the total number of rooms cleaned, given the agent's current energy, position, and the current state of all rooms. The `_find_optimal_actions_rev` function uses dynamic programming to explore the "best" possible path.

The plan is stored as a reversed list of actions (`_optimal_actions_rev`), so `pop()` can be used to retrieve the next action efficiently.

**Adaptive Waiting**: Before executing the next action from its optimal plan, the agent evaluates a specific condition:

If the current room is already clean, OR if an adjacent room (left or right) is clean, AND the simulation hasn't reached its maximum time limit too closely (i.e., there are enough timesteps left for the current plan to execute), AND the agent cannot clean all the rooms with the energy given, the agent will `TURN_IDLE`. This means it does not take an action for the current timestep, allowing the environment to potentially change (a clean room might become dirty), and then replans in the next timestep. This is an optimistic strategy, hoping for new cleaning opportunities.

However, if the agent has already calculated a plan that cleans all the dirty rooms currently in the environment (`self._max_cleaned_room >= self._environment.get_num_dirty_rooms()`), it will stick to its plan rather than idling, as no better outcome can be achieved by waiting.

**Action Execution**:

If the agent decides not to `TURN_IDLE`, it executes the next action from its `_optimal_actions_rev` plan.

Actions include `SUCK` (cleaning the current room), `MOVE_LEFT`, or `MOVE_RIGHT`.

Energy is consumed for each action, and the agent cannot perform an action if it lacks the required energy.

**Termination Conditions**: The simulation ends when:

-   The agent runs out of usable energy and cannot afford any further actions (`RunningState.OFF`).
-   All rooms are clean, and the agent has no meaningful actions left (`env.are_all_rooms_clean()`).
-   A maximum number of steps (T) is reached.

#### 3.3. Actuators

The agent can perform the following actions, provided it has sufficient energy:

-   **Suck**: Cleans the current room. Cost equals the room's dirtiness level.
-   **MoveLeft**: Moves to the adjacent room on the left. Cost is 2 units.
-   **MoveRight**: Moves to the adjacent room on the right. Cost is 2 units.
-   **TurnOff**: The agent shuts down, typically when it can no longer take beneficial actions due to lack of energy.
-   **TurnIdle**: The agent performs no action for the current timestep (loop iteration), waiting for environmental changes for optimization purposes.

### 4. Performance Observations

The agent's performance is significantly influenced by its planning mechanism and the adaptive waiting strategy.

#### 4.1. Energy Efficiency and Room Cleaning Maximization

The `_find_optimal_actions_rev` function employs a dynamic programming approach, where the agent explicitly calculates the maximum number of rooms it can clean given its current energy and the global state of the environment. This is a significant improvement over a simple baseline agent (e.g., always suck if dirty, else move right) that might get stuck in local optima or waste energy on sub-optimal paths.

**Proactive Planning**: Instead of reactive decision-making, the agent attempts to map out the most effective sequence of actions. This allows it to prioritize high-dirtiness rooms if they are along an optimal path, or strategically move to reach more rooms within its energy budget.

**Energy Conservation**: The planning inherently considers energy costs for each path. If a path to clean more rooms requires too much energy, it simply won't be chosen as optimal. This leads to efficient energy usage towards the goal of maximizing cleaned rooms.

**Complexity Optimizations**: The dynamic programming approach has a computational cost, especially in larger environments. The state space for `_find_optimal_actions_rev` is `(position, energy, tuple(room_states))`, which can grow significantly. However, memoization (`cases` dictionary) drastically reduces redundant computations by storing results for previously encountered states. For the given problem constraints (linear environment, limited dirtiness levels), this approach is feasible and effective.

#### 4.2. Impact of the Adaptive Waiting Strategy (TURN_IDLE)

The `TURN_IDLE` action introduces a fascinating dynamic to the agent's behavior and performance.

**Potential Benefit**: The 10% chance of a clean room becoming dirty again can be leveraged by the agent. If the agent waits when nearby rooms are clean, there's a chance a valuable cleaning opportunity (a newly dirty room) will emerge, potentially allowing it to clean more rooms overall than if it blindly followed a pre-calculated plan that assumed static dirty rooms. This aligns with a long-term optimization strategy.

**Eliminating the Drawbacks of Waiting Strategy**: The condition `(self._max_running_time - current_time <= len(self._optimal_actions_rev))` attempts to mitigate the drawback of reaching maximum steps T with enough energy to clean rooms by forcing the agent to stop waiting and execute its plan if time is running out. Similarly, if the current plan already cleans all currently dirty rooms, waiting becomes pointless, therefore, the agent will not wait and will execute its plan as fast as possible before a clean room turns to a dirty one.

### 5. Conclusion

In conclusion, the agent demonstrates intelligent behavior by not just reacting to its immediate surroundings but by planning several steps ahead. This foresight, combined with its adaptive waiting, makes it way performant than the approach that acts based on current room state and remaining energy level alone. The latter may spend all its energy in one room with high dirtiness level, while the implemented approach will clean several less dirty rooms with the same amount of energy.

Moreover, the agent's ability to recalculate plans based on environmental changes makes it robust to the dynamic nature of the problem (rooms randomly becoming dirty). Also, it even uses this dynamic change of the environment into its favor. If the agent has more time and close to a clean room, it will wait to see wether the room will become dirty, so it will plan again the best actions to take to clean as much rooms as possible. However, this waiting technique will be applied only if the agent cannot clean all the rooms with its given energy.
