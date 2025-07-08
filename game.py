import json
import os
import random
from enum import Enum

# --------------------------
# Enums for Game Elements
# --------------------------
class CharacterClass(Enum):
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ROGUE = "Rogue"

class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

# --------------------------
# Core Game Classes
# --------------------------
class Player:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.defense = 5
        self.gold = 50
        self.inventory = []
        self.location = "town_square"
        
        # Class-specific bonuses
        if char_class == CharacterClass.WARRIOR:
            self.attack += 5
            self.defense += 3
        elif char_class == CharacterClass.MAGE:
            self.max_hp -= 20
            self.hp = self.max_hp
            self.attack += 8
        elif char_class == CharacterClass.ROGUE:
            self.attack += 3
            self.defense += 2

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
        self.defense += 3
        
        print(f"\n=== LEVEL UP! You're now level {self.level} ===")
        print(f"HP: {self.max_hp}, ATK: {self.attack}, DEF: {self.defense}\n")
    
    def add_item(self, item):
        self.inventory.append(item)
        
    def use_item(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                if item.type == "consumable":
                    self.hp = min(self.max_hp, self.hp + item.value)
                    print(f"Used {item.name}! Restored {item.value} HP.")
                    self.inventory.remove(item)
                    return True
        return False
    
    def to_dict(self):
        return {
            "name": self.name,
            "char_class": self.char_class.value,
            "level": self.level,
            "exp": self.exp,
            "exp_to_level": self.exp_to_level,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "gold": self.gold,
            "inventory": [item.to_dict() for item in self.inventory],
            "location": self.location
        }
    
    @classmethod
    def from_dict(cls, data):
        player = cls(data["name"], CharacterClass(data["char_class"]))
        player.level = data["level"]
        player.exp = data["exp"]
        player.exp_to_level = data["exp_to_level"]
        player.hp = data["hp"]
        player.max_hp = data["max_hp"]
        player.attack = data["attack"]
        player.defense = data["defense"]
        player.gold = data["gold"]
        player.inventory = [Item.from_dict(item) for item in data["inventory"]]
        player.location = data["location"]
        return player

class Item:
    def __init__(self, name, item_type, value, price=0):
        self.name = name
        self.type = item_type
        self.value = value
        self.price = price
        
    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "value": self.value,
            "price": self.price
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["type"], data["value"], data.get("price", 0))

class Enemy:
    def __init__(self, name, level, hp, attack, defense, gold_drop, exp_drop):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.gold_drop = gold_drop
        self.exp_drop = exp_drop
        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage

class Location:
    def __init__(self, name, description, connections, enemies=None, shop_items=None, is_safe=False):
        self.name = name
        self.description = description
        self.connections = connections
        self.enemies = enemies or []
        self.shop_items = shop_items or []
        self.is_safe = is_safe

