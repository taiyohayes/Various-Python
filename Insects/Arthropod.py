import random


class Arthropod(object):
    arthropod_count = 0

    def __init__(self, name_param, color_param, limbs_count_param):
        self.name = name_param
        self.limbs_count = limbs_count_param
        self.color = color_param
        Arthropod.arthropod_count += 1

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def get_limbs_count(self):
        return self.limbs_count

    def set_color(self, new_color):
        self.color = new_color

    def lose_fight(self):
        self.limbs_count -= random.randrange(0, self.limbs_count+1)