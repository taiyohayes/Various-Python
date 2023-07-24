from Arthropod import Arthropod
import random


class Insect(Arthropod):
    insect_count = 0

    def __init__(self, name_param, color_param, limbs_count_param, wings_count_param):
        super().__init__(name_param, color_param, limbs_count_param)
        self.wings_count = wings_count_param
        Insect.insect_count += 1

    def __str__(self):
        return "The " + self.color + " " + self.name + " has " + str(self.limbs_count) + " limbs and " + \
               str(self.wings_count) + " wings."

    def get_wings_count(self):
        return self.wings_count()

    def get_power(self):
        return self.limbs_count + self.wings_count

    def lose_fight(self):
        super().lose_fight()
        self.wings_count -= random.randrange(0, self.wings_count + 1)

