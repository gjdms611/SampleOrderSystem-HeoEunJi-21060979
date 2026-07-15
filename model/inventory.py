class Inventory:
    def __init__(self, sample_id: str, quantity: int):
        if quantity < 0:
            raise ValueError("quantity must not be negative")

        self.sample_id = sample_id
        self.quantity = quantity
