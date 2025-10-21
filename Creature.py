from Location import Location , Operation
from Error import DirectionException , NotFoundLocation
from Item import Item
from Luck import Luck
import time

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
            ran_speed = Operation.generate_random_number(6 , min_number=1)
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
            message_at_sec = f"{pymon_player} (your Pymon) hopped {sec_speed_player} meters. Distance remaining for {distance_self}\n\
                {pymon_enemy} (your Pymon) hopped {sec_speed_enemy} meters. Distance remaining for {distance_self}\n"
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

# class Pymon:
#     def __init__(self, name = "The player"):
#         self.name = name
#         self.current_location = None
    
#     def move(self, direction = None):
#         if self.current_location != None:
#             if self.current_location.doors[direction] != None:
#                 self.current_location.doors[direction].add_creature(self)  
#                 self.current_location.creatures.remove(self)
#             else:
#                 print("no access to " + direction)
                
#     def spawn(self, loc):
#         if loc != None:
#             loc.add_creature(self)
#             self.current_location = loc
            
#     def get_location(self):
#         return self.current_location