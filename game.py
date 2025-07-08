class Game:
    def __init__(self):
        self.location = "town_square"
        self.locations = {
            "town_square": {
                "name": "Cliche Town Square",
                "description": "Yup this is a town",
                "exits": {"north": "market", "east": "tavern"}
            },
            "market": {
                "name": "Marketplace",
                "description": "Isn't this quite bazaar?",
                "exits": {"south": "town_square"}
            },
            "tavern": {
                "name": "The Tavern",
                "description": "It's a cardboard box that says Tavern. People gather here for seemingly no reason.",
                "exits": {"west": "town_square"}
            }
        }
    
    def display_location(self):
        loc = self.locations[self.location]
        print(f"\n{loc['name']}\n{'-' * len(loc['name'])}")
        print(loc['description'])
        print("\nExits: " + ", ".join(loc['exits'].keys()))
    
    def move(self, direction):
        loc = self.locations[self.location]
        if direction in loc['exits']:
            self.location = loc['exits'][direction]
            print(f"\nYou go {direction}...")
            return True
        print("\nYou can't go that way!!!")
        return False
    
    def run(self):
        print("=== TEXT RPG v1: BASIC MOVEMENT ===")
        while True:
            self.display_location()
            command = input("\nCommand (north/south/east/west/quit): ").lower()
            if command == "quit":
                print("Goodbye...")
                break
            if command in ["north", "south", "east", "west"]:
                self.move(command)
            else:
                print("Invalid command!!!")

if __name__ == "__main__":
    game = Game()
    game.run()