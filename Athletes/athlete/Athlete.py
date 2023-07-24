class Athlete(object):
    athlete_count = 0

    def __init__(self, name_param, dob_param, origin_param, medals_param):
        self.name = name_param
        self.dob = dob_param
        self.origin = origin_param
        self.medals = medals_param
        Athlete.athlete_count += 1

    def get_name(self):
        return self.name

    def get_dob(self):
        return self.dob

    def get_origin(self):
        return self.origin

    def get_medals(self):
        return self.medals

    def add_medals(self, medals_param):
        self.medals.append(medals_param)

