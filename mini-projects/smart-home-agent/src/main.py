from SmartHomeAgent import *

def Main():
    """
    Entry point for the Smart Home simulation.
    Initializes the agent and runs multiple simulation cycles, 
    modifying the environment dynamically between cycles.
    """
    NumberOfCycles = 6
    HomeAgent = SmartHomeAgent()

    print("\n---------------- Simulation Started -------------------")
    print("Initial Knowledge Base:")
    for Feature, RoomStates in HomeAgent.KnowledgeBase.items():
        print(f"  {Feature}: {RoomStates}")
    print("---------------------------------------------------------\n\n\n")

    for CycleNumber in range(1, NumberOfCycles):
        print(f"\n\n=============== Simulation Cycle {CycleNumber} ===============")
        HomeAgent.RunAgent()
        ChangeEnvironment(HomeAgent, CycleNumber)

    print("\n\n\n\n------------ Simulation Ended --------------")
    print("Final Knowledge Base:")
    for Feature, RoomStates in HomeAgent.KnowledgeBase.items():
        print(f"  {Feature}: {RoomStates}")


def ChangeEnvironment(HomeAgent, CycleNumber: int):
    """
    Dynamically modifies the knowledge base to simulate real-world changes 
    such as lighting, motion, temperature, and presence of people.
    """
    if CycleNumber == 1:
        print("\nDynamically changing facts for next cycle")
        HomeAgent.KnowledgeBase['dark']['room1'] = False
        print("  - room1 is no longer dark")
        HomeAgent.KnowledgeBase['motion']['room1'] = False
        print("  - room1 has no motion now")
        HomeAgent.KnowledgeBase['cold']['room1'] = False 
        print("  - room1 is no longer cold")
        HomeAgent.KnowledgeBase['person_present']['room1'] = False
        print("  - room1 has no people now")
    elif CycleNumber == 2:
        print("\nDynamically changing facts for next cycle")
        HomeAgent.KnowledgeBase['hot']['room2'] = False  
        print("  - room2 is no longer hot")
        HomeAgent.KnowledgeBase['motion']['room2'] = True
        print("  - room2 has motion now")
        HomeAgent.KnowledgeBase['dark']['room2'] = True
        print("  - room2 is dark now")
    elif CycleNumber == 3:
        print("\nDynamically changing facts for next cycle")
        HomeAgent.KnowledgeBase['hot']['room2'] = True 
        print("  - room2 is hot now")
        HomeAgent.KnowledgeBase['cold']['room1'] = True
        print("  - room1 is cold now")
        HomeAgent.KnowledgeBase['person_present']['room2'] = True
        print("  - room2 has people")
    elif CycleNumber == 4:
        print("\nDynamically changing facts for next cycle")
        HomeAgent.KnowledgeBase['light_on']['room3'] = True
        HomeAgent.KnowledgeBase['dark']['room3'] = False
        print("  - Adding new room (room3) with lights On and its Dark")
        HomeAgent.KnowledgeBase['person_present']['room4'] = True
        HomeAgent.KnowledgeBase['cold']['room4'] = True
        HomeAgent.KnowledgeBase['windows_open']['room4'] = True
        print("  - Adding new room (room4) with a person in it, cold, and windows open")


if __name__ == "__main__":
    Main()
