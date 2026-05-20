class Car:
    def __init__(self, make, model, year,price):
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        print("------over------")
    def __str__(self):
        return (f"{self.make} - {self.model} - {self.year}")
    def __eq__(self, other):
        return self.price == other.price

lambo = Car("China","Big Bull",2018,3000000)
falara = Car("ytali","La Fa",2019,3000000)
print(lambo.make)
print(lambo.model)
print(lambo.year)

print(lambo)
print(falara)
print(lambo.__eq__(falara))
print(lambo == falara)