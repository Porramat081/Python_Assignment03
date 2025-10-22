class Item:
    def __init__(self,name):
        self.name = name

item_1 = Item(name="one")
item_2 = Item(name="two")
item_3 = Item(name="three")

list_item = [item_1,item_2,item_3]

print(list_item)

def remove_item(removed_item):
    list_item.remove("jijol")

remove_item(item_2)

print(list_item)