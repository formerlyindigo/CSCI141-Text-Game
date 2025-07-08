import random

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.gold = 50
        self.inventory = []
        self.location = "town_square"
    
    def add_item(self, item):
        self.inventory.append(item)
        print(f"Added {item['name']} to inventory!")

class Item:
    def __init__(self, name, item_type, value, price=0):
        self.name = name
        self.type = item_type
        self.value = value
        self.price = price

class Game:
    def __init__(self):
        self.player = None
        self.locations = {
            "town_square": {
                "name": "Town Square",
                "description": "The town has four 90 degree angles with four sides that are equal with each other.",
                "exits": {"north": "market", "east": "forest_entrance"},
                "enemies": [],
                "shop": []
            },
            "market": {
                "name": "Marketplace",
                "description": "I'm not making another bazaar joke.",
                "exits": {"south": "town_square"},
                "enemies": [],
                "shop": [
                    Item("Health Potion", "consumable", 20, 10),
                    Item("Sword", "weapon", 5, 50)
                ]
            },
            "forest_entrance": {
                "name": "Forest Entrance",
                "description": "A sign with thick trees mark the forest. There is no forest. Just the sign. Actually there are many signs. ",
                "exits": {"west": "town_square"},
                "enemies": [Enemy("Weirdo", 30, 8)],
                "shop": []
            }
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
                print(f"Plundered {gold_gained} gold on the body! You sicko")
                return
            
            enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 2)
            self.player.hp -= enemy_damage
            print(f"The {enemy.name} hits you for {enemy_damage} damage!")
            
            if self.player.hp <= 0:
                print("\n=== YOU ARE DEFEATED! ===")
                self.player.hp = 1
                self.player.location = "town_square"
                print("You wake up in the town square, badly wounded probably. You can't tell cause you're text.")
                return
    
    def show_inventory(self):
        if not self.player.inventory:
            print("\nYour inventory is empty.")
            return
        
        print("\n=== INVENTORY ===")
        for item in self.player.inventory:
            print(f"- {item.name} ({item.type})")
    
    def use_item(self, item_name):
        for item in self.player.inventory[:]:
            if item.name.lower() == item_name:
                if item.type == "consumable":
                    self.player.hp = min(self.player.max_hp, self.player.hp + item.value)
                    self.player.inventory.remove(item)
                    print(f"Used {item.name}! Restored {item.value} HP.")
                    return True
        print("You tried using whatever that was. It doesn't exist.")
        return False
    
    def shop(self):
        loc = self.locations[self.player.location]
        if not loc['shop']:
            print("No shop here!")
            return
        
        print("\n=== SHOP ===")
        print("Items for sale:")
        for i, item in enumerate(loc['shop'], 1):
            print(f"{i}. {item.name} - {item.price} gold")
        
        print("\nYour gold:", self.player.gold)
        print("[B]uy, [S]ell, [L]eave")
        
        while True:
            action = input("Action: ").lower()
            if action == "l":
                return
            elif action == "b":
                try:
                    choice = int(input("Enter item number: ")) - 1
                    if 0 <= choice < len(loc['shop']):
                        item = loc['shop'][choice]
                        if self.player.gold >= item.price:
                            self.player.gold -= item.price
                            self.player.add_item(item)
                        else:
                            print("Not enough gold!")
                    else:
                        print("Invalid choice!")
                except ValueError:
                    print("Please enter a number.")
            elif action == "s":
                if not self.player.inventory:
                    print("Inventory empty!")
                    continue
                
                self.show_inventory()
                item_name = input("Enter item name to sell: ").lower()
                for item in self.player.inventory[:]:
                    if item.name.lower() == item_name:
                        sell_price = max(1, item.price // 2)
                        self.player.gold += sell_price
                        self.player.inventory.remove(item)
                        print(f"Sold {item.name} for {sell_price} gold!")
                        return
                print("Item not found!")
    
    def run(self):
        print("=== TEXT RPG v3: INVENTORY & SHOPS ===")
        self.create_character()
        
        while True:
            self.display_location()
            self.display_status()
            
            command = input("\nCommand (move/attack/shop/inv/quit): ").lower()
            
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
            else:
                print("Invalid command!")

if __name__ == "__main__":
    game = Game()
    game.run()