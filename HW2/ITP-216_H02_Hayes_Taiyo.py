# Taiyo Hayes, tjhayes@usc.edu
# ITP 216, Fall 2022
# Section: 32081
# Assignment 2
# Description: Pet Organizer using dictionary

def main():
    cats_names = ('Cassandra', 'Sir Whiskington', 'Truck')
    dogs_names = {'Barkey McBarkface', 'Leeloo Dallas', 'Taro'}
    parrots_names = ['Squawk', 'Squawk 2: the Squawkquel', 'Larry']
    names = ['peter', 'paul', 'mary']
    animals = ('cat', 'cat', 'hamster')

    all_pets = {}
    all_pets["cat"] = list(cats_names)
    all_pets["dog"] = list(dogs_names)
    all_pets["parrot"] = parrots_names
    for i in range(3):
        if animals[i] in all_pets.keys():
            all_pets[animals[i]].append(names[i].capitalize())
        else:
            all_pets[animals[i]] = [names[i].capitalize()]
    pets = 12

    print("Please choose from the following options:\n\t1. See all your pets' names.\n\t2. Add a pet. \n\t3. Exit.")
    answer = input("What would you like to do? (1, 2, 3): ")
    while answer != '3':
        if answer == '1':
            print("\nYou have " + str(pets) + " pets.")
            for key in all_pets:
                print(key + ": " + ', '.join(all_pets[key]))
        elif answer == '2':
            animal = input("\nWhat kind of animal is this?: ")
            name = input("\nWhat is the name of the " + animal + "?: ")
            if animal in all_pets.keys():
                all_pets[animal].append(name)
            else:
                all_pets[animal] = [name]
            print("\nGreat! " + name + " the " + animal + " is now added to your pets.")
            pets += 1
        else:
            print("\nThat is not a number.")
        print("\nPlease choose from the following options:\n\t1. See all your pets' names.\n\t2. Add a pet.\n\t3. Exit.")
        answer = input("What would you like to do? (1, 2, 3): ")
    print("\nGoodbye!")
if __name__ == '__main__':
    main()