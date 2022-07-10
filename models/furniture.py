class Furniture():
    width = 100
    height = 100
    depth = 100


class Kitchen(Furniture):
    height = 90
    depth = 60


    def __str__(self):
        return "WxHxD"


basicFurniture = Furniture()
newKitchen = Kitchen()



print(basicFurniture)
print(newKitchen)
