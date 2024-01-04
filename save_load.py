import json
import time
import messages


# Save game state
def save_game_state(file_name, game_state):
    try:
        with open(file_name, 'w') as file:
            json.dump(game_state, file)
            print("Game state saved successfully!")
    except IOError:
        print("Error: Unable to save game state.")


def choose_slot(is_load: bool):
    from main import Game
    # Show save slots
    for i, slot in enumerate(messages.Messages.SAVE_SLOTS):
        print(f"Save Slot {i + 1}: {slot}")
    print("Choose a slot")
    # Save game based on selected slot
    time.sleep(0.7)
    game_obj = Game()
    game_obj.menu("resources/images/Icons/save_state.png", "resources/sounds/18 BGM #14.wav",
                  messages.Messages.SAVE_SLOTS, False, 300, 100)
    slot_index = game_obj.state.selected_option
    selected_slot = messages.Messages.SAVE_SLOTS[slot_index]
    game_state = {
        'player_x': "TEST",
        'score': 0
    }
    if is_load:
        save_game_state(f"{selected_slot}.json", game_state)
        print(f"Game saved in {selected_slot}!")
    else:
        load_game_state(f"{selected_slot}.json")
        print(f"Game loaded in {selected_slot}!")


# Load game state
def load_game_state(file_name):
    save = MenuState()
    try:
        with open(file_name, 'r') as file:
            save.game_state = json.load(file)
            print("Game state loaded successfully!")
            return save.game_state
    except (IOError, json.JSONDecodeError):
        print("Error: Unable to load game state.")


class MenuState:
    def __init__(self):
        self.selected_slot = None
        self.game_state = {}

    def run(self):
        choose_slot()
        print("")


def test():
    save_obj = MenuState()
    save_obj.run()
