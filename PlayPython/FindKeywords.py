import json
import sys
import re
import operator
sys.path.append('Data')

class USCompaniesWordVector:
    def __init__(self, us_companies_data):
        self.us_companies_data = us_companies_data

    def clusterCompaniesInCategories(self):
        globalCount = {}
        companyWordCount = {}
        for i in range(0, len(self.us_companies_data["data"])):   #looping through companies
            company_name = self.us_companies_data["data"][i]["company_name"]
            description = self.us_companies_data["data"][i]["description"]
            revenue_source = self.us_companies_data["data"][i]["revenue_source"]
            description_short = self.us_companies_data["data"][i]["description_short"]
            #getting words from descriptin, discription_short and revenue_source
            wc = self.getWordsFromDescription(description + " " + description_short + " " + revenue_source)
            companyWordCount[company_name] = wc
            #Creating word list from all companies data
            for word,count in wc.items():
                globalCount.setdefault(word, 0)
                if count > 1:
                    globalCount[word] += 1   #if word count > 1 increasing it's count

        wordList = []  #filtered Words, eliminated words like A, the, in etc
        for word, count in globalCount.items():
            #fraction is average count of word per company
            fraction = float(count) / len(self.us_companies_data["data"])
            #selecting average count from 6% to 20% as well eliminating words up to 3 charactors
            if(fraction > 0.06 and fraction < 0.20 and len(word) > 3): wordList.append(word)

        #creating output JSON file(word vector)
        fileName = "output.json"
        file = open(fileName, "w")
        jsonObj = {}
        for company,words in companyWordCount.items():
            jsonObj.setdefault(company, {})
            for word in wordList:
                jsonObj[company][word] = 0
                if word in words:
                    jsonObj[company][word] += words[word]

            data = [(key) for key in jsonObj[company].keys() if jsonObj[company][key] > 0]
        json.dump(jsonObj, file)
        print("Created file " + fileName)


    def getWordsFromDescription(self, description):
        wc = {}  #list of words with count
        words = self.getWords(description)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1; 
        return wc

    def getWords(self, text):
        txt = re.compile(r'<[^>]+>').sub('', text)
        words = re.compile(r'[^A-Z^a-z]+').split(txt)
        return [word.lower() for word in words if word != '']



loaded_json = json.load(open("data/USCompaniesData.json"))
usCmpny = USCompaniesWordVector(loaded_json)
usCmpny.clusterCompaniesInCategories()

