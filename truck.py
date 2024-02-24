class Truck:
    def __init__(self, miles, packages, lastDropOffPoint, nextDropOffPoint, time):
        self.miles = miles
        self.packages = packages
        self.lastDropOffPoint = lastDropOffPoint
        self.nextDropOffPoint = nextDropOffPoint
        self.time = time

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.miles, self.packages, self.lastDropOffPoint, self.nextDropOffPoint, self.time)