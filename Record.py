import os.path as op
import csv

from Error import FileNotFound
from Location import Location
from Creature import Pymon , Creature

class Record:
    def __init__(self):
        self.file_location = "locations.csv"
        self.file_creatures = "creatures.csv"
        self.list_location = []
        self.list_creature = []

    # @property
    # def list_location(self):
    #     return self.list_location
    
    # @list_location.setter
    # def list_location(self,new_list):
    #     self.list_location = new_list

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

                loc_w = row[2].strip()
                loc_n = row[3].strip()
                loc_e = row[4].strip()
                loc_s = row[5].strip()

                current_loc = Location(loc_name,loc_des)
                
                if loc_w != "None":
                    location_w = Location(loc_w)
                    current_loc.connect_west(location_w)
                    self.update_list_location(location_w)
                if loc_n != "None":
                    location_n = Location(loc_n)
                    current_loc.connect_north(location_n)
                    self.update_list_location(location_n)
                if loc_e != "None":
                    location_e = Location(loc_e)
                    current_loc.connect_east(location_e)
                    self.update_list_location(location_e)
                if loc_s != "None":
                    location_s = Location(loc_s)
                    current_loc.connect_south(location_s)
                    self.update_list_location(location_s)
                    
                self.update_list_location(current_loc)
        
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

    def update_list_location(self,location:Location):
        is_exist = False
        selected_index = 0

        for index , loc in enumerate(self.list_location):
            if loc.get_name().lower() == location.get_name().lower():
                is_exist = True
                selected_index = index
        if not is_exist:
            self.list_location.append(location)
        else:
            self.list_location[selected_index] = location

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
        print(self.list_location)
        for i in self.list_location:
            i.display_full_info()
# class Record:
#     def __init__(self):
#         self.locations = []
#         #please implement constructor

#     def import_location(self):
#         #please import data from locations.csv
#         #here are sample data to start with
#         school = Location("school")
#         car_park = Location("car park")
#         self.locations.append(school)
#         self.locations.append(car_park)
        
#         school.connect_west(car_park)
        
#     def get_locations(self):
#         return self.locations
        
#     def import_creatures(self):
#         pass #please import data from creatures.csv

#     def import_items(self):
#         pass #please import data from items.csv