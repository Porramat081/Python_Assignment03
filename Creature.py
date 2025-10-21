import Location
from Error import DirectionException , NotFoundLocation

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


class Pymon(Creature):
    def __init__(self,name,location:Location=None,speed=0,energy=3,des=""):
        super().__init__(name,location,des)
        self.energy = energy
        self.speed = speed       

    def move(self,direction):
        if not direction in ["west","north","south","east"]:
            raise DirectionException(direction)
        else:
            new_location = self.current_location.get_connect_location(direction)
            if not new_location:
                raise NotFoundLocation(new_location,direction)
            else:
                self.current_location = new_location
    
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