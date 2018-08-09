import random

class groupTravel:

    def __init__(self, people, flights, dest):
        self.familyMembers = []
        self.flights = {}
        self.destination = dest
        #Dumping family data in dictionary
        with open(people) as file:
            for line in file:
                person,city = line.strip().split(',')
                self.familyMembers.append([person,city])
        #Dumping flights data in dictionary
        with open(flights) as file:
            for line in file:
                source,destination,departure,arrival,price = line.strip().split(',')
                self.flights.setdefault((source,destination), [])
                #Key is (origin, destination) and value is (departure, arrival, price) of flight
                self.flights[(source,destination)].append((departure,arrival,int(price)))

    #Converts HH:MM into minutes
    def getMinutes(self, time):
        hours = time.strip().split(':')
        return int(hours[0])*60 + int(hours[1])

    #Printing solution
    def printSolution(self, solution):
        i = 0
        print('Trip plan:')
        for person, city in self.familyMembers:
            print(person, ':')
            print('    ', 'from:', city, self.flights[(city, self.destination)][solution[i]][0], 'To:', self.destination, self.flights[(city, self.destination)][solution[i]][1])
            i = i + 1   #For return flight
            print('    ', 'from:', self.destination, self.flights[(self.destination, city)][solution[i]][0], 'To:', city, self.flights[(self.destination, city)][solution[i]][1])
            i = i + 1
        print('Total cost:', cost)

    #Calculates total cost of a solution
    def calculateCost(self, solution):
        totalCost = 0
        lastArrivalAtDestination = 0
        firstDepartureFromDestination = 24*60
        
        i = 0
        for person, city in self.familyMembers:
            outboundFlight = self.flights[(city,self.destination)][solution[i]]
            returnFlight = self.flights[(self.destination, city)][solution[i+1]]
            #Time taken in going and returning
            minutesOutbound  = self.getMinutes(outboundFlight[1]) - self.getMinutes(outboundFlight[0])
            minutesReturn  = self.getMinutes(returnFlight[1]) - self.getMinutes(returnFlight[0])

            #Outbound and return flight cost
            totalCost += outboundFlight[2];
            totalCost += returnFlight[2];
            #Hour cost is 1$/hour
            totalCost += minutesOutbound * 1;
            totalCost += minutesReturn * 1;

            #Setting arrival time of person reaches last
            if(lastArrivalAtDestination < self.getMinutes(outboundFlight[1])):
                lastArrivalAtDestination = self.getMinutes(outboundFlight[1])
            #Setting departure time of person leaves first
            if(firstDepartureFromDestination > self.getMinutes(returnFlight[0])):
                firstDepartureFromDestination = self.getMinutes(returnFlight[0])
            i = i + 2

        totalWait = 0
        i = 0
        for person, city in self.familyMembers:
            #Person's waiting time on airport
            outboundFlight = self.flights[(city,self.destination)][solution[i]]
            returnFlight = self.flights[(self.destination, city)][solution[i+1]]
            waitOutbound  = lastArrivalAtDestination - self.getMinutes(outboundFlight[1])
            waitReturn  = self.getMinutes(returnFlight[0]) - firstDepartureFromDestination

            totalWait += (waitOutbound + waitReturn)
            i = i + 2
        #Per hour cost of wait is 0.5$/hour
        totalCost += 0.5 * totalWait
        return totalCost

    #Hill Climbing Approach to find best solution
    def hillClimbSolution(self, costFun):
        randomSolution = []
        #Generating a random solution
        for person, city in self.familyMembers:
            maxFlightsOutBound = len(self.flights[(city, self.destination)])
            maxFlightsReturn = len(self.flights[(self.destination, city)])
            randomSolution.append(random.randint(0, maxFlightsOutBound - 1))
            randomSolution.append(random.randint(0, maxFlightsReturn - 1))

        while 1:
            neighbours = []
            for i in range(len(randomSolution)):
                origin = None
                destination = None
                #Switching origin and destination based on index
                #(0,2,4,6,8) are upbound and (1,3,5,7,9) are return for each person
                if(i%2 == 0):
                    origin = self.familyMembers[int(i/2)][1]
                    destination = self.destination
                else:
                    origin = self.destination
                    destination = self.familyMembers[int(i/2)][1]

                #One way up
                if(randomSolution[i] < (len(self.flights[(origin, destination)]) - 1)):
                    solution = randomSolution[0:i]+[randomSolution[i]+1]+randomSolution[i+1:]
                    neighbours.append(solution)
                #One way down
                if(randomSolution[i] > 0):
                    solution = randomSolution[0:i]+[randomSolution[i]-1]+randomSolution[i+1:]
                    neighbours.append(solution)
            #Current solution cost
            currentSolution = costFun(randomSolution)
            bestSolution = currentSolution
            print('Current cost:', currentSolution)
            for solution in neighbours:
                cost = costFun(solution)
                #If neighbour is best solution
                if cost < bestSolution:
                    bestSolution = cost
                    randomSolution = solution

            #If no improvement in neighbours then we have reached bottom of hill
            if(currentSolution == bestSolution):
                break;

        return randomSolution, bestSolution



grp = groupTravel('Data\\Family.txt', 'Data\\Flights.txt', "Seattle")
sol, cost = grp.hillClimbSolution(grp.calculateCost)
grp.printSolution(sol)
#print(grp.calculateCost([1,0,1,1,0,1,1,0,1,1]))