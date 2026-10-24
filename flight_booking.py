# Task 04: Flight Booking Console Application — OOP
# Name: Gaurav Ravindra More
# Date: 23 October 2026

import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

# Ensure UTF-8 output encoding across all platforms and Windows consoles
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def format_currency(amount: float) -> str:
    """Format an amount with the Rupee symbol (e.g., ₹4,000 or ₹4,000.50)."""
    if amount == int(amount):
        return f"₹{int(amount):,}"
    return f"₹{amount:,.2f}"


# ============================================================================
# 1. Flight Class (Demonstrating Class, Object & Encapsulation)
# ============================================================================
class Flight:
    """
    Represents a flight. Seat availability is encapsulated and protected
    from arbitrary direct modifications.
    """

    def __init__(
        self,
        flight_code: str,
        airline: str,
        source: str,
        destination: str,
        available_seats: int,
        base_fare: float,
    ):
        self._flight_code = flight_code.strip().upper()
        self._airline = airline.strip()
        self._source = source.strip()
        self._destination = destination.strip()
        self._available_seats = max(0, int(available_seats))
        self._base_fare = float(base_fare)

    @property
    def flight_code(self) -> str:
        return self._flight_code

    @property
    def airline(self) -> str:
        return self._airline

    @property
    def source(self) -> str:
        return self._source

    @property
    def destination(self) -> str:
        return self._destination

    @property
    def route(self) -> str:
        return f"{self._source} to {self._destination}"

    @property
    def available_seats(self) -> int:
        """Encapsulated getter for available seats."""
        return self._available_seats

    @property
    def base_fare(self) -> float:
        return self._base_fare

    def has_seats(self, count: int) -> bool:
        """Check if the requested number of seats is available."""
        return count > 0 and count <= self._available_seats

    def book_seats(self, count: int) -> bool:
        """
        Controlled method to decrement seat count (Encapsulation).
        Seats are only deducted if there are sufficient seats available.
        """
        if self.has_seats(count):
            self._available_seats -= count
            return True
        return False

    def __str__(self) -> str:
        return (
            f"{self._flight_code:<10} {self._airline:<14} "
            f"{self.route:<24} {self._available_seats:<15} "
            f"{format_currency(self._base_fare)}"
        )


# ============================================================================
# 2. Passenger Hierarchy (Demonstrating Abstraction, Inheritance & Polymorphism)
# ============================================================================
class Passenger(ABC):
    """
    Abstract Base Class defining the passenger contract (Abstraction).
    All passenger types must declare their type and discount rate.
    """

    def __init__(self, name: str, age: int):
        self._name = name.strip()
        self._age = int(age)

    @property
    def name(self) -> str:
        return self._name

    @property
    def age(self) -> int:
        return self._age

    @property
    @abstractmethod
    def passenger_type(self) -> str:
        """Abstract property representing the passenger type name."""
        pass

    @abstractmethod
    def get_discount_percentage(self) -> float:
        """
        Abstract method defining discount percentage (e.g. 0.10 for 10%).
        Overridden by concrete subclasses.
        """
        pass

    def calculate_discount(self, subtotal: float) -> float:
        """
        Polymorphic calculation: determines discount amount using the subclass rate.
        """
        return subtotal * self.get_discount_percentage()


class RegularPassenger(Passenger):
    """
    Represents a regular passenger with a 0% discount.
    """

    @property
    def passenger_type(self) -> str:
        return "Regular"

    def get_discount_percentage(self) -> float:
        return 0.0


class StudentPassenger(Passenger):
    """
    Represents a student passenger with a 10% discount.
    """

    @property
    def passenger_type(self) -> str:
        return "Student"

    def get_discount_percentage(self) -> float:
        return 0.10  # 10% student discount


