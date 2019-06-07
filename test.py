#!/usr/bin/python
# vim: set fileencoding=utf-8 :
import heapq
import csv
from tempfile import TemporaryFile
from itertools import islice

def extract_date(ligne):
    str_date = ligne.split(',')[0]
    return ''.join(str_date.split(',')[::-1])

sorted_temp_files = []

with open('Culture_BDD_V3.csv') as infile:
    #progress = 0
    while True:
        lines =[""]
        #lines = list(infile)

        for Line in infile:
           lines = lines.sort(key=extract_date)
        print(Line[0],Line[2])
       # print("{:.2f}%".format(progress))
        #progress += (100 /10 * 100)



        f = TemporaryFile(mode="r+")
        f.writelines(lines)


        f.seek(0)


        sorted_temp_files.append(f)


    with open('sorted_data.csv', 'w') as outfile:
        for ligne in heapq.merge(*sorted_temp_files, key=extract_date):
            outfile.write(ligne)