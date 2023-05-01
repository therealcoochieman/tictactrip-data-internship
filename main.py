import algorithms
import loader


def print_instructions():
    print("[1]. Show minimum, maximum, and average prices for each trip on the database")
    print("[2]. Show minimum, maximum, and average duration for each trip on the database")
    print("[3]. Show time & price averages seperated in intervals (<200km, <800km, ...)")
    print("[4]. Estimate time & price of a trip depending on its origin, destination, and transport mode")
    print("[5]. Show time & price data of a specific trip")
    print("[6]. Exit this masterpiece of a UI")


def switch(user_input):
    if user_input == 1:
        return algorithms.route_price()
    elif user_input == 2:
        return algorithms.route_duration()
    elif user_input == 3:
        return algorithms.display_route_ranges()
    elif user_input == 4:
        return algorithms.predict_origin_to_dest()
    elif user_input == 5:
        return algorithms.specific_route_duration()

    print("I look forward to hearing from you! :)")
    exit(0)


def main():
    print("Hello Hello!\nWelcome to Theo's entry exercise! How can I help?")
    possible_inputs = [1, 2, 3, 4, 5, 6]
    while True:
        user_input = -1
        while user_input not in possible_inputs:
            print_instructions()
            user_input = loader.input_num("Just pick from the above!")

        switch(user_input)


main()
