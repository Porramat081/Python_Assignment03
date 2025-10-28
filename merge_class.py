import time
import csv
import os
import os.path as op
import random
import sys
from datetime import datetime

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

class LocationCustomException(Exception):
    def __init__(self,option):
        message = ""
        if option=="format_len":
            message = f"Invalid format , please enter in format (location name , location description , location west connect , location north connect , location east connect , location south connect) , please try again"
        elif option == "data_type":
            message = f"Invalid data type , please enter only string data type"
        super().__init__(message)

class CreatureCustomException(Exception):
    def __init__(self, option):
        message = ""
        if option == "format_len":
            message = f'Invalid format , please enter in format (creature_name , creature_description , creature_adoptable(yes/no) , creature_speed(number)) , please try again'
        elif option == "speed_type":
            message = f'Speed datatype must be numeric data type'
        elif option == "invalid_string":
            message = f'Name , Description must be string'
        elif option == "invalid_adopt":
            message == f'Adoptable option , must be yes or no'
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

    def get_creature(self , des=False):
        if des:
            des_creature = ""
            is_have_pymon = False
            for i in self.creatures:
                if not isinstance(i,Pymon):
                    des_creature += f'a {i.get_name()}, '
                else:
                    is_have_pymon = True
            if is_have_pymon:
                des_creature += "another Pymon. "
            
            if des_creature != "":
                des_creature = f"This place has " + des_creature
            else:
                des_creature = "There's no other creature"
            return des_creature
        return self.creatures
    
    def get_items(self , des = False):
        if des:
            des_item = ""
            for i in self.items:
                des_item += f' {i.get_name()}, '
            if des_item != "":
                des_item = "This place has " + des_item
            else:
                des_item = "There's no item"
            return des_item
        return self.items

    def get_des(self):
        return self.des

    def set_des(self,des):
        self.des = des
        
    def add_creature(self, creature):
        self.creatures.append(creature)
        #please implement this method to by simply appending a creature to self.creatures list.
    
    def remove_creature(self,removed_creature):
        if removed_creature in self.creatures:
            self.creatures.remove(removed_creature)

    def add_item(self, item):
        self.items.append(item)
        #please implement this method to by simply appending an item to self.items list.

    def remove_item(self,item:Item):
        if item in self.items:
            self.items.remove(item)

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

    def re_connect(self):
        self.doors["east"] = None
        self.doors["west"] = None
        self.doors["north"] = None
        self.doors["south"] = None

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

    def display_info_one_location(self,location:Location , direction):
        if not location:
            print("This direction leads nowhere")
        else:
            init_string = location.get_creature(des=True)+location.get_items(des=True)
            if direction != "current":
                init_string = "In the " + direction+" , " + init_string
            else:
                w = self.doors["west"]
                n = self.doors["north"]
                s = self.doors["south"]
                e = self.doors["east"]
                if w:
                    init_string += " , In the west is a " + w.get_name()
                if n:
                    init_string += " , In the north is a " + n.get_name()
                if s:
                    init_string += " , In the south is a " + s.get_name()
                if e:
                    init_string += " , In the east is a " + e.get_name()
            print(init_string)

    def display_info_by_direction(self,direction):
        target_loc = self
        if direction != "current":
            target_loc = self.doors[direction]
        self.display_info_one_location(target_loc,direction)

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

    def spawn(self, location:Location , is_main=False):
        if location != None:
            if not is_main:
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
        else:
            print(f'{self.name} just pity you')

