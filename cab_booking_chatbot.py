import random

# Predefined cab rates (rupees per kilometre)
cab_rates = {
    "1": ("Auto", 12),
    "2": ("Sedan", 18),
    "3": ("SUV", 25)
}

# Predefined routes: route number -> (source, destination, distance)
routes = {
    "1": ("Pune Station", "Shivajinagar", 5),
    "2": ("Swargate", "Kothrud", 8),
    "3": ("Hinjawadi", "Wakad", 10)
}

while True:
    print("\n===== CAB BOOKING CHATBOT =====")
    print("1. Book Ride")
    print("2. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "2":
        print("Thank you for using Cab Booking Chatbot. Goodbye!")
        break

    elif choice == "1":
        print("\nChoose your cab type:")
        print("1. Auto - Rs. 12/km")
        print("2. Sedan - Rs. 18/km")
        print("3. SUV - Rs. 25/km")

        cab_choice = input("Enter cab choice (1-3): ").strip()

        if cab_choice not in cab_rates:
            print("Invalid cab choice. Returning to the main menu.")
            continue

        cab_type, rate = cab_rates[cab_choice]

        print("\nChoose your route:")
        print("1. Pune Station to Shivajinagar - 5 km")
        print("2. Swargate to Kothrud - 8 km")
        print("3. Hinjawadi to Wakad - 10 km")

        route_choice = input("Enter route choice (1-3): ").strip()

        if route_choice not in routes:
            print("Invalid route choice. Returning to the main menu.")
            continue

        source, destination, distance = routes[route_choice]
        fare = rate * distance

        print("\n----- RIDE DETAILS -----")
        print(f"Cab Type       : {cab_type}")
        print(f"Source         : {source}")
        print(f"Destination    : {destination}")
        print(f"Distance       : {distance} km")
        print(f"Rate           : Rs. {rate}/km")
        print(f"Total Fare     : Rs. {fare}")

        print("\n1. Confirm & Share OTP")
        print("2. Cancel Ride")
        confirm_choice = input("Enter your choice: ").strip()

        if confirm_choice == "2":
            print("Ride cancelled. No OTP has been shared.")
            continue

        elif confirm_choice == "1":
            otp = random.randint(1000, 9999)
            print(f"Your ride OTP is: {otp}")
            print("Important: Once the OTP is shared, the ride cannot be cancelled.")
            print("Booking confirmed. Have a safe journey!")
            continue

        else:
            print("Invalid choice. Ride cancelled; no OTP has been shared.")
            continue

    else:
        print("Invalid menu choice. Please enter 1 or 2.")
