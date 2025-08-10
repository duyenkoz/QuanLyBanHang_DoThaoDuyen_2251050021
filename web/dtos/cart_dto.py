class CartDTO:
    def __init__(self, id, productid, quantity, price, title, image, total_price=None, size=None, sugar=None, ice=None, toppings=None):
        self.id = id
        self.productid = productid
        self.quantity = quantity
        self.price = price
        self.title = title
        self.image = image
        self.total_price = total_price
        self.size = size
        self.sugar = sugar
        self.ice = ice
        self.toppings = toppings
