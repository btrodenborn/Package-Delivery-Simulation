#Brian Rodenborn - 010518741
import csv
from package import Package
import truck
from hashTable import ChainingHashTable
import datetime

#open address csv file
with open("CSV/addressCSV") as csvFile1:
    addressCSV = csv.reader(csvFile1)
    addressCSV = list(addressCSV)

#open distance csv file
with open("CSV/distanceCSV") as csvFile2:
    distanceCSV = csv.reader(csvFile2)
    distanceCSV = list(distanceCSV)

#open package file, read in data, create packages, and store packages in hash table
def loadPackageData(fileName):
    with open(fileName) as packageInformation:
        packageData = csv.reader(packageInformation, delimiter=',')
        for package in packageData:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pStatus = "At the hub"
            pDepartureTime = 0
            pDeliveredTime = 0

            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline, pWeight, pStatus, pDepartureTime, pDeliveredTime)

            packageHashTable.insert(pID, p)

packageHashTable = ChainingHashTable()

loadPackageData("CSV/packageCSV")

#use the address from a package and return an address id number
def address(address):
    for row in addressCSV:
        if address in row[2]:
            return int(row[0])

#Use the distance matrix to find the distance between two addresses. Since the matrix is bi-directional the addresses have to be read both ways.
def distanceBetweenAddress(i, j):
    distance = distanceCSV[i][j]
    if distance == '':
        distance = distanceCSV[j][i]
    return float(distance)

#find the package from truckPackages with the shortest distance from the current location of the truck
def findNextPackage(fromAddress, truckPackages):
    minDistance = 100000
    nextPackageDelivered = None
    for package in truckPackages:
        if distanceBetweenAddress(address(fromAddress), address(package.address)) <= minDistance:
            minDistance = distanceBetweenAddress(address(fromAddress), address(package.address))
            nextPackageDelivered = package
    return nextPackageDelivered

#Sets the status of a package at a user inputted time for a specific package choose by the user. Returns said package.
def packageStatusUpdate(packageID, timeInput):
    package = packageHashTable.search(packageID)
    if package.departureTime < timeInput and package.deliveredTime > timeInput:
        package.status = "En route"
    if package.departureTime > timeInput:
        package.status = "At the hub"
    return package

#Sets the status of all packages at a user inputted time and then prints all of the packages.
def packageStatusUpdateAll(timeInput):
    for x in range(1,41):
        package = packageHashTable.search(x)
        if package.departureTime < timeInput and package.deliveredTime > timeInput:
            package.status = "En route"
        if package.departureTime > timeInput:
            package.status = "At the hub"
        print(package)

#updates the departure time of a specific package
def packageUpdateDeparture(packageID, time):
    p = packageHashTable.search(packageID)
    p.departureTime = time

#updates the package status to delivered and gives the time of delivery to the package status
def packageStatusDelivered(packageID, time):
    p = packageHashTable.search(packageID)
    p.deliveredTime = time
    p.status = str(time) + " - Delivered"

#totals the mileage of all 3 trucks
def totalMiles(truck1, truck2, truck3):
    total = truck1.miles + truck2.miles + truck3.miles
    return str(total)

#This first loads the packages from the specific truck into an array. Then while there are still packages remaining in the array, this function calls
#findNextPackage to find the next address to deliver by finding the shortest distance remaining in the array. Then this function updates the specific
#truck's time and mileage, calls packageStatusDelivered function, sets the current location and removes the delivered package from the array.
def deliverPackages(truck):
    packagesToBeDelivered = []
    for packageID in truck.packages:
        package = packageHashTable.search(packageID)
        packagesToBeDelivered.append(package)
        packageUpdateDeparture(packageID, truck.time)

    while len(packagesToBeDelivered) > 0:
        nextPackage = findNextPackage(truck.lastDropOffPoint, packagesToBeDelivered)
        truck.nextDropOffPoint = nextPackage.address
        truck.miles += distanceBetweenAddress(address(truck.lastDropOffPoint), address(truck.nextDropOffPoint))
        truck.time += datetime.timedelta(hours=distanceBetweenAddress(address(truck.lastDropOffPoint),
                                                                      address(truck.nextDropOffPoint))/18)
        packageStatusDelivered(nextPackage.ID, truck.time)
        truck.lastDropOffPoint = truck.nextDropOffPoint
        packagesToBeDelivered.remove(nextPackage)

#Truck declarations
truck1 = truck.Truck(0, [1,13,14,15,16,19,29,30,34,37,40,20,21], "4001 South 700 East", None, datetime.timedelta(hours = 8))
truck2 = truck.Truck(0, [3,18,28,32,36,38,11,17,12,39,2,5,9,23], "4001 South 700 East", None, datetime.timedelta(hours = 10, minutes = 20))
truck3 = truck.Truck(0, [4,7,8,10,22,24,27,33,35,31,25,26,6], "4001 South 700 East", None, datetime.timedelta(hours = 9, minutes = 5))
deliverPackages(truck1)
deliverPackages(truck3)
deliverPackages(truck2)

#this is the interactive menu for the user
def menu():
    response = ""
    while response != "4":
        print("Options:")
        print("1. Print All Package Status and Total Mileage")
        print("2. Get a Single Package Status with a Time")
        print("3. Get All Package Status with a Time")
        print("4. Exit the Program")
        response = input("Enter a menu option")
        if response == "1":
            for packageID in range(1, 41):
                print(packageHashTable.search(packageID))
            print("Total Mileage: " + totalMiles(truck1, truck2, truck3))
        if response == "2":
            responseID = input("Please enter a package ID (1-40) to be searched")
            responseTime = input("Please enter a time in format 00:00")
            (hour, minute) = responseTime.split(":")
            pID = int(responseID)
            timeInput = datetime.timedelta(hours=int(hour), minutes=int(minute))
            p = packageStatusUpdate(pID, timeInput)
            print(p)
            print("Total Mileage: " + totalMiles(truck1, truck2, truck3))
        if response == "3":
            responseTime = input("Please enter a time in format 00:00")
            (hour, minute) = responseTime.split(":")
            timeInput = datetime.timedelta(hours=int(hour), minutes=int(minute))
            packageStatusUpdateAll(timeInput)
            print("Total Mileage: " + totalMiles(truck1, truck2, truck3))

    print("Exiting the program")

menu()















