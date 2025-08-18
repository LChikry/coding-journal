class SmartHomeAgent:
    """
    Represents a smart home automation agent that uses a rule-based system
    to manage lighting and environmental controls in different rooms based
    on motion, temperature, and presence of people.
    """

    def __init__(self):
        """
        Initializes the knowledge base with predefined sensor states
        for various features across rooms.
        """
        self.KnowledgeBase = {
            "motion": {"room1": True, "room2": False},
            "dark": {"room1": True, "room2": False},
            "light_on": {"room1": False, "room2": True},
            "cold": {"room1": True, "room2": False},
            "person_present": {"room1": True, "room2": False},
            "hot": {"room2": True},
            "windows_open": {"room1": False, "room2": False}
        }

    def RunAgent(self):
        """
        Executes the agent's perception-reasoning-action cycle
        and logs the results of applied rules.
        """
        RoomList = self.SenseEnvironment()
        Decisions = self.ApplyRules(RoomList)
        self.LogDecisions(Decisions)

    def LogDecisions(self, DecisionsTaken):
        """
        Logs all actions taken during the reasoning phase.
        """
        print("\nAgent decisions:")
        if not DecisionsTaken:
            print("  - No specific actions taken in this cycle.")
        else:
            for Decision in DecisionsTaken:
                print(f"  - {Decision}")

    def SenseEnvironment(self):
        """
        Updates the knowledge base by ensuring all rooms are accounted for
        across all feature categories, and prints the current state.
        """
        print("Sensing environment (Current KB state):")
        Features = self.KnowledgeBase
        RoomNames = list(set([Room for FeatureRooms in Features.values() for Room in FeatureRooms.keys()]))

        RoomAdditionLog = []
        for Feature, RoomStates in Features.items():
            for Room in RoomNames:
                if Room not in RoomStates:
                    RoomAdditionLog.append(f"  - {Room} has been added to Knowledge base in {Feature} section.")
                RoomStates.setdefault(Room, False)
            print(f"  {Feature}: {RoomStates}")

        print("\nAdded Rooms to Knowledge Base:")
        if not RoomAdditionLog:
            print("  - No rooms have been added in this cycle.")
        else:
            for Log in RoomAdditionLog:
                print(Log)
        return RoomNames

    def SwitchFeatureState(self, Feature: str, Room: str):
        """
        Toggles the state of a given feature in a specified room.
        """
        assert Feature in self.KnowledgeBase, f"Error: Feature '{Feature}' not found in knowledge base."
        assert Room in self.KnowledgeBase[Feature], f"Error: Room '{Room}' not found for feature '{Feature}'."
        self.KnowledgeBase[Feature][Room] = not self.KnowledgeBase[Feature][Room]

    def ApplyRules(self, RoomList: list[str]):
        """
        Applies a series of conditional rules to manage home automation
        features based on the current knowledge base state.
        """
        Decisions = []
        KB = self.KnowledgeBase
        for Room in RoomList:
			# Rule 1: If motion is detected and it's dark, turn on the light.
            if KB['motion'][Room] and KB['dark'][Room] and not KB['light_on'][Room]:
                self.SwitchFeatureState('light_on', Room)
                Decisions.append(f"Turned on light in {Room} due to motion and dark.")

			# Rule 2: If no motion and light is on, turn it off.
            if not KB['motion'][Room] and KB['light_on'][Room]:
                self.SwitchFeatureState('light_on', Room)
                Decisions.append(f"Turned off light in {Room} due to no motion detected.")

			# Rule 3: If it's cold, a person exist, and windows are open, close the windows
            if KB['cold'][Room] and KB['person_present'][Room] and KB['windows_open'][Room]:
                self.SwitchFeatureState('windows_open', Room)
                Decisions.append(f"Closed windows in {Room} due to cold and person present.")

			# Rule 4: If it's hot, a person exist, and windows are closed, open the windows.
            if KB['hot'][Room] and not KB['windows_open'][Room] and KB['person_present'][Room]:
                self.SwitchFeatureState('windows_open', Room)
                Decisions.append(f"Opened windows in {Room} due to hot temperature.")

			# rule 5: if it's no longer hot and windows are open, close the windows.
            if not KB['hot'][Room] and KB['windows_open'][Room]:
                self.SwitchFeatureState('windows_open', Room)
                Decisions.append(f"Closed windows in {Room} as it's no longer hot.")

			# Rule 6: If light is on, and it's no longer dark, turn off the light.
            if KB['light_on'][Room] and not KB['dark'][Room]:
                self.SwitchFeatureState('light_on', Room)
                Decisions.append(f"Turned off light in {Room} as it's no longer dark.")

        return Decisions