# ============================================================================
# 3. Booking Class (Demonstrating Class, Object & Encapsulation)
# ============================================================================
class Booking:
    """
    Represents a confirmed booking containing passenger, flight, and fare details.
    """

    def __init__(
        self,
        booking_id: str,
        flight: Flight,
        passenger: Passenger,
        num_tickets: int,
    ):
        self._booking_id = booking_id
        self._flight = flight
        self._passenger = passenger
        self._num_tickets = num_tickets

        # Calculate fare details
        self._base_fare = flight.base_fare
        self._subtotal = self._base_fare * num_tickets
        # Polymorphic discount calculation
        self._discount = passenger.calculate_discount(self._subtotal)
        self._final_amount = self._subtotal - self._discount

    @property
    def booking_id(self) -> str:
        return self._booking_id

    @property
    def flight(self) -> Flight:
        return self._flight

    @property
    def passenger(self) -> Passenger:
        return self._passenger

    @property
    def num_tickets(self) -> int:
        return self._num_tickets

    @property
    def base_fare(self) -> float:
        return self._base_fare

    @property
    def subtotal(self) -> float:
        return self._subtotal

    @property
    def discount(self) -> float:
        return self._discount

    @property
    def final_amount(self) -> float:
        return self._final_amount

    def get_summary(self) -> str:
        """Returns the formatted summary string for this booking."""
        discount_rate_pct = int(self._passenger.get_discount_percentage() * 100)
        lines = [
            f"Booking ID: {self._booking_id}",
            f"Flight: {self._flight.flight_code} | {self._flight.route}",
            f"Passenger: {self._passenger.name}",
            f"Passenger type: {self._passenger.passenger_type}",
            f"Tickets: {self._num_tickets}",
            f"Base fare per ticket: {format_currency(self._base_fare)}",
            f"Subtotal: {format_currency(self._subtotal)}",
            f"{self._passenger.passenger_type} discount ({discount_rate_pct}%): {format_currency(self._discount)}",
            f"Final amount: {format_currency(self._final_amount)}",
        ]
        return "\n".join(lines)


