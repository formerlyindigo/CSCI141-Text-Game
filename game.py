import random

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.gold = 50
        self.inventory = []
        self.location = "town_square"
        self.quests = {"Weirdos": 0}
    
    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_level:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)
        
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        
        print(f"\n=== LEVEL UP! You're now level {self.level} ===")
        print(f"HP: {self.max_hp}, ATK: {self.attack}")

class Enemy:
    def __init__(self, name, hp, attack, exp):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.exp = exp

class Item:
    def __init__(self, name, item_type, value, price=0):
        self.name = name
        self.type = item_type
        self.value = value
        self.price = price

#alright enough of the joke descriptions I like the weirdos though...
class Game:
    def __init__(self):
        self.player = None
        self.locations = {
            "town_square": {
                "name": "Town Square",
                "description": "You're in the bustling town square.",
                "exits": {"north": "market", "east": "forest_entrance"},
                "enemies": [],
                "shop": []
            },
            "market": {
                "name": "Marketplace",
                "description": "Colorful stalls line the streets.",
                "exits": {"south": "town_square"},
                "enemies": [],
                "shop": [
                    Item("Health Potion", "consumable", 20, 10),
                    Item("Sword", "weapon", 5, 50)
                ]
            },
            "forest_entrance": {
                "name": "Forest Entrance",
                "description": "Thick trees mark the entrance to the forest.",
                "exits": {"west": "town_square"},
                "enemies": [Enemy("Weirdo", 30, 8, 25)],
                "shop": []
            }
        }
        self.quests = {
            "Weirdos": {"target": 3, "reward": 100}
        }
    

    
    def combat(self, enemy):
        while self.player.hp > 0 and enemy.hp > 0:
            print(f"\n{self.player.name} HP: {self.player.hp}")
            print(f"{enemy.name} HP: {enemy.hp}")
            
            action = input("\nChoose action: [A]ttack, [U]se item, [R]un: ").lower()
            
            if action == "a":
                damage = random.randint(self.player.attack - 2, self.player.attack + 2)
                enemy.hp -= damage
                print(f"You deal {damage} damage to {enemy.name}!")
            elif action == "u":
                self.show_inventory()
                item_name = input("Enter item name to use: ").lower()
                self.use_item(item_name)
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
                gold_gained = random.randint(5, 15)
                self.player.gold += gold_gained
                print(f"Found {gold_gained} gold on the body!")
                
                # Gain XP
                self.player.add_exp(enemy.exp)
                print(f"Gained {enemy.exp} XP!")
                
                # Update quest
                if enemy.name == "Weirdo":
                    self.player.quests["Weirdos"] += 1
                    print(f"\nWeirdos defeated: {self.player.quests['Weirdos']}/{self.quests['Weirdos']['target']}")
                
                return
            
            # Enemy attack
            enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 2)
            self.player.hp -= enemy_damage
            print(f"The {enemy.name} hits you for {enemy_damage} damage!")
            
            if self.player.hp <= 0:
                print("\n=== YOU ARE DEFEATED! ===")
                self.player.hp = 1
                self.player.location = "town_square"
                print("You wake up in the town square, badly wounded.")
                return
    
    def display_status(self):
        print(f"\n{self.player.name} - Level {self.player.level}")
        print(f"HP: {self.player.hp}/{self.player.max_hp}")
        print(f"EXP: {self.player.exp}/{self.player.exp_to_level}")
        print(f"Gold: {self.player.gold}")
    
    def check_quests(self):
        print("\n=== ACTIVE QUESTS ===")
        weirdo_quest = self.player.quests["Weirdos"]
        target = self.quests["Weirdos"]["target"]
        print(f"Defeat Weirdos: {weirdo_quest}/{target}")
        
        if weirdo_quest >= target:
            print("\n=== QUEST COMPLETE! ===")
            reward = self.quests["Weirdos"]["reward"]
            print(f"Reward: {reward} gold!")
            self.player.gold += reward
            self.player.quests["Weirdos"] = -1000  # Mark as completed
    
    def run(self):
        print("=== TEXT RPG v4: LEVELING & QUESTS ===")
        self.create_character()
        
        while True:
            self.display_location()
            self.display_status()
            
            command = input("\nCommand (move/attack/shop/inv/quests/quit): ").lower()
            
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
            elif command == "shop":
                self.shop()
            elif command == "inv":
                self.show_inventory()
                if self.player.inventory:
                    use = input("Use item? (y/n): ").lower()
                    if use == "y":
                        item_name = input("Enter item name: ")
                        self.use_item(item_name)
            elif command == "quests":
                self.check_quests()
            else:
                print("Invalid command!")

if __name__ == "__main__":
    game = Game()
    game.run()