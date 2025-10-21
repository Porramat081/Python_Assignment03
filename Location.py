from Error import DirectionException
from Operation import Pymon

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

    def find_creature(self,creature_name="",find_pymon=False , is_random = False):
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
                    if isinstance(i,Pymon):
                        search_creature = i
                else: 
                    if i.get_name().lower() == creature_name.lower():
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