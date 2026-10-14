# Calculate electronics amount with 18% GST
def calculateElectronicsGST(a, b):
    amount = a + b
    gst = amount * 18 / 100
    return amount + gst


# Calculate fashion amount with 13% GST
def calculateFashionGST(c, d):
    amount = c + d
    gst = amount * 13 / 100
    return amount + gst


# Calculate food amount with 7% GST
def calculateFoodGST(e):
    gst = e * 7 / 100
    return e + gst


# Calculate total bill after GST
def totalBill(a, b, c, d, e):
    electronics = calculateElectronicsGST(a, b)
    fashion = calculateFashionGST(c, d)
    food = calculateFoodGST(e)

    return electronics + fashion + food


# Calculate the final bill after a 20% discount
def calculateDiscountedBill(a, b, c, d, e):
    total = totalBill(a, b, c, d, e)
    discount = total * 20 / 100

    return total - discount


# Sample values supplied directly to the functions
a = 100
b = 100
c = 100
d = 100
e = 100

electronics = calculateElectronicsGST(a, b)
fashion = calculateFashionGST(c, d)
food = calculateFoodGST(e)

total = totalBill(a, b, c, d, e)
discount = total * 20 / 100
final_amount = calculateDiscountedBill(a, b, c, d, e)

print(f"Electronics after GST: Rs. {electronics:.2f}")
print(f"Fashion after GST: Rs. {fashion:.2f}")
print(f"Food after GST: Rs. {food:.2f}")
print(f"Total after GST: Rs. {total:.2f}")
print(f"Discount: Rs. {discount:.2f}")
print(f"Final payable amount: Rs. {final_amount:.2f}")