class Pymon(Creature):
    def __init__(self,name,location:Location=None,speed=0,energy=3,des=""):
        super().__init__(name,location,des)
        self.energy = energy
        if speed == 0:
            ran_speed = Operation.generate_random_number(max_number=6 , min_number=5)
            self.speed = ran_speed
        else:
            self.speed = speed
        self.item_list = []
        self.move_attempt = 0
        self.pogo_effect = False
    
    def get_pogo_effect(self):
        return self.pogo_effect

    def set_pogo_effect(self,new_effect:bool):
        self.pogo_effect = new_effect

    def get_energy(self):
        return self.energy
    
    def get_speed(self):
        return self.speed
    
    def set_energy(self,energy):
        self.energy = energy

    def use_move_attempt(self):
        self.move_attempt += 1
        if self.move_attempt == 2:
            self.drop_energy(1)
            print("You moved every 2 locations ,Pymons'energy is dropped 1 point")
            self.move_attempt = 0

    def add_energy(self,add_energy):
        if self.energy + add_energy > 3:
            self.energy = 3
        else:
            self.energy += add_energy
    
    def drop_energy(self,drop_energy):
        self.energy -= drop_energy
    
    def add_item(self, item:Item):
        self.item_list.append(item)
        self.current_location.remove_item(item)

    def drop_item(self,item:Item):
        self.item_list.remove(item)

    def get_items(self,carry=False):
        if carry:
            if len(self.item_list) > 0:
                return self.item_list[0]
            return None
        else:
            return self.item_list
        
    def use_item(self,item_index):
        selected_item = self.item_list[item_index]
        selected_item.activate_effect(self)
        
    def transfer_items(self,item_list):
        self.item_list += item_list

    def move(self,direction):
        direction = direction.lower()
        if not direction in ["west","north","south","east"]:
            raise DirectionException(direction)
        else:
            new_location = self.current_location.get_connect_location(direction)
            if not new_location:
                return False
            else:
                self.current_location = new_location
                return True

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
            if self.get_pogo_effect():
                print("Up speed by pogo stick effect")
                sec_speed_player *= 2
            luck_enemy = Luck()
            sec_speed_enemy = luck_enemy.cal_sec_speed(target_creature.speed)
            distance_self -= sec_speed_player
            distance_enemy -= sec_speed_enemy

            display_distance_self = 0 if distance_self <= 0 else distance_self
            display_distance_enemy = 0 if distance_enemy <= 0 else distance_enemy

            message_at_sec = f"{pymon_player} (your Pymon) hopped {sec_speed_player:.2f} meters. Distance remaining for {display_distance_self:.2f}\n{pymon_enemy} (Opponent) hopped {sec_speed_enemy:.2f} meters. Distance remaining for {display_distance_enemy:.2f}\n"
            print(message_at_sec)
            if display_distance_self < display_distance_enemy:
                leader = self
            elif display_distance_self > display_distance_enemy:
                leader = target_creature
            else:
                leader = None
            sec += 1
            time.sleep(1)

        if not leader:
            print(f"{pymon_player} (your Pymon) and {pymon_enemy} (Opponent) reached the finish line in {sec} seconds at the same time! You draw!")
            return "draw"
        else:
            if leader.get_name().lower() == pymon_player.lower():
                print(f"{pymon_player} (your Pymon) reached the finish line in {sec} seconds! You win!")
                return "win"
            elif leader.get_name().lower() == pymon_enemy.lower():
                print(f"{pymon_enemy} (Opponent) reached the finish line in {sec} seconds! You lose!")
                return "lose"

    def display_info(self):
        print(f"\nHi Player, my name is {self.name}, I am {self.des}.\nMy energy level is {self.energy}/3.What can I do to help you?\n")

class Item:
    def __init__(self,name,des=""):
        self.name = name
        self.des = des
    def get_name(self):
        return self.name

class InventoryItem(Item):
    def __init__(self, name, des=""):
        super().__init__(name, des)

    def activate_effect(self,current_pymon:Pymon):
        print("Activate Item Effect")

class Pogostick(InventoryItem):
    def __init__(self, name="pogo", des=""):
        super().__init__(name, des)
    
    def activate_effect(self,current_pymon:Pymon):
        current_pogo_effect = current_pymon.get_pogo_effect()
        if not current_pogo_effect:
            # activate pogo effect
            current_pymon.set_pogo_effect(True)
            print("Pogo effect activate , now your speed is double")
        else:
            print("You're already using Pogo effect right now , it'll disappear after race")
        
    def distroy_after_match(self,current_pymon:Pymon):
        current_pymon.set_pogo_effect(False)
        current_pymon.drop_item(self)
        print("Pogo stick is broken and disappear")

class Binocular(InventoryItem):
    def __init__(self, name="binocular" ,des=""):
        super().__init__(name, des)
    
    def activate_effect(self,current_pymon:Pymon):
        while True:
            try:
                current_loc = current_pymon.get_location()
                input_direction = input("Enter direction that you want to check (press n to cancel) : ").strip()
                input_direction = input_direction.lower()
                if input_direction == "n":
                    break
                elif not input_direction in ["current","west","north","east","south"]:
                    raise DirectionException(input_direction)
                else:
                    current_loc.display_info_by_direction(input_direction.lower())
            except Exception as e:
                print(e)
        
