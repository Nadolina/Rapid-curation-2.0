
import csv 

with open("corrected.agp") as file:
    agp = csv.reader(file, delimiter='\t')

    for line in agp:
        print (line)

file.close()