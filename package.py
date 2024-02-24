class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline, weight, status, departureTime, deliveredTime):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departureTime = departureTime
        self.deliveredTime = deliveredTime


    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zipcode,
                                                   self.deadline, self.weight, self.status)


