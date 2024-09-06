class TransactionManager:
    def __init__(self):
        self.inventory = {}

    def add_to_inventory(self, basket_name, quantity):
        if basket_name in self.inventory:
            self.inventory[basket_name] += quantity
        else:
            self.inventory[basket_name] = quantity

    def remove_from_inventory(self, basket_name, quantity):
        if basket_name in self.inventory:
            if self.inventory[basket_name] >= quantity:
                self.inventory[basket_name] -= quantity
            else:
                print("Insufficient quantity in inventory.")
        else:
            print("Basket not found in inventory.")

    def get_inventory(self):
        return self.inventory