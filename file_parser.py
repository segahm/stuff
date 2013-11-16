#!/usr/bin/python -tt
import csv
import re
import sys
import copy

def main():
    folder = "Excel Data"
    filename = "_1111_Data.csv"
    states = ['IL','IN','MI','OH']
    years = range(2009,2014,1)
    #CERT  NAMEFULL    BRNUM   RPT_YR  RSSDHCR DEPDOM  CITY2BR CNTYNUMB    DEPSUMBR
    cols = {'bank_id':4,'deposits':5,'name':1,'branch_deposits':8,'year':3}
    data = {}
    for state in states:
        data[state] = {}
        print 'state:',state
        for year in years:
            data[state][year] = {}
            print 'year:',year
            filename = re.sub(r"\d+", str(year), filename)
            file_str = folder+'/'+state+filename
            print 'opening file:', file_str
            with open(file_str) as csvfile:
                reader = csv.reader(csvfile)
                #header
                reader.next()
                #market wide statistics
                data[state][year]['total_deposits'] = 0
                top_banks = {1:['id',1],2:['id',1],3:['id',1]}
                for row in reader:
                    if "\n" not in row:
                        #save bank's statistics
                        id = row[cols['bank_id']]
                        #is this a new bank
                        if id in data[state][year]:
                            data[state][year][id]['branches'] += 1
                        else:
                            data[state][year][id] = {}
                            data[state][year][id]['branches'] = 1
                            data[state][year][id]['name'] = row[cols['name']]
                            deposit = int(row[cols['deposits']])
                            data[state][year][id]['deposits'] = deposit
                            #top 3 bank comparison
                            top_bank_i = 4
                            while top_bank_i > 1 and deposit > top_banks[top_bank_i-1][1]:
                                top_bank_i -= 1
                            if top_bank_i < 4:
                                top_banks[top_bank_i] = [id,deposit]
                            #update total for the year & state
                            data[state][year]['total_deposits'] += int(row[cols['deposits']])
                #mark top 3 banks
                if year == 2013:
                    data[state][year]['top_bank1'] = copy.copy(top_banks[1][0])
                    data[state][year]['top_bank2'] = copy.copy(top_banks[2][0])
                    data[state][year]['top_bank3'] = copy.copy(top_banks[3][0])
    
    for state in states:
        #annual statistics:
        id1 = data[state][2013]['top_bank1']
        id2 = data[state][2013]['top_bank2']
        id3 = data[state][2013]['top_bank3']
        print data[state][year][id1]['name'],' ',data[state][year][id2]['name'],' ',data[state][year][id3]['name']
        for year in years:
                print "%s, %d, %d, %d, %d" % (year,data[state][year][id1]['deposits'],
                           data[state][year][id2]['deposits'],
                           data[state][year][id3]['deposits'],
                           data[state][year]['total_deposits'])


if __name__ == '__main__':
    main()