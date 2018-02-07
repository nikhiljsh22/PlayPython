import sys
import math
sys.path.append('/playpython/Data')
from recommendations import critics

def sim_pearson(perfs, person1, person2):
    si = {}
    for item in perfs[person1]:
        if item in perfs[person2]:
            si[item] = 1

    n = len(si)
    if n == 0:
        return 0

    #calculating sum
    sum1 = sum([perfs[person1][it] for it in si])
    sum2 = sum([perfs[person2][it] for it in si])

    #calculating sum of squares
    sumSq1 = sum([pow(perfs[person1][it], 2) for it in si])
    sumSq2 = sum([pow(perfs[person2][it], 2) for it in si])

    #calculate sum of products
    sumPr = sum([perfs[person1][it] * perfs[person2][it] for it in si])

    #calculate person score
    num = sumPr - (sum1*sum2/n)
    den = math.sqrt((sumSq1-pow(sum1, 2)/n)*(sumSq2 - pow(sum2, 2)/n))
    if(den == 0):
        return 0
    r = num/den
    return r

print(sim_pearson(critics, 'Lisa Rose', 'Gene Seymour'))


def topMatches(perfs, person, n, similirity=sim_pearson):
    scores = [(similirity(perfs, person, other), other) for other in perfs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

print(topMatches(critics,'Toby', n=3))

