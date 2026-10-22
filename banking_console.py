# Task 03: Banking Console Application
# Name: Gaurav Ravindra More

def main():
    balance = 10000.00

    print("Welcome to Kiran Bank")
    print(f"Opening Balance: ₹{balance:.2f}")

    while True:
        print("\n--- Banking Menu ---")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            print(f"Current Balance: ₹{balance:.2f}")

        elif choice == "2":
            amount_text = input("Enter deposit amount: ").strip()
            try:
                amount = float(amount_text)
                if amount <= 0:
                    print("Invalid amount. Please enter an amount greater than 0.")
                else:
                    balance += amount
                    print("Deposit successful.")
                    print(f"Updated Balance: ₹{balance:.2f}")
            except ValueError:
                print("Invalid amount. Please enter a valid number.")

        elif choice == "3":
            amount_text = input("Enter withdrawal amount: ").strip()
            try:
                amount = float(amount_text)
                if amount <= 0:
                    print("Invalid amount. Please enter an amount greater than 0.")
                elif amount > balance:
                    print("Transaction failed: Insufficient balance.")
                    print(f"Current Balance: ₹{balance:.2f}")
                else:
                    balance -= amount
                    print("Withdrawal successful.")
                    print(f"Updated Balance: ₹{balance:.2f}")
            except ValueError:
                print("Invalid amount. Please enter a valid number.")

        elif choice == "4":
            print("Thank you for banking with us. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