# ============================================================================
# 4. Flight Booking System (System Coordination & Program Flow)
# ============================================================================
class FlightBookingSystem:
    """
    Coordinates flight inventory, bookings, validations, fare calculations,
    and the user interactive console menu.
    """

    def __init__(self):
        self._flights: Dict[str, Flight] = {}
        self._bookings: List[Booking] = []
        self._next_booking_number: int = 1001

        self._initialize_flights()

    def _initialize_flights(self) -> None:
        """Initializes at least 3 predefined flights into system memory."""
        predefined_flights = [
            Flight("PN101", "IndiGo", "Pune", "Delhi", 20, 4000.0),
            Flight("AI202", "Air India", "Mumbai", "Bengaluru", 25, 4500.0),
            Flight("SG303", "SpiceJet", "Pune", "Hyderabad", 15, 3500.0),
            Flight("UK404", "Vistara", "Mumbai", "Delhi", 10, 5000.0),
        ]
        for flight in predefined_flights:
            self._flights[flight.flight_code] = flight

    def display_flights(self) -> None:
        """Displays available flights with code, airline, route, seats, and fare."""
        print("\nAvailable Flights:")
        print("-" * 75)
        print(f"{'Code':<10} {'Airline':<14} {'Route':<24} {'Seats':<15} {'Base Fare'}")
        print("-" * 75)
        for flight in self._flights.values():
            print(flight)
        print("-" * 75)

    def find_flight(self, flight_code: str) -> Optional[Flight]:
        """Finds and returns a flight by code, or None if not found."""
        if not flight_code:
            return None
        return self._flights.get(flight_code.strip().upper())

    def validate_booking_details(
        self,
        flight_code: str,
        passenger_name: str,
        age_str: str,
        passenger_type_str: str,
        num_tickets_str: str,
    ) -> Tuple[bool, str, Optional[Flight], Optional[Passenger], int]:
        """
        Validates all booking inputs:
        - Flight code must exist
        - Passenger name cannot be blank
        - Age must be a positive integer
        - Passenger type must be Regular or Student
        - Number of tickets must be a positive integer
        - Seat availability must be sufficient

        Returns (is_valid, error_message, flight, passenger, num_tickets)
        """
        # 1. Flight code validation
        flight = self.find_flight(flight_code)
        if not flight:
            return (
                False,
                f"Flight code '{flight_code.strip().upper()}' does not exist.",
                None,
                None,
                0,
            )

        # 2. Passenger name validation
        cleaned_name = passenger_name.strip()
        if not cleaned_name:
            return False, "Passenger name cannot be blank.", None, None, 0

        # 3. Age validation
        try:
            age = int(age_str.strip())
            if age <= 0:
                return False, "Age must be greater than 0.", None, None, 0
        except ValueError:
            return False, "Invalid age. Please enter a valid number.", None, None, 0

        # 4. Passenger type validation & polymorphic object creation
        type_clean = passenger_type_str.strip().lower()
        if type_clean in ("student", "s"):
            passenger = StudentPassenger(cleaned_name, age)
        elif type_clean in ("regular", "r"):
            passenger = RegularPassenger(cleaned_name, age)
        else:
            return (
                False,
                "Invalid passenger type. Please enter 'Regular' or 'Student'.",
                None,
                None,
                0,
            )

        # 5. Number of tickets validation
        try:
            tickets = int(num_tickets_str.strip())
            if tickets <= 0:
                return False, "Number of tickets must be greater than 0.", None, None, 0
        except ValueError:
            return False, "Invalid number of tickets. Please enter a valid number.", None, None, 0

        # 6. Seat availability check
        if not flight.has_seats(tickets):
            return (
                False,
                "Not enough seats available.\nNo booking was created. Available seats remain unchanged.",
                None,
                None,
                0,
            )

        return True, "", flight, passenger, tickets

    def calculate_fare(
        self, flight: Flight, passenger: Passenger, num_tickets: int
    ) -> Tuple[float, float, float]:
        """
        Calculates subtotal, discount, and final amount.
        Formula:
          Subtotal = base fare * number of tickets
          Discount = subtotal * passenger discount percentage
          Final total = subtotal - discount
        """
        subtotal = flight.base_fare * num_tickets
        discount = passenger.calculate_discount(subtotal)
        final_amount = subtotal - discount
        return subtotal, discount, final_amount

    def confirm_booking(
        self, flight: Flight, passenger: Passenger, num_tickets: int
    ) -> Optional[Booking]:
        """
        Confirms booking: decreases available seats, generates booking ID,
        and saves confirmed booking to memory.
        """
        if not flight.book_seats(num_tickets):
            return None

        booking_id = f"BK{self._next_booking_number}"
        self._next_booking_number += 1

        booking = Booking(booking_id, flight, passenger, num_tickets)
        self._bookings.append(booking)
        return booking

    def display_summary(self, booking: Booking) -> None:
        """Displays the confirmed booking summary."""
        print("\nBooking confirmed!")
        print(booking.get_summary())

    def view_recent_booking(self) -> None:
        """Displays the most recent confirmed booking."""
        if not self._bookings:
            print("\nNo bookings found. Please book a flight first.")
            return

        recent_booking = self._bookings[-1]
        print("\n--- Most Recent Booking ---")
        print(recent_booking.get_summary())

    def book_flight_flow(self) -> None:
        """Interactive flow for booking a flight."""
        flight_code = input("Enter flight code: ").strip()
        passenger_name = input("Enter passenger name: ").strip()
        age_str = input("Enter age: ").strip()
        passenger_type_str = input("Passenger type (Regular/Student): ").strip()
        num_tickets_str = input("Enter number of tickets: ").strip()

        (
            is_valid,
            error_msg,
            flight,
            passenger,
            tickets,
        ) = self.validate_booking_details(
            flight_code,
            passenger_name,
            age_str,
            passenger_type_str,
            num_tickets_str,
        )

        if not is_valid:
            print(f"\nBooking failed: {error_msg}")
            return

        booking = self.confirm_booking(flight, passenger, tickets)
        if booking:
            self.display_summary(booking)
        else:
            print("\nBooking failed: Unable to confirm seat reservation.")

    def run(self) -> None:
        """Main menu loop."""
        print("Welcome to Kiran Air Booking")

        while True:
            print("\n1. View Flights")
            print("2. Book Flight")
            print("3. View Booking")
            print("4. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.display_flights()
            elif choice == "2":
                self.book_flight_flow()
            elif choice == "3":
                self.view_recent_booking()
            elif choice == "4":
                print("Thank you for using Kiran Air Booking!")
                break
            else:
                print("Invalid choice. Please select 1, 2, 3, or 4.")


def main():
    system = FlightBookingSystem()
    system.run()


if __name__ == "__main__":
    main()
