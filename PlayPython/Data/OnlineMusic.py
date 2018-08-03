online_music = {
    'Donald':{'Taylor Swift':3.5,'Rihanna':3.0,'Justin Bieber':4.0},
    'Chandler':{'Taylor Swift':3.0,'Rihanna':3.5,'Justin Bieber':4.5},
    'Ruby':{'Rihanna':5.0,'Justin Bieber':2.0,'Demi Lovato':3.5, 'MJ':3.0},
    'Zoya':{'Taylor Swift': 3.0, 'Rihanna':2.0, 'Justin Bieber':4.0,'Demi Lovato':3.0},
    'Sam': {'Rihanna':3.0, 'Justin Bieber':3.5, 'MJ':4.0},
    'Robert': {'Rihanna':1.0,'Justin Bieber':2.5,'Demi Lovato':2.5}
}

online_music_reverse = {
'Taylor Swift': {'Donald': 3.5, 'Chandler': 3.0, 'Zoya': 3.0},
'Rihanna': {'Donald': 3.0, 'Chandler': 3.5, 'Ruby': 5.0, 'Zoya': 2.0, 'Sam': 3.0, 'Robert': 1.0},
'Justin Bieber': {'Donald': 4.0, 'Chandler': 4.5, 'Ruby': 2.0, 'Zoya': 4.0, 'Sam': 3.5, 'Robert': 2.5},
'Demi Lovato': {'Ruby': 3.5, 'Zoya': 3.0, 'Robert': 2.5},
'MJ': {'Ruby': 3.0, 'Sam': 4.0}
}

def transform_dataset(data):
	result = {}
	for item in data.keys():   #item is person like 'Donald'
		for subitem in data[item].keys():    #subitem is actually item like 'Tylor Swift'
			result.setdefault(subitem, {})
			
			result[subitem][item] = data[item][subitem]    #swap between person and item
			
	return result