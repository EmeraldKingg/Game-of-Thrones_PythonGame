class Item:
    """Represents collectible items in the game"""

    def __init__(self, name, description, usable_in=None):
        self.name = name
        self.description = description
        self.usable_in = usable_in # Location name where item is used

    def __str__(self):
        return self.name

class NPC:
    """Represents non-player characters that can block paths"""

    def __init__(self, name, dialogue, required_item=None, defeated=False):
        self.name = name
        self.dialogue = dialogue
        self.required_item = required_item # Item needed to defeat/bypass
        self.defeated = defeated

class Location:
    """Represents a room/area in Westeros"""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {} # dict: {"north": Location_object}
        self.items = [] # list of Item objects
        self.npc = None # NPC object if present
        self.locked = False

    def add_exit(self, direction, location):
        self.exits[direction] = location

    def add_item(self, item):
        self.items.append(item)

    def describe(self):
        desc = f"\n=== {self.name} ===\n{self.description}\n"
        if self.items:
            desc += "You see: " + ", ".join([item.name for item in self.items]) + "\n"
        if self.npc and not self.npc.defeated:
            desc += f"{self.npc.name} is here. {self.npc.dialogue}\n"
        if self.exits:
            desc += "Exits: " + ", ".join(self.exits.keys()) + "\n"
        return desc

class Character:
    """Represents the player"""

    def __init__(self, name, house, start_location):
        self.name = name
        self.house = house
        self.current_location = start_location
        self.satchel = [] # Max 4 items
        self.health = 100

    def move(self, direction):
        if direction in self.current_location.exits:
            new_location = self.current_location.exits[direction]

            # 1. Check if new location is locked
            if new_location.locked:
                if any(item.name == "Seal of the Hand" for item in self.satchel):
                    new_location.locked = False
                    print("The guards see the Seal of the Hand. You may pass.")
                else:
                    return "The path is locked. You need proper authority."

            # 2. Move into the new location
            self.current_location = new_location

            # 3. Print NPC dialogue if they are undefeated, but DO NOT use 'return' 
            # so the player successfully finishes their move.
            if new_location.npc and not new_location.npc.defeated:
                print(f"\n[{new_location.npc.name} is here!]")
                print(f"'{new_location.npc.dialogue}'")

            return f"You travel to {new_location.name}."
        else:
            # Matches exact spec: "You know nothing, Jon Snow. Try again!"
            return "You know nothing, Jon Snow. Try again!"

    def take_item(self, item_name):
        for item in self.current_location.items:
            if item.name.lower() == item_name.lower():
                if len(self.satchel) < 4:
                    self.current_location.items.remove(item)
                    self.satchel.append(item)
                    return f"You take the {item.name}. {item.description}"
                else:
                    return "Your satchel is full, like Lord Tywin's coffers."
        return "That item isn't here."

    def use_item(self, item_name, target_name=None):
        # Find item in satchel
        item = next((i for i in self.satchel if i.name.lower() == item_name.lower()), None)
        if not item:
            return "You don't have that item."

        npc = self.current_location.npc

        # Special case: Seal of the Hand at King's Landing after Clegane is dead
        if item.name == "Seal of the Hand" and self.current_location.name == "King's Landing":
            if npc and not npc.defeated:
                return "You must defeat Gregor Clegane before claiming the throne."
            return "You show the Seal of the Hand. The city guards kneel. You claim the Iron Throne!"

        # Normal NPC interactions
        if not npc or npc.defeated:
            return "There's nothing to use that on here."

        # Dragonglass vs Night King
        if item.name == "Dragonglass Dagger" and npc.name == "Night King":
            npc.defeated = True
            return "You plunge the dagger into the Night King. He shatters into ice!"

        # Valerian Steel vs The Hound
        if item.name == "Valyrian Steel Sword" and npc.name == "The Hound":
            npc.defeated = True
            return "You draw your sword. 'Fuck the Kingsguard,' The Hound grunts, then steps aside. 'Go on then.'"

        # Valerian Steel vs Gregor Clegane
        if item.name == "Valerian Steel Sword" and npc.name == "Gregor Clegane":
            npc.defeated = True
            return "CLEGANEBOWL! Your Valerian steel cuts through The Mountain. You win!"

        return f"The {item.name} has no effect on {npc.name}."

    def show_satchel(self):
        if self.satchel:
            return "Satchel: " + ", ".join([item.name for item in self.satchel]) + f" [{len(self.satchel)}/4]"
        else:
            return "Your satchel is empty."

