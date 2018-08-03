#importing required packages
import sys
import math
sys.path.append('Data')    #path where OnlineMusic file is stored
from OnlineMusic import online_music
from OnlineMusic import transform_dataset

#function calculates distance start
def euclidean_distnce(music_data, person1, person2):
    common_item = {}
    #common buy in person1 and person2
    for item in music_data[person1]:
        if item in music_data[person2]:
            common_item[item] = True

    #if no item is common
    if len(common_item) == 0: return 0

    #calculate distance
    #?((x1-x2)^2 + (y1-y2)^2)
    distance = sum([math.pow(music_data[person1][itm] - music_data[person2][itm], 2) for itm in common_item.keys()])
    distance = math.sqrt(distance)
    #return result
    return 1/(distance + 1)



x = transform_dataset(online_music);
similarities = [(euclidean_distnce(x, 'Taylor Swift', other), other) for other in x.keys() if 'Taylor Swift' != other]
similarities.sort()
similarities.reverse()



def calculateSimilarItems(music_data, n=2):   #n is how many top similar items to store
	result = {}
	music_data_reverse = transform_dataset(music_data)   #transforms dataset to item centric
	for item in music_data_reverse.keys():
		#finding distance score of all other items with respect to current item
		similarities = [(euclidean_distnce(music_data_reverse, item, other), other) for other in x.keys() if item != other] 
		similarities.sort()
		similarities.reverse()   #top scores first
		result[item] = similarities[0:n]   #taking only top 2 items and storing in result
	return result
	
print(calculateSimilarItems(online_music))