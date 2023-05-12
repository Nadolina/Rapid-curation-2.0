## For the modification of scaffold names to reflect chromosomal assignment. 

import csv
import sys 
from Bio import SeqIO, Seq
from Bio.SeqRecord import SeqRecord

corr_agp="corrected.agp"
hap_sort="hap.sorted.fa"

agp_lines=[]
with open(corr_agp) as file:
    agp = csv.reader(file,delimiter='\t')
    for line in agp:
        agp_lines.append(line)

file.close()

x=0
unlocs_haps=[]
chr_list=[]
X_chr=""
Y_chr=""
W_chr=""
Z_chr=""
sex_chrs=[X_chr,Y_chr,W_chr,Z_chr]

while x < (len(agp_lines)):
    line = agp_lines[x]
    if "#" in line[0]:
        x+=1 
        continue
    elif line[-2]=="X":
        X_chr=line[0]
    elif line[-2]=="Y":
        Y_chr=line[0]
    elif line[-2]=="W":
        W_chr=line[0]
    elif line[-2]=="Z":
        Z_chr=line[0]
    elif line[-1]=="Painted" or line[-1]=="proximity_ligation":
        chr_list.append(line[0])
    elif line[-2]=="Unloc":
        chr_list.append(line[0]+"_unloc")
        
    x+=1 ## I feel like we just need to make this chunk into a function and repeat it for X/Y/Z/W (the redundancy is bothering me).

chr_list_filter = [chr for chr in chr_list if chr != X_chr and chr != Y_chr and chr != W_chr and chr != Z_chr]

print ([chr for chr in chr_list_filter])


scaff_num=1
new_records=[]
inter_chr_dict={}
with open(hap_sort) as original:
    records = SeqIO.parse(original, 'fasta')
    for record in records:
        if record.id in chr_list_filter:
            inter_chr_dict[record.id]=("SUPER_"+str(scaff_num))
            record.id=("SUPER_"+str(scaff_num))
            scaff_num += 1
        elif record.id==X_chr:
            inter_chr_dict[record.id]="SUPER_X"
            record.id="SUPER_X"
        elif record.id==Y_chr:
            inter_chr_dict[record.id]="SUPER_Y"
            record.id="SUPER_Y"
        elif record.id==W_chr:
            inter_chr_dict[record.id]="SUPER_W"
            record.id="SUPER_W"
        elif record.id==Z_chr:
            inter_chr_dict[record.id]="SUPER_Z"
            record.id="SUPER_Z"
        new_records.append(SeqRecord(record.seq,id=record.id, description=""))

with open("inter_chr.tsv",'w') as file: 
    for key in inter_chr_dict.keys():
        file.write("%s\t%s\n"%(key,inter_chr_dict[key]))
    file.close()


handle=open("hap.chr_level.fa","w")
SeqIO.write(new_records,handle,"fasta")
handle.close()
    



