import math
import random

class kNearestNeighbors:
    def __init__(self):
        pass

    #genearting price
    def winePrice(self, rating, age):
        peakAge = (rating+1)*20
        price = (rating+1)
        if(age > peakAge):
            #after 5 years of peak age wine will be expired
            price += price*(5 - (age - peakAge))
        else:
            #price will be increased in proportional to it's age
            price += price*(5*(age+1)/peakAge)

        if(price < 0): price = 0
        return price

    #generating random 200 wine data
    def generateRandomWines(self):
        wines = []
        for i in range(200):
            #rating in range of 0-5
            rating = round(random.random()*5)
            #age in range of 10-20
            age = round(random.random()*10) + 10
            price = self.winePrice(rating,age)
            wines.append({'input':(rating,age), 'result':price})
        return wines

    #calculating eluclidean distance
    def eluclideanDistance(self, obj1, obj2):
        distance = math.sqrt(sum([(obj1[i] - obj2[i])**2 for i in range(len(obj1))]))
        return distance

    #distance of object from all other training data
    def getDistances(self, data, obj1):
        distances  = []
        for i in range(len(data)):
            obj2 = data[i]['input']
            #distance, index of data item
            distances.append((self.eluclideanDistance(obj1, obj2), i))
        distances.sort()
        return distances

    def knnEstimate(self, data, obj1, k=3):
        distList = self.getDistances(data, obj1)
        avg = 0
        #considering only k neighbors
        for i in range(k):
            index = distList[i][1]
            avg += data[index]['result']

        return avg/k

    #weighted average of k neighbors
    def knnWeightedEstimate(self, data, obj1, weightFun, k=3):
        distList = self.getDistances(data, obj1)
        avg = 0
        totalWeight = 0

        averageDistance = sum([distList[i][0] for i in range(k)])/k
        standardDiviation = math.sqrt(sum([(averageDistance - distList[i][0])**2 for i in range(k)])/(k-1))

        for i in range(k):
            index = distList[i][1]
            price = data[index]['result']
            weight = weightFun(distList[i][0], standardDiviation)

            avg += price*weight
            totalWeight += weight

        return avg/totalWeight

    #gusssian function to calculate weight
    def gaussianFunction(self, distance, standerdDeviation):
        return math.e**(-distance**2/2*standerdDeviation**2)

knn = kNearestNeighbors()
#wine data
wines = knn.generateRandomWines()
#new wine which price to be calculated
wine1 = (4,30)
print(knn.knnWeightedEstimate(wines, wine1, knn.gaussianFunction))