
import csv 
import sys

stdout_file=sys.stdout

former=[]
new=[]
filename="inter.chr.tsv"
fasta="rCycPin1.HiC.hap_2.agp_corrected.sorted.fa"

with open(filename) as file:
    inter = csv.reader(file, delimiter='\t')
    for line in inter:
        former.append(line[0])
        new.append(line[1])
file.close()

sys.stdout = open('name_change_commands.sh', 'w')

n=0
while n < (len(former)+1):
    #print (former[n], new[n])
    if n==0:
        print ("#!/bin/sh\n")
        print ("outfasta=`echo %s | sed 's/.fa/.chr_level.fa/g'`\n" % fasta)
        print ("sed 's/%1s\\b/%2s/g' %3s | \\" % (former[n],new[n],fasta))
    elif (new[n] != "n") & (new[n+1] != "n"):
        print ("\tsed 's/%1s\\b/%2s/g' | \\" % (former[n],new[n]))
    else:
        print ("\tsed 's/%1s\\b/%2s/g' > $outfasta" % (former[n],new[n]))
        break
    n+=1
    
sys.stdout.close()
sys.stdout = stdout_file