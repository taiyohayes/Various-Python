from athlete.Boxer import Boxer
from athlete.Swimmer import Swimmer


def main():
    a = Swimmer("Allie Yen", "05/17/2002", "Cupertino", ["Gold (2020)", "Silver (2021)"], ["breaststroke"])
    a.add_stroke("backstroke")
    a.add_stroke("breaststroke")
    t = Boxer("Taiyo Hayes", "12/29/2001", "Seattle", ["Gold (2022)"], "welterweight")
    t.win_fight()
    t.win_fight()
    message = t.lose_fight()
    print(message)
    print(t)
    print(a)
    print("There are", Boxer.athlete_count, "athletes")
    print("There is", Boxer.boxer_count, "boxer")
    print("There is", Swimmer.swimmer_count, "swimmer")

if __name__ == '__main__':
    main()