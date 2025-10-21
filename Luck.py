from Operation import Operation

class Luck:
    def __init__(self):
        ran_percentage = Operation.generate_random_number(max_number=0.5 , min_number=0.2)
        ran_sign = Operation.generate_random_number(max_number=1)
        if ran_sign == 1:
            self.percentage = ran_percentage
        elif ran_sign == 0:
            self.percentage = ran_percentage * -1
    
    def cal_sec_speed(self, initial_speed):
        return initial_speed + (self.percentage * initial_speed)
