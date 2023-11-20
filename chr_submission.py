
import csv
import sys
from Bio import SeqIO, Seq
from Bio.SeqRecord import SeqRecord

cur_fasta=sys.argv[1]

supers=[]
with open(cur_fasta) as file:
    records = SeqIO.parse(file, 'fasta')
    for record in records:
        if "SUPER" in record.id:
            supers.append(record.id)
file.close()

for line in supers:
    chr_num=(line.split("_"))[1]
    if "unloc" in line:
        print (line+","+chr_num+",no")
    else:
        print (line+","+chr_num+",yes")

        
        