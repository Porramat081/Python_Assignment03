from Creature import Pymon
from Record import Record
from Error import InputInvalid , DirectionException
import random

class Operation:

    #you may use, extend and modify the following random generator
    @staticmethod
    def generate_random_number(max_number = 1):
        if not max_number <= 0:
            r = random.randint(0,max_number)
            return r 
        return 1

    
    def handle_menu(self):
        while True:
            try:
                print("Please issue a command to your Pymon:")
                print("1) Inspect Pymon")
                print("2) Inspect current location")
                print("3) Move")
                print("4) Exit the program")

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
                    print(f"You traveled {input_direction} and arrived at a {current_loc.get_name()}")
                elif input_option == "4":
                    print("Exit the game and save?")
                    break
                else:
                    raise InputInvalid(input_option,[1,2,3,4])
            except Exception as e:
                print(e)
    
    def __init__(self):
        self.record = None
        self.current_pymon = Pymon("Toromon",des="white and yellow Pymon with a square face")
      
    def setup(self,location_file="",creature_file=""):
        self.record = Record()
        self.record.import_location()
        locations = self.record.list_location

        school_loc = self.record.find_location("school")
        playground_loc = self.record.find_location("playground")
        beach_loc = self.record.find_location("beach")

        kitimon = self.record.find_creature("kitimon")
        sheep = self.record.find_creature("sheep")
        marimon = self.record.find_creature("marimon")

        playground_loc.add_creature(kitimon)
        beach_loc.add_creature(sheep)
        school_loc.add_creature(marimon)

        if not school_loc:
            a_random_number = Operation.generate_random_number(len(locations)-1)
            if len(locations)>0:
                spawned_loc = locations[a_random_number]
                self.current_pymon.spawn(spawned_loc)
        else:
            self.current_pymon.spawn(school_loc)
    
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

    