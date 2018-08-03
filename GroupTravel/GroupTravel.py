

class groupTravel:

    def __init__(self, people, flights, dest):
        self.familyMembers = {}
        self.flights = {}
        self.destination = dest
        #Dumping family data in dictionary
        with open(people) as file:
            for line in file:
                person,city = line.strip().split(',')
                self.familyMembers[person] = city
        #Dumping flights data in dictionary
        with open(flights) as file:
            for line in file:
                source,destination,departure,arrival,price = line.strip().split(',')
                self.flights.setdefault((source,destination), [])
                self.flights[(source,destination)].append((departure,arrival,int(price)))

    def getMinutes(self, time):
        hours = time.strip().split(':')
        return int(hours[0])*60 + int(hours[1])

    def calculateCost(self, solution):
        totalCost = 0
        lastArrivalAtDestination = 0
        earlistDepartureFromDestination=24*60
        i = 0
        for person, city in self.familyMembers.items():
            outboundFlight = self.flights[(city,self.destination)][solution[i]]
            returnFlight = self.flights[(self.destination, city)][solution[i+1]]
            hoursOutbound  = self.getMinutes(outboundFlight[1]) - self.getMinutes(outboundFlight[0])
            hoursReturn  = self.getMinutes(returnFlight[1]) - self.getMinutes(returnFlight[0])

            totalCost += outboundFlight[2];
            totalCost += hoursOutbound * 1;
            totalCost += returnFlight[2];
            totalCost += hoursReturn * 1;

            if(lastArrivalAtDestination < self.getMinutes(outboundFlight[1])):
                lastArrivalAtDestination = self.getMinutes(outboundFlight[1])
            if(earlistDepartureFromDestination > self.getMinutes(returnFlight[0])):
                earlistDepartureFromDestination = self.getMinutes(returnFlight[0])

            x = 0
grp = groupTravel('Data\\Family.txt', 'Data\\Flights.txt', "Seattle")

grp.calculateCost([1,0,1,1,0,1,1,0,1,1])