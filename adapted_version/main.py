import random
from ai import call_gpt

ROOMS_TO_ESCAPE = 5
ITEMS = ["weapon", "boots", "shield"]

class Player:
    def __init__(self, name):
        self.name = name
        self.room = 0
        self.inventory = []

    def has_item(self, item):
        return item in self.inventory

def roll_dice(mod=0):
    return random.randint(1, 6) + mod

def short_gpt_prompt(prompt):
    print("Loading story...")
    return call_gpt(prompt + " Keep it very short, 1-2 sentences max.")

def describe_room(player):
    return short_gpt_prompt(
        f"Describe briefly the appearance of dungeon room {player.room + 1} with 3 suspicious door hints: A, B, and C."
    )

def get_enemy_threshold(enemy_strength):
    return {"weak": 3, "medium": 5, "strong": 7}[enemy_strength]

def encounter_enemy(player, enemy_strength):
    threshold = get_enemy_threshold(enemy_strength)
    print(f"A {enemy_strength} enemy appears! You must roll at least a {threshold} to defeat it.")
    print("Do you want to fight or try to escape? (Escape: success if you roll 4 or more)")

    while True:
        action = input("Choose (F)ight or (E)scape: ").strip().upper()
        if action in ["F", "E"]:
            break
        print("Invalid input. Please enter F or E.")

    if action == "E":
        escape_roll = roll_dice()
        print(f"You rolled a {escape_roll} to escape...")
        if escape_roll >= 4:
            print("You managed to escape safely. You remain in the same room.")
        else:
            print("You failed to escape. The enemy blocks your way.")
        return

    # Fight
    mod = 1 if player.has_item("weapon") else 0
    if mod > 0:
        print("You grip your weapon tightly... it gives you an edge in battle (+1 to your roll).")
    player_roll = roll_dice(mod)
    print(f"You rolled a {player_roll} to fight.")

    if player_roll >= threshold:
        print("You defeated the enemy and move forward!")
        player.room += 1
    else:
        if player.has_item("shield"):
            print("You were defeated... but your shield absorbs the blow and shatters in the process. You stay in place.")
            player.inventory.remove("shield")
        else:
            print("You were defeated and fall back one room.")
            player.room = max(0, player.room - 1)

def room_outcome(player):
    chance = random.random()
    difficulty_modifier = player.room / ROOMS_TO_ESCAPE

    if chance < 0.3 - difficulty_modifier:
        print("The room is eerily silent... nothing happens. You move forward.")
        player.room += 1
    elif chance < 0.6:
        enemy_strength = random.choices(
            ["weak", "medium", "strong"], weights=[4, 3, 2]
        )[0]
        encounter_enemy(player, enemy_strength)
    else:
        item = random.choices(
            ITEMS, weights=[2, 1, 1 if player.room > 2 else 0]
        )[0]
        print(f"You found a treasure chest containing a {item}!")
        if not player.has_item(item):
            player.inventory.append(item)
        else:
            print(f"You already had a {item}, so you leave it.")

        if item == "boots":
            print("You feel lighter... the boots speed you forward by one extra room!")
            player.room += 2
        else:
            player.room += 1

def choose_door():
    while True:
        choice = input("Choose a door (A, B, C): ").strip().upper()
        if choice in ["A", "B", "C"]:
            return choice
        print("Invalid choice. Please choose A, B, or C.")

def main():
    print("WELCOME TO ESCAPE THE DUNGEON!")
    name = input("What is your name, prisoner? ")
    player = Player(name)

    intro = short_gpt_prompt(
        f"Speak directly to {player.name} as a mysterious voice. Explain briefly he must escape 5 rooms with traps, enemies, and treasures. Wish him luck."
    )
    print(intro)

    while player.room < ROOMS_TO_ESCAPE:
        print(f"\nRoom {player.room + 1} of {ROOMS_TO_ESCAPE}")
        print(describe_room(player))
        _ = choose_door()
        print("You open the door...")
        room_outcome(player)
        print(f"Progress: Room {player.room}/{ROOMS_TO_ESCAPE}")
        print(f"Inventory: {player.inventory}")

    print(f"\nCongratulations, {player.name}! You escaped the dungeon alive!")

if __name__ == "__main__":
    main()