class ConsumeItem(Item):
    def __init__(self, name, des="" , gain_power = 1):
        super().__init__(name, des)
        self.gain_power = gain_power

    def get_gain_power(self):
        return self.gain_power
    
    def activate_effect(self,current_pymon:Pymon):
        if current_pymon.get_energy() < 3:
            current_pymon.add_energy(self.get_gain_power())
            current_pymon.drop_item(self)
            print(f"\n{current_pymon.get_name()}s'energy gains {self.get_gain_power()} point , now energy = {current_pymon.get_energy()}/3\n")
        else:
            print(f'\nYour Pymon has max energy , don\'t need to eat\n')

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

class RaceStat:
    def __init__(self,pymon_name,result,opponent_name):
        self.pymon_name = pymon_name
        self.result = result
        self.time_stamp = datetime.now()
        self.opponent_name = opponent_name

    def get_pymon_name(self):
        return self.pymon_name
    
    def get_tuple_format(self):
        return (self.result,self.time_stamp,self.opponent_name)
    
    @staticmethod
    def get_format_dict(race_stat_list):
        pymon_dict = {}
        for race in race_stat_list:
            pymon_name = race.get_pymon_name()
            race_tuple = race.get_tuple_format()
            if not pymon_name in pymon_dict:
                pymon_dict[pymon_name] = [race_tuple]
            else:
                pymon_dict[pymon_name].append(race_tuple)
        return pymon_dict
    
