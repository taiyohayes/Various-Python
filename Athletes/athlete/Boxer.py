from athlete.Athlete import Athlete


class Boxer(Athlete):
    boxer_count = 0

    def __init__(self, name_param, dob_param, origin_param, medals_param, weight_class_param):
        super().__init__(name_param, dob_param, origin_param, medals_param)
        self.weight_class = weight_class_param
        self.record = [0, 0]
        Boxer.boxer_count += 1

    def __str__(self):
        return self.name + " is a " + self.weight_class + " boxer from " + self.origin + " born on " + self.dob + ". " +\
               self.name + " has a " + str(self.record[0]) + "-" + str(self.record[1]) + " record, and has won " + \
               str(len(self.medals)) + " medals: " + str(self.medals) + "."

    def get_weight_class(self):
        return self.weight_class

    def get_record(self):
        return self.record

    def set_weight_class(self, weight_class_param):
        self.weight_class = weight_class_param

    def win_fight(self):
        self.record[0] += 1

    def lose_fight(self):
        self.record[1] += 1
        if self.record[1] == 10:
            return "This boxer has retired."
        else:
            return str(10 - self.record[1]) + " losses left before retirement."
