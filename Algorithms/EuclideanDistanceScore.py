import sys
import math
sys.path.append('/playpython/Data')
from recommendations import critics
#print(critics)
print(critics['Lisa Rose'])
print(critics['Gene Seymour'])
def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    #print(si)
    if len(si) == 0:
        return 0
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])
    return 1/(sum_of_squares+1)

print(sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))