# --------------------------
# Game Logic
# --------------------------
class Game:
    SAVE_FILE = "game_save.json"
    
    def __init__(self):
        self.player = None
        self.locations = self.create_world()
        self.quests = {
            "defeat_goblins": {"completed": False, "target": 3, "current": 0, "reward": 100}
        }
    
    def create_world(self):
        return {
            "town_square": Location(
                "Town Square",
                "You're in the bustling town square. People are going about their business.",
                {"north": "market", "east": "tavern", "south": "forest_entrance"},
                is_safe=True
            ),
            "market": Location(
                "Marketplace",
                "Colorful stalls line the streets selling various goods.",
                {"south": "town_square", "east": "blacksmith"},
                shop_items=[
                    Item("Health Potion", "consumable", 20, 10),
                    Item("Sword", "weapon", 5, 50),
                    Item("Shield", "armor", 3, 40)
                ],
                is_safe=True
            ),
            "blacksmith": Location(
                "Blacksmith",
                "The clang of hammers fills the air. Weapons and armor line the walls.",
                {"west": "market"},
                shop_items=[
                    Item("Steel Sword", "weapon", 8, 100),
                    Item("Chainmail", "armor", 5, 150)
                ],
                is_safe=True
            ),
            "tavern": Location(
                "The Drunken Dragon Tavern",
                "A lively tavern filled with adventurers sharing tales.",
                {"west": "town_square"},
                is_safe=True
            ),
            "forest_entrance": Location(
                "Forest Entrance",
                "Thick trees mark the entrance to the Darkwood Forest.",
                {"north": "town_square", "south": "deep_forest"},
                enemies=[Enemy("Goblin", 1, 30, 8, 2, 15, 25)]
            ),
            "deep_forest": Location(
                "Deep Forest",
                "The forest grows darker and more foreboding.",
                {"north": "forest_entrance", "east": "spider_cave"},
                enemies=[
                    Enemy("Goblin", 1, 30, 8, 2, 15, 25),
                    Enemy("Wolf", 2, 40, 12, 3, 20, 35)
                ]
            ),
            "spider_cave": Location(
                "Spider Cave",
                "Sticky webs cover the walls of this damp cave.",
                {"west": "deep_forest"},
                enemies=[Enemy("Giant Spider", 3, 60, 15, 5, 30, 50)]
            )
        }
    
    def create_character(self):
        print("=== CHARACTER CREATION ===")
        name = input("Enter your name: ")
        
        print("\nChoose your class:")
        for i, char_class in enumerate(CharacterClass, 1):
            print(f"{i}. {char_class.value}")
        
        while True:
            try:
                choice = int(input("Select class (1-3): "))
                if 1 <= choice <= len(CharacterClass):
                    char_class = list(CharacterClass)[choice-1]
                    break
                print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")
        
        self.player = Player(name, char_class)
        print(f"\nWelcome, {self.player.name} the {self.player.char_class.value}!")
    
    def display_location(self):
        location = self.locations[self.player.location]
        print(f"\n{location.name}")
        print("=" * len(location.name))
        print(location.description)
        
        # Show connections
        print("\nExits:")
        for direction, loc_name in location.connections.items():
            print(f"- {direction.capitalize()}: {self.locations[loc_name].name}")
    
    def handle_movement(self):
        location = self.locations[self.player.location]
        valid_directions = [d.value for d in Direction]
        
        print("\nWhere would you like to go?")
        print("Available directions: " + ", ".join(location.connections.keys()))
        
        while True:
            direction = input("Direction (or 'cancel'): ").lower()
            if direction == "cancel":
                return
            
            if direction in location.connections:
                self.player.location = location.connections[direction]
                print(f"\nYou head {direction}...")
                self.random_encounter()
                return
            elif direction in valid_directions:
                print("You can't go that way from here.")
            else:
                print("Invalid direction. Use north/south/east/west.")
    
    def random_encounter(self):
        location = self.locations[self.player.location]
        if location.is_safe or not location.enemies:
            return
        
        # 40% chance of encounter
        if random.random() < 0.4:
            enemy = random.choice(location.enemies)
            print(f"\nA wild {enemy.name} appears!")
            self.combat(enemy)
    
    def combat(self, enemy):
        print(f"\n=== COMBAT: {self.player.name} vs {enemy.name} ===")
        
        while self.player.hp > 0 and enemy.hp > 0:
            # Player's turn
            print(f"\nYour HP: {self.player.hp}/{self.player.max_hp}")
            print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
            
            action = input("\nChoose action: [A]ttack, [U]se item, [R]un: ").lower()
            
            if action == "a":
                damage = max(1, self.player.attack - enemy.defense)
                enemy.hp -= damage
                print(f"You deal {damage} damage to {enemy.name}!")
            elif action == "u":
                self.display_inventory()
                item_name = input("Enter item name to use (or 'cancel'): ")
                if item_name.lower() != "cancel":
                    if not self.player.use_item(item_name):
                        print("Item not found or not usable!")
                        continue
            elif action == "r":
                if random.random() < 0.5:  # 50% chance to escape
                    print("You successfully escaped!")
                    return
                print("Escape failed!")
            else:
                print("Invalid action!")
                continue
            
            # Check if enemy defeated
            if enemy.hp <= 0:
                print(f"\nYou defeated the {enemy.name}!")
                gold_gained = enemy.gold_drop
                exp_gained = enemy.exp_drop
                
                self.player.gold += gold_gained
                self.player.add_exp(exp_gained)
                
                print(f"Gained {gold_gained} gold and {exp_gained} XP!")
                
                # Update quest progress
                if enemy.name == "Goblin" and not self.quests["defeat_goblins"]["completed"]:
                    self.quests["defeat_goblins"]["current"] += 1
                    if self.quests["defeat_goblins"]["current"] >= self.quests["defeat_goblins"]["target"]:
                        self.quests["defeat_goblins"]["completed"] = True
                        self.player.gold += self.quests["defeat_goblins"]["reward"]
                        print("\n=== QUEST COMPLETE: Defeat Goblins ===")
                        print(f"Received {self.quests['defeat_goblins']['reward']} gold reward!")
                return
            
            # Enemy's turn
            enemy_damage = max(1, enemy.attack - self.player.defense)
            self.player.hp -= enemy_damage
            print(f"The {enemy.name} hits you for {enemy_damage} damage!")
            
            # Check if player defeated
            if self.player.hp <= 0:
                print("\n=== YOU HAVE BEEN DEFEATED! ===")
                print("Game over...")
                self.player.hp = 1  # Reset to 1 HP to continue
                self.player.location = "town_square"
                print("You wake up in the town square, badly wounded.")
                return
    
    def display_status(self):
        player = self.player
        print("\n=== CHARACTER STATUS ===")
        print(f"Name: {player.name} ({player.char_class.value})")
        print(f"Level: {player.level} (XP: {player.exp}/{player.exp_to_level})")
        print(f"HP: {player.hp}/{player.max_hp}")
        print(f"Attack: {player.attack}, Defense: {player.defense}")
        print(f"Gold: {player.gold}")
    
    def display_inventory(self):
        if not self.player.inventory:
            print("\nYour inventory is empty.")
            return
        
        print("\n=== INVENTORY ===")
        for i, item in enumerate(self.player.inventory, 1):
            print(f"{i}. {item.name} ({item.type})", end="")
            if item.type == "consumable":
                print(f" - Heals {item.value} HP")
            elif item.type == "weapon":
                print(f" - ATK +{item.value}")
            elif item.type == "armor":
                print(f" - DEF +{item.value}")
    
    def shop(self):
        location = self.locations[self.player.location]
        if not location.shop_items:
            print("There's no shop here.")
            return
        
        print("\n=== SHOP ===")
        print("Items for sale:")
        for i, item in enumerate(location.shop_items, 1):
            print(f"{i}. {item.name} - {item.price} gold")
        
        print("\nYour gold:", self.player.gold)
        print("[B]uy, [S]ell, [L]eave")
        
        while True:
            choice = input("Select action: ").lower()
            
            if choice == "l":
                return
            elif choice == "b":
                try:
                    item_idx = int(input("Enter item number: ")) - 1
                    if 0 <= item_idx < len(location.shop_items):
                        item = location.shop_items[item_idx]
                        if self.player.gold >= item.price:
                            self.player.gold -= item.price
                            self.player.add_item(Item(item.name, item.type, item.value))
                            print(f"You bought a {item.name}!")
                        else:
                            print("Not enough gold!")
                    else:
                        print("Invalid item number.")
                except ValueError:
                    print("Please enter a number.")
            elif choice == "s":
                if not self.player.inventory:
                    print("Your inventory is empty.")
                    continue
                
                self.display_inventory()
                try:
                    item_idx = int(input("Enter item number to sell: ")) - 1
                    if 0 <= item_idx < len(self.player.inventory):
                        item = self.player.inventory[item_idx]
                        sell_price = max(1, item.price // 2) if item.price > 0 else 5
                        self.player.gold += sell_price
                        self.player.inventory.pop(item_idx)
                        print(f"You sold {item.name} for {sell_price} gold!")
                    else:
                        print("Invalid item number.")
                except ValueError:
                    print("Please enter a number.")
    
    def display_quests(self):
        print("\n=== ACTIVE QUESTS ===")
        for name, quest in self.quests.items():
            if not quest["completed"]:
                print(f"- Defeat Goblins: {quest['current']}/{quest['target']} (Reward: {quest['reward']} gold)")
    
    def save_game(self):
        data = {
            "player": self.player.to_dict(),
            "quests": self.quests
        }
        
        with open(self.SAVE_FILE, "w") as f:
            json.dump(data, f)
        
        print("Game saved successfully!")
    
    def load_game(self):
        try:
            with open(self.SAVE_FILE, "r") as f:
                data = json.load(f)
            
            self.player = Player.from_dict(data["player"])
            self.quests = data["quests"]
            print("Game loaded successfully!")
            return True
        except FileNotFoundError:
            print("No save file found.")
            return False
        except json.JSONDecodeError:
            print("Save file corrupted.")
            return False
    
    def main_menu(self):
        print("\n=== TEXT RPG ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Quit")
        
        while True:
            choice = input("Select: ")
            if choice == "1":
                self.create_character()
                return True
            elif choice == "2":
                if self.load_game():
                    return True
            elif choice == "3":
                return False
            else:
                print("Invalid choice.")
    
    def game_loop(self):
        while True:
            location = self.locations[self.player.location]
            
            # Check victory condition
            if self.quests["defeat_goblins"]["completed"] and self.player.level >= 5:
                print("\n=== VICTORY! ===")
                print("You've proven yourself a true hero!")
                print("Thanks for playing!")
                break
            
            self.display_location()
            self.display_status()
            
            print("\nWhat would you like to do?")
            print("[M]ove, [S]tatus, [I]nventory, [Q]uests, [S]hop, Sa[v]e, [Q]uit")
            
            if not location.is_safe:
                print("[E]xplore area")
            
            action = input("Action: ").lower()
            
            if action == "m":
                self.handle_movement()
            elif action == "s":
                self.display_status()
            elif action == "i":
                self.display_inventory()
                if self.player.inventory:
                    use_item = input("Use an item? (y/n): ").lower()
                    if use_item == "y":
                        item_name = input("Enter item name: ")
                        self.player.use_item(item_name)
            elif action == "q":
                self.display_quests()
            elif action == "v":
                self.save_game()
            elif action == "shop":
                self.shop()
            elif action == "e" and not location.is_safe:
                self.random_encounter()
            elif action == "quit":
                save = input("Save before quitting? (y/n): ").lower()
                if save == "y":
                    self.save_game()
                print("Goodbye!")
                break
            else:
                print("Invalid action.")

# --------------------------
# Main Execution
# --------------------------
if __name__ == "__main__":
    game = Game()
    
    if game.main_menu():
        game.game_loop()