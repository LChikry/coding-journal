import os
if not os.environ.get("DISPLAY"):
    os.environ["DISPLAY"] = ":0"


from PlayingTheGame import *

if __name__ == "__main__":
    try:
        game = PlayingTheGame()
        game.PlayGame()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please try running the game again.") 