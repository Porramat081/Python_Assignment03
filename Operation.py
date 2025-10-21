from Error import InputInvalid , DirectionException
import random

class Operation:

    #you may use, extend and modify the following random generator
    @staticmethod
    def generate_random_number(max_number = 1 , min_number = 0):
        if not max_number <= 0:
            r = random.randint(min_number,max_number)
            return r 
        return 0

    def handle_menu(self):
        while True:
            try:
                print("Please issue a command to your Pymon:")
                print("1) Inspect Pymon")
                print("2) Inspect current location")
                print("3) Move")
                print("4) Pick an item")
                print("5) View inventory")
                print("6) Challenge a creature")
                print("7) Exit the program")

                input_option = input("Enter your option : ").strip()
                if input_option == "1":
                    print("Your command: 1")
                    self.current_pymon.display_info()
                elif input_option == "2":
                    print("Your command: 2")
                    current_loc = self.current_pymon.get_location()
                    print(f"You are at a {current_loc.get_name()},{current_loc.get_des()}\n")
                elif input_option == "3":
                    print("Your command: 3")
                    input_direction = input("Moving to which direction?: ").strip()
                    if not input_direction in ["west","north","south","east"]:
                        raise DirectionException(input_direction)
                    self.current_pymon.move(input_direction)
                    current_loc = self.current_pymon.get_location()
                    print(f"You traveled {input_direction} and arrived at a {current_loc.get_name()}.")
                elif input_option == "4":
                    print("Your command: 4")
                    input_item = input("Picking what : ").strip()
                    current_loc = self.current_pymon.get_location()
                    picked_item = current_loc.find_item(input_item)
                    if not picked_item:
                        print("Not Found This Item In This Location") 
                    else:
                        self.current_pymon.add_item(picked_item)
                        print(f"You picked up an {picked_item.get_name()} from the ground")
                elif input_option == "5":
                    print("Your command: 5")
                    carry_item = self.current_pymon.get_items(carry=True)
                    print(f"You are carrying : {carry_item.get_name()}")
                elif input_option == "6":
                    print("Your command: 6")
                    current_loc = self.current_pymon.get_location()
                    another_pymon = current_loc.find_creature(find_pymon = True)
                    if not another_pymon:
                        random_creature = current_loc.find_creature(is_random=True)
                        random_creature.display_taunt()
                    else:
                        result = self.current_pymon.challenge_race(another_pymon)
                        print(result)

                elif input_option == "7":
                    print("Exit the game and save?")
                    break    
                else:
                    raise InputInvalid(input_option,[1,2,3,4])
            except Exception as e:
                print(e)
    
    def __init__(self):
        self.record = None
        self.pet_list = []
        self.current_pymon = None

    def setup(self,location_file="",creature_file=""):
        self.record = Record()
        self.record.import_location()
        locations = self.record.list_location

        # new game
        current_pymon = Pymon("Toromon",des="white and yellow Pymon with a square face")
        self.pet_list.append(current_pymon)
        self.current_pymon = self.pet_list[0]

        school_loc = self.record.find_location("school")
        playground_loc = self.record.find_location("playground")
        beach_loc = self.record.find_location("beach")

        kitimon = self.record.find_creature("kitimon")
        sheep = self.record.find_creature("sheep")
        marimon = self.record.find_creature("marimon")

        playground_loc.add_creature(kitimon)
        beach_loc.add_creature(sheep)
        school_loc.add_creature(marimon)

        apple = ConsumeItem("Apple")
        pogo_stick = InventoryItem("pogo stick")
        binocular = InventoryItem("binocular")
        tree = Item("tree")

        playground_loc.add_item(tree)
        playground_loc.add_item(pogo_stick)
        beach_loc.add_item(binocular)
        school_loc.add_item(apple)

        if len(locations)>0:
            a_random_number = Operation.generate_random_number(len(locations)-1)
            spawned_loc = locations[a_random_number]
            self.current_pymon.spawn(spawned_loc)
          
    def display_setup(self):
        for location in self.locations:
            print(location.name + " has the following creatures:")
            for creature in location.creatures:
                print(creature.name)

    #you may use this test run to help test methods during development
    def test_run(self):
        print(self.current_pymon.get_location().get_name())
        self.current_pymon.move("west")
        print(self.current_pymon.get_location().get_name())
        
    def start_game(self):
        print("Welcome to Pymon World\n")
        print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.\n")
        current_location = self.current_pymon.get_location()
        if current_location:
            print("You started at ",current_location.get_name())
        else:
            print("Your pymon is nowhere")
        self.handle_menu()

    