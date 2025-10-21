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