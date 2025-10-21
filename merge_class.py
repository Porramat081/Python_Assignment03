import time
import csv
import os.path as op
import random

class DirectionException(Exception):
    def __init__(self,direction):
        message = f'{direction} not in the direction list , please enter only "west" , "north" , "south" , "east"'
        super().__init__(message)

class NotFoundLocation(Exception):
    def __init__(self,location:Location,direction=""):
        message = ""
        if direction == "":
            message = f'{location.name} not found'
        else:
            message = f'{location.name} have no adjacent location in {direction} , please try another direction'
        super().__init__(message)

class FileNotFound(Exception):
    def __init__(self, file_name):
        message = f'{file_name} not found , please try again'
        super().__init__(message)

class InputInvalid(Exception):
    def __init__(self, input , option):
        result_string = ' '.join(map(str, option))
        message = f'{input} not in available options [{result_string}] , please try again'
        super().__init__(message)

class Location:
    def __init__(self, name = "New room", des="" ,w = None, n = None , e = None, s = None):
        self.name = name
        self.doors = {}
        self.doors["west"] = w
        self.doors["north"] = n
        self.doors["east"] = e
        self.doors["south"] = s
        self.des = des
        self.creatures = []
        self.items = []

    def get_doors(self):
        return self.doors

    def get_name(self):
        return self.name

    def get_des(self):
        return self.des

    def set_des(self,des):
        self.des = des
        
    def add_creature(self, creature):
        self.creatures.append(creature)
        #please implement this method to by simply appending a creature to self.creatures list.
        
    def add_item(self, item):
        self.items.append(item)
        #please implement this method to by simply appending an item to self.items list.

    def find_item(self,item_name):
        search_item = None
        for i in self.items:
            if i.get_name().lower() == item_name.lower():
                search_item = i
        return search_item

    def find_creature(self,self_name="",find_pymon=False , is_random = False):
        search_creature = None
        random_index = 0
        if is_random and len(self.creatures) > 0:
            random_index = Operation.generate_random_number(len(self.creatures)-1)
        for index , i in enumerate(self.creatures):
            if is_random:
                if index == random_index:
                    search_creature = i
            else:
                if find_pymon:
                    if isinstance(i,Pymon) and i.get_name().lower() != self_name.lower():
                        search_creature = i
        return search_creature

    def get_connect_location(self,direction):
        if not direction in ["west","north","south","east"]:
            raise DirectionException(direction)
        else:
            return self.doors[direction]

    def connect_east(self, another_room):
        self.doors["east"] = another_room 
        another_room.doors["west"]  = self
        
    def connect_west(self, another_room):
        self.doors["west"] = another_room 
        another_room.doors["east"]  = self
    
    def connect_north(self, another_room):
        self.doors["north"] = another_room 
        another_room.doors["south"]  = self
        
    def connect_south(self, another_room):
        self.doors["south"] = another_room 
        another_room.doors["north"]  = self

    def display_full_info(self):
        w = self.doors["west"].get_name() if self.doors["west"] else "Nope"
        n = self.doors["north"].get_name() if self.doors["north"] else "Nope"
        s = self.doors["south"].get_name() if self.doors["south"] else "Nope"
        e = self.doors["east"].get_name() if self.doors["east"] else "Nope"
        print(self.name , w,n,s,e)
        print(self.des)
        print(self.creatures)

class Creature:
    def __init__(self,name,location:Location=None,des=""):
        self.name = name
        self.current_location = location
        self.des = des

    def spawn(self, location:Location):
        if location != None:
            location.add_creature(self)
            self.current_location = location
        else:
            raise NotFoundLocation(location)
    
    def get_name(self):
        return self.name
    
    def get_des(self):
        return self.des
    
    def get_location(self):
        return self.current_location
    
    def display_info(self):
        print("")

    def display_taunt(self):
        if self.name.lower() == "sheep":
            print("the sheep just ignored you")
        elif self.name.lower() == "chicken":
            print("the chicken just laughed at you")

