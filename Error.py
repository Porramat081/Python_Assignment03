import Location

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