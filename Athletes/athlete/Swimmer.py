from athlete.Athlete import Athlete


class Swimmer(Athlete):
    swimmer_count = 0

    def __init__(self, name_param, dob_param, origin_param, medals_param, strokes_param):
        super().__init__(name_param, dob_param, origin_param, medals_param)
        self.strokes = strokes_param
        Swimmer.swimmer_count += 1

    def __str__(self):
        return self.name + " is a swimmer from " + self.origin + " born on " + self.dob + ". " + self.name + " knows " \
        + str(self.strokes) + ", and has won " + str(len(self.medals)) + " medals: " + str(self.medals) + "."

    def get_strokes(self):
        return self.strokes

    def add_stroke(self, new_stroke):
        if new_stroke not in self.strokes:
            self.strokes.append(new_stroke)