class SaveFile:
    def __init__(self,file_name):
        pass

    @staticmethod
    def search_save():
        save_list = []
        for i in os.listdir():
            if i.lower().startswith("gamesave") and i.lower().endswith(".csv"):
                save_list.append(i)
        return save_list
    
    @staticmethod
    def load_save_data(save_path):
        print(save_path)
    
        current_pymon = None
        list_pet = []
        list_other = []

        with open(save_path , "r" , encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
        
            for row in reader:
            
                pymon_name = row[0].strip()
                pymon_loc_name = row[1].strip()
                pymon_type = row[2].strip()
                pymon_energy = row[3].strip()
                pymon_inventory_arr  = row[4].split(",")

                if pymon_energy and int(pymon_energy) > 0:

                    current_pymon = (pymon_name,pymon_loc_name,pymon_type,pymon_energy,pymon_inventory_arr)
                    list_pet.append(current_pymon)
                else:
                    other_creature = (pymon_name,pymon_loc_name,pymon_type)
                    list_other.append(other_creature)
          
            
        return list_pet , list_other
                
    @staticmethod
    def gen_save_pet_data(current_pet , other_list):
        current_item = ""
        current_location = current_pet.get_location().get_name()
        for index , item in enumerate(current_pet.get_items()):
            current_item += item.get_name()
            if index != (len(current_pet.get_items())-1):
                current_item += ","
        data = [["name" , "location" , "type","energy" , "inventory"] , [current_pet.get_name() , current_location ,"pymon", current_pet.get_energy() , current_item]]
   
        for other in other_list:
           
            if other.get_name() == current_pet.get_name():
                continue
            other_item = ""
       
            if len(other.get_items()) > 0:
                for index , item in enumerate(other.get_items()):
                    other_item += item.get_name()
                    if index != (len(current_pet.get_items())-1):
                        other_item += ","

            new_data = [other.get_name() , current_location , "pymon",other.get_energy() , other_item]
        
            data.append(new_data)
        
        return data
        
    @staticmethod
    def gen_save_other_data(list_other_creature , own_list):
        data = []
        for i in list_other_creature:
            if i in own_list:
                continue
            i_type = "creature"
            if isinstance(i,Pymon):
                i_type = "pymon"
            new_data = [i.get_name(),i.get_location().get_name(),i_type,0,""]
            data.append(new_data)
        return data

class Record:
    def __init__(self):
        self.file_location = "locations.csv"
        self.file_creatures = "creatures.csv"
        self.file_items = "items.csv"
        self.list_location = []
        self.list_creature = []
        self.list_item = []
        self.list_stat = []

    def gen_stats(self):
        if len(self.list_stat) == 0:
            raise Exception("No race stat")
        list_format = RaceStat.get_format_dict(self.list_stat)
        display_string = ""
        for race_stat in list(list_format.items()):
            display_string += f'Pymon Nickname : "{race_stat[0]}"\n'
            win_count = 0
            lose_count = 0
            draw_count = 0
            for index , item in enumerate(race_stat[1]):
                time_format = item[1].strftime("%d/%m/%Y %H:%M %p")
                display_string += f'Race {index + 1} , {time_format} , Opponent : "{item[2]}" , {item[0]}\n'
                if item[0] == "win":
                    win_count += 1
                elif item[0] == "lose":
                    lose_count += 1
                elif item[0] == "draw":
                    draw_count += 1
            display_string += f'Total: W: {win_count} L: {lose_count} D: {draw_count}\n'
        return display_string

    def record_race_stat(self,pymon_name,result,another_name):
        new_record = RaceStat(pymon_name,result,another_name)
        self.list_stat.append(new_record)

    def get_list(self,key=""):
        if key == "location":
            return self.list_location
        elif key == "creature":
            return self.list_creature
        elif key == "item":
            return self.list_item

    def check_available_pymon(self):
        for loc in self.list_location:
            if len(loc.get_creature()) > 0:
                for creature in loc.get_creature():
                    if isinstance(creature,Pymon):
                        return True
        return False

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
               
    def init_connection(self , randomized=False):

        for i in self.list_location:
            doors = i.get_doors()
            if randomized:
                vals = list(doors.values())
                random.shuffle(vals)
                doors = dict(zip(doors.keys(), vals))
                i.re_connect()
                if doors["east"]:
                    i.connect_east(doors["east"])
                if doors["west"]:
                    i.connect_west(doors["west"])
                if doors["north"]:
                    i.connect_north(doors["north"])
                if doors["south"]:
                    i.connect_south(doors["south"])
            else:
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

    def get_ran_location(self):
        ran_in = Operation.generate_random_number(min_number=0,max_number=len(self.list_location)-1)
        return self.list_location[ran_in]

    def create_custom_location(self , loc_name , loc_des , doors):
        new_loc = Location(loc_name,loc_des, doors["west"] , doors["north"],doors["east"],doors["south"])
        self.list_location.append(new_loc)
        self.init_connection()
        data = [["name","description","west","north","east","south"]]
        for i in self.list_location:
            new_door = i.get_doors()
            w_door = new_door["west"].get_name() if new_door["west"] else "None"
            e_door = new_door["east"].get_name() if new_door["east"] else "None"
            n_door = new_door["north"].get_name() if new_door["north"] else "None"
            s_door = new_door["south"].get_name() if new_door["south"] else "None"
            new_data = [i.get_name() , i.get_des() , w_door , n_door , e_door,s_door]
            data.append(new_data)
        with open(self.file_location , "w" , encoding="utf-8" , newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)

    def create_custom_creature(self,c_name,c_des,c_abopt,c_speed=0):
        new_c = None
        if c_abopt == "yes":
            new_c = Pymon(name=c_name,des=c_des,speed=c_speed)
        else:
            new_c = Creature(name=c_name,des=c_des)
        ran_lo = self.get_ran_location()
        new_c.spawn(ran_lo)
        self.list_creature.append(new_c)
        data = [["name" , "description" , "adoptable" , "speed"]]
        for i in self.list_creature:
            is_adopt = "no"
            new_speed = 0
            if isinstance(i,Pymon):
                is_adopt = "yes"
                new_speed = i.get_speed()
            new_data = [i.get_name() , i.get_des() , is_adopt , new_speed]
            data.append(new_data)
        with open(self.file_creatures , "w" , encoding="utf-8" ,newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)

    def import_creature(self,file_name=""):
        if file_name != "":
            self.file_creatures = file_name
        if not op.exists(self.file_creatures):
            raise FileNotFound(self.file_creatures)
        with open(self.file_creatures,"r",encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
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
    
    def import_item(self,file_name=""):
        if file_name != "":
            self.file_items = file_name
        if not op.exists(self.file_items):
            raise FileNotFound(self.file_items)
        with open(self.file_items,"r",encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                current_item = None
                i_name = row[0].lower().strip()
                i_des = row[1].lower().strip()
                i_pick = row[2].lower().strip()
                i_con = row[3].lower().strip()
                if i_pick == "yes":
                    if i_con == "yes":
                        current_item = ConsumeItem(name=i_name , des=i_des)
                    elif i_con == "no":
                        if i_name == "pogo":
                            current_item = Pogostick(name=i_name,des=i_des)
                        elif i_name == "binocular":
                            current_item = Binocular(name=i_name,des=i_des)
                        else:
                            current_item = InventoryItem(name=i_name , des=i_des)
                elif i_pick == "no":
                    current_item = Item(name=i_name,des=i_des)
                
                self.update_list_item(current_item)
                
    def update_list_item(self,item:Item , is_remove=False):
        if not is_remove:
            self.list_item.append(item)
        else:
            pass

    def update_list_creature(self,creature:Creature , is_remove=False):
        if not is_remove:
            self.list_creature.append(creature)
        else:
            target_creature = self.find_creature(creature_name=creature.get_name())
            self.list_creature.remove(target_creature)

    def find_location(self,loc_name):
        search_loc = None
        for i in self.list_location:
            if i.get_name().lower() == loc_name.lower():
                search_loc = i
        return search_loc
    
    def find_creature(self,creature_name , on_load = False):
        search_creature = None
        for i in self.list_creature:
            if i.get_name().lower() == creature_name.lower():
                search_creature = i
        if not search_creature and on_load and creature_name.lower() == "toromon":
            search_creature = Pymon("Toromon",des="white and yellow Pymon with a square face")
            self.list_creature.append(search_creature)
        return search_creature
    
    def find_item(self,item_name):
        search_item = None
        for i in self.list_item:
            if i.get_name().lower() == item_name.lower():
                search_item = i
        return search_item

    def display_list_location(self):
        for i in self.list_location:
            i.display_full_info()

class Operation:

    @staticmethod
    def generate_random_number(max_number = 1 , min_number = 0 , is_float = False):
        if is_float:
            r = random.uniform(min_number,max_number)
            return r
        elif not is_float and not max_number <= 0:
            r = random.randint(min_number,max_number)
            return r 
        return 0
    
    def release_to_wild(self):
        # remove released pymon from pat_list
        if self.current_pymon in self.pet_list:
            print(f"{self.current_pymon.get_name()} ran out of energy , Released to the wild")
            self.pet_list.remove(self.current_pymon)
        
        if len(self.pet_list) == 0:
            self.is_over = True

        current_loc = self.current_pymon.get_location()
        old_current_pymon = Pymon(name=self.current_pymon.get_name(),des=self.current_pymon.get_des())
        
        # spawn random
        ran_loc_index = Operation.generate_random_number(max_number=(len(self.record.list_location)-1))
        old_current_pymon.spawn(self.record.list_location[ran_loc_index])

        # transfer item
        old_item_list = self.current_pymon.get_items()
        
        if len(self.pet_list) > 0:
            self.current_pymon = self.pet_list[0]
            self.current_pymon.spawn(current_loc,is_main=True)
            self.current_pymon.transfer_items(old_item_list)

    def handle_menu(self):
        while not self.is_over:
            try:
                print("Please issue a command to your Pymon:")
                print("1) Inspect Pymon")
                print("2) Inspect current location")
                print("3) Move")
                print("4) Pick an item")
                print("5) View inventory")
                print("6) Challenge a creature")
                print("7) Generate stats")
                print("8) Admin feature")
                print("9) Exit the program")

                input_option = input("Enter your option : ").strip()
                if input_option == "1":
                    print("Your command: 1")
                    while True:
                        try:
                            print("1) Inspect Current Pymon")
                            print("2) List and select a benched Pymon to use")
                            input_option = input("Enter your option : ").strip()
                            if input_option == "1":
                                self.current_pymon.display_info()
                                break
                            elif input_option == "2":
                                if len(self.pet_list) <= 1:
                                    for i in self.pet_list:
                                        print(i.get_name())
                                    print("\nYou only have one Pymon , cannot change pymon yet\n")
                                    break
                                else:
                                    print("List Your Pymon")
                                    for index,pet in enumerate(self.pet_list):
                                        print(f'{index+1}) {pet.get_name()}')
                                    pet_option = input("Enter pet number for current Pymon changing (press n to cancel) : ").strip()
                                    if pet_option.lower() == "n":
                                        print("\nCancel changing Pymon\n")
                                        break
                                    elif not int(pet_option) in range(1,len(self.pet_list)+1):
                                        raise InputInvalid(pet_option,range(1,len(self.pet_list)+1))
                                    else:
                                        actual_index = int(pet_option) - 1 
                                        current_loc = self.current_pymon.get_location()
                                        self.current_pymon = self.pet_list[actual_index]
                                        self.current_pymon.spawn(current_loc,is_main=True)
                                        break
                            else:
                                raise InputInvalid(input_option,["1","2"])
                        except ValueError:
                            print("Please enter only positive integer number")
                        except Exception as e:
                            print(e)
                elif input_option == "2":
                    print("Your command: 2")  
                    current_loc = self.current_pymon.get_location()
                    print(f"\nYou are at a {current_loc.get_name()},{current_loc.get_des()}\n")   
                elif input_option == "3":
                    print("Your command: 3")
                    while True:
                        try:
                            input_direction = input("Moving to which direction?: ").strip()
                            result_move = self.current_pymon.move(input_direction)
                            if not result_move:
                                current_loc = self.current_pymon.get_location()
                                print(f'{input_direction} of {current_loc.get_name()} is a dead end , Your Pymon is still at {current_loc.get_name()}')
                            else:
                                self.current_pymon.use_move_attempt()
                                current_loc = self.current_pymon.get_location()
                                print(f"You traveled {input_direction} and arrived at a {current_loc.get_name()}.")
                            break
                        except Exception as e:
                            print(e)
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
                    item_list = self.current_pymon.get_items()
                    if len(item_list) == 0:
                        print(f"\nYour Pymon don't have any item\n")
                    else:
                        print("Select Item to Use")
                        while True:
                            try:
                                for index , item in enumerate(item_list):
                                    print(f'{index+1}) {item.get_name()}')
                                input_option = input("Enter item number (press n to cancel) : ").strip()
                                if input_option.lower() == "n":
                                    break
                                elif not int(input_option) in range(1,len(item_list)+1):
                                    raise InputInvalid(input_option,range(1,len(item_list)+1))
                                else:
                                    actual_index = int(input_option) - 1
                                    print(f"\nYou are using : {item_list[actual_index].get_name()}\n")
                                    self.current_pymon.use_item(actual_index)
                                    break
                            except ValueError:
                                print("please enter positive integer number")
                            except Exception as e:
                                print(e)
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
                        if result == "draw":
                            print(f'{self.current_pymon.get_name()} drew with {another_pymon.get_name()} , Nothing happen')
                        elif result == "win": # pytmon player win
                            c_loc = another_pymon.get_location()
                            c_loc.remove_creature(another_pymon)
                            self.pet_list.append(another_pymon)
                            print(f"You caught {another_pymon.get_name()}.It's now in your pet list.")
                        else:
                            self.current_pymon.drop_energy(1)
                            print("Your Pymons'energy is decreased by 1 point.")

                        self.record.record_race_stat(self.current_pymon.get_name(),result,another_pymon.get_name())
                        
                        if not self.record.check_available_pymon():
                            print(f"You caught all pymon in this game , well done")
                            self.is_over = True
                            
                        if self.current_pymon.get_pogo_effect():
                            for i in self.current_pymon.get_items():
                                if isinstance(i,Pogostick):
                                    i.distroy_after_match(self.current_pymon)

                elif input_option == "7":
                    print("Generate Stats")
                    stat = self.record.gen_stats()
                    with open("race_stats.txt", "a", encoding="utf-8") as f:
                        f.write(stat)
                    print(stat)  

                elif input_option == "8":
                    print("Admin Feature")
                    while True:
                        try:
                            print("1) Add Custom Location")
                            print("2) Add Custom Creature")
                            print("3) Randomize Location Connection")
                            admin_option = input("Enter admin option (press n to cancel) : ").strip()
                            if admin_option == "1":
                                print("Add Custom Location")
                                while True:
                                    try:
                                        location_input = input("Enter location detail in format (location name , location description , location west connect , location north connect , location east connect , location south connect)\n").strip()
                                        location_input_split = location_input.split(",")
                                        if len(location_input_split) != 6:
                                            raise LocationCustomException(option="format_len")
                                        loc_name = location_input_split[0].strip()
                                        loc_des = location_input_split[1].strip()
                                        loc_west = location_input_split[2].strip()
                                        loc_north = location_input_split[3].strip()
                                        loc_east = location_input_split[4].strip()
                                        loc_south = location_input_split[5].strip()

                                        if loc_name.isnumeric() or loc_des.isnumeric() or loc_east.isnumeric() or loc_north.isnumeric() or loc_west.isnumeric() or loc_south.isnumeric():
                                            raise LocationCustomException(option="data_type")
                                        loc_west = location_input_split[2].strip() if location_input_split[2].lower().strip() != "none" else None
                                        loc_north = location_input_split[3].strip() if location_input_split[3].lower().strip() != "none" else None
                                        loc_east = location_input_split[4].strip() if location_input_split[4].lower().strip() != "none" else None
                                        loc_south = location_input_split[5].strip() if location_input_split[5].lower().strip() != "none" else None
                                        doors = {"east" : loc_east , "west":loc_west , "north":loc_north , "south" : loc_south}
                                        self.record.create_custom_location(loc_name=loc_name , loc_des=loc_des , doors=doors)
                                       
                                        print("create new location successfully")
                                        break
                                    except Exception as e:
                                        print(e)
                            elif admin_option == "2":
                                print("Add Custom Creature")
                                while True:
                                    try:
                                        creature_input = input("Enter creature detail in format (creature_name , creature_description , creature_adoptable(yes/no) , creature_speed)\n").strip()
                                        creature_input_split = creature_input.split(",")
                                        if len(creature_input_split) != 4:
                                            raise CreatureCustomException(option="format_len")
                                        c_name = creature_input_split[0].strip()
                                        c_des = creature_input_split[1].strip()
                                        c_adopt = creature_input_split[2].lower().strip()
                                        c_speed = creature_input_split[3].strip()

                                        if c_name.isnumeric() or c_des.isnumeric():
                                            raise CreatureCustomException(option="invalid_string")
                                        elif not c_speed.isnumeric():
                                            raise CreatureCustomException(option="speed_type")
                                        elif not c_adopt.lower() in ["yes" , "no"]:
                                            raise CreatureCustomException(option="invalid_adopt")
                                        
                                        self.record.create_custom_creature(c_name=c_name , c_des=c_des , c_abopt=c_adopt.lower() , c_speed=int(c_speed))
                                        print("Create new creature successfully")
                                        break
                                    except ValueError:
                                        print("Speed must be integer")
                                    except Exception as e:
                                        print(e)
                            elif admin_option == "3":
                                print("Randomize Location Connection")
                                self.record.init_connection(randomized = True)
                                print("Random Location Successfully")
                            elif admin_option.lower() == "n":
                                break
                            else:
                                raise InputInvalid(admin_option,["1","2","n"])
                        except Exception as e:
                            print(e)
                    
                elif input_option == "9":
                    print("Exit the game and save?")
                    save_option = input("Do you want to save game?(y:n) ").strip()
                    if not save_option.lower() in ["y","n"]:
                        raise InputInvalid(save_option,["y","n"])
                    else:
                        if save_option.lower() == "y":
                            print("Create New Save")
                            this_year = datetime.now().year
                            path_name = "gameSave"+str(this_year)+".csv"

                            with open(path_name,"w", newline='') as csv_pet_pymon:
                                data1 = SaveFile.gen_save_pet_data(self.current_pymon,self.pet_list)
                                own_list = self.pet_list
                                data2 = SaveFile.gen_save_other_data(self.record.get_list(key="creature") , own_list)
                                csv_writer = csv.writer(csv_pet_pymon)
                                csv_writer.writerows(data1+data2)
                        break    
                elif input_option == "10":
                    self.record.display_list_location()
                else:
                    raise InputInvalid(input_option,[1,2,3,4,5,6,7,8,9])
                
                if self.current_pymon.get_energy() == 0:
                    self.release_to_wild()
            except Exception as e:
                print(e)
    
    def __init__(self):
        self.record = None
        self.pet_list = []
        self.current_pymon = None
        self.is_over = False

    def setup(self,location_file="",creature_file="",item_file=""):
        self.record = Record()
        self.record.import_location(file_name=location_file)
        self.record.import_creature(file_name=creature_file)
        self.record.import_item(file_name=item_file)
        self.record.init_connection()
        locations = self.record.get_list(key="location")
        creatures = self.record.get_list(key="creature")
        items = self.record.get_list(key="item")

        save_file = SaveFile.search_save()
        is_load = True

        list_pet_load = []
        list_other_load = []

        if len(save_file) > 0:
            load_option = input("You have save file , Do you want to load game from save? (y/n) : ").strip()
            if not load_option.lower() in ["y",'n']:
                raise InputInvalid(load_option , ["y","n"])
            else:
                if load_option.lower() == "y":
                    list_load = SaveFile.load_save_data(save_file[0])
                    list_other_load = list_load[1]
                    list_pet_load = list_load[0]
                    for i in list_pet_load:
                        search_pet = self.record.find_creature(i[0].strip())
                        search_loc = self.record.find_location(i[1].strip())
                        if (not search_loc or not search_pet) and (i[0].lower().strip() != 'toromon'):
                            is_load = False
                    for j in list_other_load:
                        search_pet = self.record.find_creature(j[0].strip())
                        search_loc = self.record.find_location(j[1].strip())
                        if (not search_loc or not search_pet) and (j[0].lower().strip() != 'toromon'):
                            is_load = False
                    if not is_load:
                         print("Incomplete Loading , because loading data and csv file mismatch")
                elif load_option.lower() == "n":
                    is_load = False
        else:
            is_load = False

        if is_load:
            current_loc = self.record.find_location(list_pet_load[0][1].strip())
            for i in list_pet_load:
                search_pet = self.record.find_creature(i[0].strip(),on_load=True)
                search_pet.set_energy(int(i[3]))
                for item in i[4]:
                    search_item = self.record.find_item(item.strip())
                    if search_item:
                        search_pet.add_item(search_item)
                self.pet_list.append(search_pet)
            self.current_pymon = self.pet_list[0]
            self.current_pymon.spawn(current_loc,is_main=True)
            for j in list_other_load:
                search_creature = self.record.find_creature(j[0].strip(),on_load=True)
                search_loc_creature = self.record.find_location(j[1].strip())
                search_creature.spawn(search_loc_creature)
                
        else:
            # new game - init pymon 
            current_pymon = Pymon("Toromon",des="white and yellow Pymon with a square face")
            self.pet_list.append(current_pymon)
            self.current_pymon = self.pet_list[0]
            # add Toromon to list in case new game
            self.record.update_list_creature(current_pymon)

            if len(locations)>0:
                a_random_number = Operation.generate_random_number(len(locations)-1)
                spawned_loc = locations[a_random_number]
                self.current_pymon.spawn(spawned_loc,is_main=True)

                # random spawn creature
                for creature in creatures:
                    if creature.get_name() == current_pymon.get_name():
                        continue
                    ran_index = Operation.generate_random_number(min_number=0,max_number=(len(locations)-1))
                    creature.spawn(locations[ran_index])

        # random add item
        for item in items:
            ran_index = Operation.generate_random_number(min_number=0,max_number=(len(locations)-1))
            locations[ran_index].add_item(item)
          
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
        if self.is_over:
            if not self.record.check_available_pymon():
                print("Game Clear")
            else:
                print("Game Over")

if __name__ == '__main__':
    operation = Operation()
    try:
        location_file = ""
        creature_file = ""
        item_file = ""
        
        if len(sys.argv) > 4:
            raise Exception("Argument out of range , please enter in this format (location.csv creature.csv item.csv)")

        for i in range(1,len(sys.argv)):
            if i == 1:
                location_file = sys.argv[1]
            elif i == 2:
                creature_file = sys.argv[2]
            elif i == 3:
                item_file = sys.argv[3]

        operation.setup(location_file=location_file,creature_file=creature_file,item_file=item_file)
        operation.start_game()
    except Exception as e:
        print(e)