class Pymon(Creature):
    def __init__(self,name,location:Location=None,speed=0,energy=3,des=""):
        super().__init__(name,location,des)
        self.energy = energy
        if speed == 0:
            ran_speed = Operation.generate_random_number(max_number=20 , min_number=10)
            self.speed = ran_speed
        else:
            self.speed = speed
        self.item_list = []

    def add_item(self, item:Item):
        self.item_list.append(item)    

    def get_items(self,carry=False):
        if carry:
            return self.item_list[0]
        else:
            return self.item_list

    def move(self,direction):
        if not direction in ["west","north","south","east"]:
            raise DirectionException(direction)
        else:
            new_location = self.current_location.get_connect_location(direction)
            if not new_location:
                raise NotFoundLocation(new_location,direction)
            else:
                self.current_location = new_location
    
    def challenge_race(self,target_creature:Pymon):
        sec = 0
        distance_self = 100
        distance_enemy = 100
        leader = None

        pymon_player = self.get_name()
        pymon_enemy = target_creature.get_name()

        while not distance_self <= 0 and not distance_enemy <= 0:
            luck_player = Luck()
            sec_speed_player = luck_player.cal_sec_speed(self.speed)
            luck_enemy = Luck()
            sec_speed_enemy = luck_enemy.cal_sec_speed(target_creature.speed)
            distance_self -= sec_speed_player
            distance_enemy -= sec_speed_enemy
            message_at_sec = f"{pymon_player} (your Pymon) hopped {sec_speed_player:.2f} meters. Distance remaining for {distance_self:.2f}\n{pymon_enemy} (Opponent) hopped {sec_speed_enemy:.2f} meters. Distance remaining for {distance_enemy:.2f}\n"
            print(message_at_sec)
            if distance_self < distance_enemy:
                leader = self
            elif distance_self > distance_enemy:
                leader = target_creature
            else:
                leader = None
            sec += 1
            time.sleep(1)
        
        if leader.get_name().lower() == pymon_player.lower():
            print(f"{pymon_player} (your Pymon) reached the finish line in {sec} seconds! You win!")
            return True
        elif leader.get_name().lower() == target_creature.lower():
            print(f"{pymon_enemy} (Opponent) reached the finish line in {sec} seconds! You lose!")
            return False

    def display_info(self):
        print(f"Hi Player, my name is {self.name}, I am {self.des}.\nMy energy level is {self.energy}/3.What can I do to help you?\n")

class Item:
    def __init__(self,name,effect=None,des=""):
        self.name = name
        self.des = des
        self.effect = effect
    def get_name(self):
        return self.name

class InventoryItem(Item):
    def __init__(self, name, des=""):
        super().__init__(name, des)

class ConsumeItem(Item):
    def __init__(self, name, des=""):
        super().__init__(name, des)

class Luck:
    def __init__(self):
        ran_percentage = Operation.generate_random_number(max_number=50 , min_number=20 , is_float=True)
        ran_sign = Operation.generate_random_number(max_number=1)

        if ran_sign == 1:
            self.percentage = ran_percentage
        elif ran_sign == 0:
            self.percentage = ran_percentage * (-1)
    
    def cal_sec_speed(self, initial_speed):
        return float(initial_speed) + ((self.percentage/100 )* float(initial_speed))

