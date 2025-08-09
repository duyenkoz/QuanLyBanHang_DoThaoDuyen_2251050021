class CartDTO:
    def __init__(self, id, quantity, price, title, image, total_price):
        self.id = id
        self.quantity = quantity
        self.price = price
        self.title = title
        self.image = image
        self.total_price = total_price