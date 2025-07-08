import random

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.location = "town_square"

class Enemy:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

class Game:
    def __init__(self):
        self.player = None
        self.locations = {
            "town_square": {
                "name": "Town Square",
                "description": "You're in a square town.",
                "exits": {"north": "market", "east": "forest_entrance"},
                "enemies": []
            },
            "market": {
                "name": "Marketplace",
                "description": "This is even more bazaar.",
                "exits": {"south": "town_square"},
                "enemies": []
            },
            "forest_entrance": {
                "name": "Forest Entrance",
                "description": "REALLY scarey forest. Cool stuff in there though.",
                "exits": {"west": "town_square"},
                "enemies": [Enemy("Weirdo", 30, 8)]
            }
        }
    
    def create_character(self):
        name = input("Enter your name: ")
        self.player = Player(name)
        print(f"\nWelcome, {self.player.name}!")
    
    def display_status(self):
        print(f"\nHP: {self.player.hp}/{self.player.max_hp}")
    
    def display_location(self):
        loc = self.locations[self.player.location]
        print(f"\n{loc['name']}\n{'-' * len(loc['name'])}")
        print(loc['description'])
        print("\nExits: " + ", ".join(loc['exits'].keys()))
        
        # Show enemies
        if loc['enemies']:
            print(f"\nEnemies here: {', '.join(e.name for e in loc['enemies'])}")
    
    def move(self, direction):
        loc = self.locations[self.player.location]
        if direction in loc['exits']:
            self.player.location = loc['exits'][direction]
            print(f"\nYou go {direction}...")
            self.check_combat()
            return True
        print("\nYou can't go that way!")
        return False
    
    def check_combat(self):
        loc = self.locations[self.player.location]
        if loc['enemies']:
            enemy = random.choice(loc['enemies'])
            print(f"\nA {enemy.name} attacks you!")
            self.combat(enemy)
    
    def combat(self, enemy):
        while self.player.hp > 0 and enemy.hp > 0:
            print(f"\n{self.player.name} HP: {self.player.hp}")
            print(f"{enemy.name} HP: {enemy.hp}")
            
            action = input("\nChoose action: [A]ttack, [R]un: ").lower()
            
            if action == "a":
                damage = random.randint(self.player.attack - 2, self.player.attack + 2)
                enemy.hp -= damage
                print(f"You deal {damage} damage to {enemy.name}!")
            elif action == "r":
                if random.random() < 0.5:
                    print("You escaped!")
                    return
                print("Escape failed!")
            else:
                print("Invalid action!")
                continue
            
            if enemy.hp <= 0:
                print(f"\nYou defeated the {enemy.name}!")
                return
            
            # Enemy attack
            enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 2)
            self.player.hp -= enemy_damage
            print(f"The {enemy.name} hits you for {enemy_damage} damage!")
            
            if self.player.hp <= 0:
                print("\n=== YOU ARE DEFEATED! ===")
                self.player.hp = 1
                self.player.location = "town_square"
                print("You wake up in the town square. Must've been a bad dream.")
                return
    
    def run(self):
        print("=== TEXT RPG v2: CHARACTER & COMBAT ===")
        self.create_character()
        
        while True:
            self.display_location()
            self.display_status()
            
            command = input("\nCommand (move/attack/status/quit): ").lower()
            
            if command == "quit":
                print("Goodbye!")
                break
            elif command in ["north", "south", "east", "west"]:
                self.move(command)
            elif command == "attack":
                loc = self.locations[self.player.location]
                if loc['enemies']:
                    self.combat(random.choice(loc['enemies']))
                else:
                    print("No enemies here!")
            elif command == "status":
                self.display_status()
            else:
                print("Invalid command!")

if __name__ == "__main__":
    game = Game()
    game.run()