class Record:
    def __init__(self):
        self.file_location = "locations.csv"
        self.file_creatures = "creatures.csv"
        self.list_location = []
        self.list_creature = []

    def import_location(self,file_name=""):
        if file_name != "":
            self.file_location = file_name
        if not op.exists(self.file_location):
            raise FileNotFound(self.file_location)
        with open(self.file_location,"r",encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                loc_name = row[0].strip()
                loc_des = row[1].strip()

                loc_w = row[2].strip() if row[2].strip() != "None" else None
                loc_n = row[3].strip() if row[3].strip() != "None" else None
                loc_e = row[4].strip() if row[4].strip() != "None" else None
                loc_s = row[5].strip() if row[5].strip() != "None" else None

                current_loc = Location(loc_name,loc_des,loc_w,loc_n,loc_e,loc_s)
                self.list_location.append(current_loc)
               
    def init_connection(self):
        for i in self.list_location:
            doors = i.get_doors()
            if doors["east"] and not isinstance(doors["east"], Location):
                loc_e = self.find_location(doors["east"])
                i.connect_east(loc_e)
            if doors["west"] and not isinstance(doors["west"], Location):
                loc_w = self.find_location(doors["west"])
                i.connect_west(loc_w)
            if doors["north"] and not isinstance(doors["north"], Location):
                loc_n = self.find_location(doors["north"])
                i.connect_north(loc_n)
            if doors["south"] and not isinstance(doors["south"], Location):
                loc_s = self.find_location(doors["south"])
                i.connect_south(loc_s)

    def import_creature(self,file_name=""):
        if file_name != "":
            self.file_creatures = file_name
        if not op.exists(self.file_creatures):
            raise FileNotFound(self.file_creatures)
        with open(self.file_creatures,"r",encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                c_name = row[0].strip()
                c_des = row[1].strip()
                c_adoptable = True if row[2].strip().lower() == "yes" else False
                c_speed = row[3].strip()

                current_creature = None
                if c_adoptable:
                    current_creature = Pymon(c_name,des=c_des,speed=c_speed)
                else:
                    current_creature = Creature(c_name,des=c_des)
                
                self.update_list_creature(current_creature)


    def update_list_creature(self,creature:Creature):
        self.list_creature.append(creature)

    def find_location(self,loc_name):
        search_loc = None
        for i in self.list_location:
            if i.get_name().lower() == loc_name.lower():
                search_loc = i
        return search_loc
    
    def find_creature(self,creature_name):
        search_creature = None
        for i in self.list_creature:
            if i.get_name().lower() == creature_name.lower():
                search_creature = i
        return search_creature

    def display_list_location(self):
        for i in self.list_location:
            i.display_full_info()

class Operation:

    #you may use, extend and modify the following random generator
    @staticmethod
    def generate_random_number(max_number = 1 , min_number = 0 , is_float = False):
        if is_float:
            r = random.uniform(min_number,max_number)
            return r
        elif not is_float and not max_number <= 0:
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
                print("8) List location")
                print("9) List creatures")

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
                    another_pymon = current_loc.find_creature(self.current_pymon.get_name(),find_pymon = True)
                    if not another_pymon:
                        random_creature = current_loc.find_creature(is_random=True)
                        if random_creature:
                            random_creature.display_taunt()
                        else:
                            print("Not Found any creature") 
                    else:
                        print("challenge start")
                        result = self.current_pymon.challenge_race(another_pymon)
                        print(result)

                elif input_option == "7":
                    print("Exit the game and save?")
                    break    
                elif input_option == "8":
                    self.record.display_list_location()
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
        self.record.import_creature()
        self.record.init_connection()
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

if __name__ == '__main__':
    operation = Operation()
    try:
        # for i in range(1, len(sys.argv)):
        #     if sys.argv[i] == '-o' and i + 1 < len(sys.argv):
        #         orders_file = sys.argv[i + 1]
        #     elif sys.argv[i] == '-g' and i + 1 < len(sys.argv):
        #         guests_file = sys.argv[i + 1]
        #     elif sys.argv[i] == '-p' and i + 1 < len(sys.argv):
        #         products_file = sys.argv[i + 1]
        #     elif not sys.argv[i] in ["-o","-g","-p"] and sys.argv[i].startswith("-"):
        #         print("This program have no ",sys.argv[i]," there's only -g for guest_file , -p for product_file , -o for order_file")

        operation.setup()
        operation.start_game()
    except Exception as e:
        print(e)
