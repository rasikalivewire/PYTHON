from abc import ABC, abstractmethod

# Base Class
class Restaurant(ABC):

    def __init__(self, menu):
        self.__menu = menu  # Private Menu

    def get_menu(self):
        return self.__menu

    @abstractmethod
    def prepare_food(self):
        pass


# Pizza Restaurant
class PizzaRestaurant(Restaurant):

    def __init__(self):
        super().__init__({
            "Margherita Pizza": 200,
            "Veg Pizza": 250,
            "Cheese Burst Pizza": 350
        })

    def prepare_food(self):
        print("Preparing Pizza...")


# Burger Restaurant
class BurgerRestaurant(Restaurant):

    def __init__(self):
        super().__init__({
            "Veg Burger": 120,
            "Cheese Burger": 150,
            "Chicken Burger": 180
        })

    def prepare_food(self):
        print("Preparing Burger...")


# South Indian Restaurant
class SouthIndianRestaurant(Restaurant):

    def __init__(self):
        super().__init__({
            "Idli": 40,
            "Dosa": 70,
            "Vada": 50,
            "Pongal": 80
        })

    def prepare_food(self):
        print("Preparing South Indian Food...")


# ---------------- MAIN ----------------

restaurants = {
    1: PizzaRestaurant(),
    2: BurgerRestaurant(),
    3: SouthIndianRestaurant()
}

print("\n===== RESTAURANT SYSTEM =====")
print("1. Pizza Restaurant")
print("2. Burger Restaurant")
print("3. South Indian Restaurant")

choice = int(input("Choose Restaurant: "))

if choice in restaurants:

    r = restaurants[choice]

    print("\nMENU")
    menu = r.get_menu()

    items = list(menu.keys())

    for i, item in enumerate(items, start=1):
        print(f"{i}. {item} - ₹{menu[item]}")

    food_choice = int(input("\nSelect Food Item: "))
    qty = int(input("Enter Quantity: "))

    selected_food = items[food_choice - 1]
    price = menu[selected_food]

    r.prepare_food()

    bill = price * qty

    print("\n===== BILL =====")
    print("Food :", selected_food)
    print("Price:", price)
    print("Qty  :", qty)
    print("Total: ₹", bill)

else:
    print("Invalid Restaurant Choice")