def setup_game():
    # Create all locations
    castle_black = Location("Castle Black", "The last bastion of the Night's Watch. Cold winds howl.")
    the_wall = Location("The Wall", "700 feet of ice. Something moves in the darkness beyond.")
    winterfell = Location("Winterfell", "Home of House Stark. The crypts lie below.")
    the_neck = Location("The Neck", "Swamps and crannogs. The path is treacherous.")
    dragonstone = Location("Dragonstone", "Ancient Targaryen stronghold. Obsidian litters the beach.")
    the_twins = Location("The Twins", "House Frey's castle. The bridge is heavily guarded.")
    riverrun = Location("Riverrun", "Tully stronghold, surrounded by rivers.")
    harrenhal = Location("Harrenhal", "Cursed castle. Whispers echo in the ruins.")
    the_eyrie = Location("The Eyrie", "Impregnable fortress in the sky.")
    kings_landing = Location("King's Landing", "Capital of the Seven Kingdoms. The Iron Throne awaits.")

    # Add ship route to bypass The Wall
    castle_black.add_exit("east", dragonstone)
    dragonstone.add_exit("west", castle_black)

    # Connect locations - two way paths
    # Connect locations - two way paths matching your project map
    castle_black.add_exit("south", the_wall)
    the_wall.add_exit("north", castle_black)
    
    the_wall.add_exit("south", winterfell)
    winterfell.add_exit("north", the_wall)
    
    winterfell.add_exit("south", the_neck)
    the_neck.add_exit("north", winterfell)
    
    the_neck.add_exit("east", dragonstone)
    dragonstone.add_exit("west", the_neck)
    
    the_neck.add_exit("south", riverrun)
    riverrun.add_exit("north", the_neck)
    
    riverrun.add_exit("east", the_twins)
    the_twins.add_exit("west", riverrun)
    
    riverrun.add_exit("south", harrenhal)
    harrenhal.add_exit("north", riverrun)
    
    harrenhal.add_exit("east", kings_landing)
    kings_landing.add_exit("west", harrenhal)
    
    kings_landing.add_exit("east", the_eyrie)
    the_eyrie.add_exit("west", kings_landing)

    # Create and place items
    dragonstone.add_item(Item("Dragonglass Dagger", "Kills White Walkers", "The Wall"))
    winterfell.add_item(Item("Valerian Steel Sword", "Forged with dragon fire", "King's Landing"))
    harrenhal.add_item(Item("Seal of the Hand", "Grants authority in King's Landing", "King's Landing"))
    the_eyrie.add_item(Item("Map to Dragonstone", "Contains secrets of the Vale", "The Eyrie"))
    kings_landing.add_item(Item("Wildfire Jar", "Burns with green flame", "King's Landing"))

    # Create and place NPCs/Bosses
    the_wall.npc = NPC("Night King", "The Long Night comes for all.", "Dragonglass Dagger")
    the_twins.npc = NPC("The Hound", "Bugger off. Pay the toll or fight me.", "Valerian Steel Sword")
    kings_landing.npc = NPC("Gregor Clegane", "The Mountain stands before the Iron Throne.", "Valerian Steel Sword")
    kings_landing.locked = True

    locations = {
        "Castle Black": castle_black, "The Wall": the_wall, "Winterfell": winterfell,
        "The Neck": the_neck, "Dragonstone": dragonstone, "The Twins": the_twins,
        "Riverrun": riverrun, "Harrenhal": harrenhal, "The Eyrie": the_eyrie,
        "King's Landing": kings_landing
    }

    return locations


def check_win(player, locations):
    night_king_dead = any(
        loc.npc and loc.npc.name == "Night King" and loc.npc.defeated 
        for loc in locations.values()
    )
    clegane_dead = any(
        loc.npc and loc.npc.name == "Gregor Clegane" and loc.npc.defeated 
        for loc in locations.values()
    )

    iron_throne = player.current_location.name == "King's Landing" and clegane_dead
    has_seal = any(item.name == "Seal of the Hand" for item in player.satchel)
    # Define 'has_sword' so the computer knows what it is!
    has_sword = any(item.name == "Valerian Steel Sword" for item in player.satchel)

    # Both items must be in the satchel to claim the throne
    if night_king_dead and iron_throne and has_seal and has_sword:
        return "You defeated the Night King AND claimed the Iron Throne. You win the Game of Thrones!"
    return None

    

def main():
    locations = setup_game()

    print("=== A GAME OF THRONES: CLAIM THE THRONE ===")
    name = input("Enter your character name: ")
    house = input("Choose your house: ")
    player = Character(name, house, locations["Castle Black"])

    print(f"\nWelcome, {player.name} of {player.house}.")
    print("Defeat the Night King and claim the Iron Throne to win.")
    print("Type 'help' for commands.\n")

    while True:
        print(player.current_location.describe())
        print(player.show_satchel())

        command = input("\nWhat do you do? > ").lower().strip()

        if command in ["north", "south", "east", "west"]:
            print(player.move(command))
        elif command.startswith("take "):
            item_name = command[5:]
            print(player.take_item(item_name))
        elif command.startswith("use "):
            parts = command[4:].split(" on ")
            item_name = parts[0]
            print(player.use_item(item_name))
        elif command == "satchel":
            print(player.show_satchel())
        elif command == "help":
            print("Commands: north, south, east, west | take [item] | use [item] | satchel | quit")
        elif command == "quit":
            print("You abandon your quest. Game over.")
            break
        else:
            # Updated to match success criteria 10 exactly
            print("You know nothing, Jon Snow. Try again!")

        win_message = check_win(player, locations)
        if win_message:
            print(f"\n{win_message}")
            break #this stops the game when the win condition is met

if __name__ == "__main__":
    main()