import math
import sys
import json
import random

def pearsonScore(obj1, obj2):
    col = {}
    for item in obj1:
        if item in obj2:
            col[item] = 1;
    n = len(col)
    if(n == 0):
        return 0;
    #calculating sum
    sum1 = sum([obj1[item] for item in col])
    sum2 = sum([obj2[item] for item in col])
    #calculating sum of squares
    sumSq1 = sum([pow(obj1[item], 2) for item in col])
    sumSq2 = sum([pow(obj2[item], 2) for item in col])
    #calculating sum of products
    sumPr = sum([obj1[item] * obj2[item] for item in col])
    #calculating pearson score
    num = sumPr - (sum1*sum2)/n
    den = math.sqrt(abs(sumSq1 - pow(sum1, 2)/n)*abs(sumSq2 - pow(sum1, 2)/n))
    if(den == 0):
        return 0
    return num/den

def kClusterCreate(rows, k, distance_score = pearsonScore):
    # picking a company to list all properties
    randonCompany = next(iter(rows))
    properties = rows[randonCompany]
    # getting maximum and minimun values of a keyword
    minOfRange = min([row[i] for row in rows.values() for i in properties.keys()])
    maxOfRange = max([row[i] for row in rows.values() for i in properties.keys()])
    # creating random centroids
    centroids = [({item:random.randint(minOfRange, maxOfRange) for item in properties.keys()}) for i in range(k)]
    lastMatches = None
    for i in range(100):
        print("Iteration: ", i)
        # array of array to hold cluster
        bestMatches = [[] for i in range(k)]
        # calculating each centroid distance with a row and assigning a row to centroid which is closer
        for key_company, value_company in rows.items():
            bestMatch = 0;
            for j in range(k):
                d = distance_score(value_company, centroids[j])
                # centroid and row are more closer if d is higher than last match
                if(d > distance_score(value_company, centroids[bestMatch])):
                    bestMatch = j
            # appending company name to centroid which is closest to company
            bestMatches[bestMatch].append(key_company)

        # if no change in previous calculation and current calculation means we have got our results
        if(bestMatches == lastMatches):
            break;
        lastMatches = bestMatches

        # moving centroid to average position
        for i_centroid in range(len(centroids)):
            rowsOfCentroid = bestMatches[i_centroid]
            # creating average data for each centroid
            centroids[i_centroid] = {};
            for row in rowsOfCentroid:
                row_data = rows[row]
                for property in properties:
                    centroids[i_centroid].setdefault(property, 0)
                    centroids[i_centroid][property] += row_data[property]
            # getting average of each property by deviding it by number of rows
            for property in properties:
                centroids[i_centroid][property] = centroids[i_centroid][property]/len(rowsOfCentroid) if len(rowsOfCentroid) > 0 else 0

    return lastMatches

def getCompaniesMatrix():
    loaded_json = json.load(open("output.json"))
    return loaded_json

results = kClusterCreate(getCompaniesMatrix(), 4)
fileName = "company-k-cluster.json"
file = open(fileName, "w")
json.dump(results, file)

