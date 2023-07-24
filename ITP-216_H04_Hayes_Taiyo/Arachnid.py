from Arthropod import Arthropod


class Arachnid(Arthropod):
    arachnid_count = 0

    def __init__(self, name_param, color_param, limbs_count_param, venomous_param):
        super().__init__(name_param, color_param, limbs_count_param)
        self.venomous = venomous_param
        Arachnid.arachnid_count += 1

    def __str__(self):
        venom = "non-venomous"
        if self.venomous:
            venom = "venomous"
        return "The " + self.color + " " + venom + " " + self.name + " has " + str(self.limbs_count) + " limbs."

    def get_venomous(self):
        return self.venomous

    def get_power(self):
        if self.venomous:
            return self.limbs_count * 2
        else:
            return self.limbs_count

