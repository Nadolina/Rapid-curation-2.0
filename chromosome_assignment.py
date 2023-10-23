## For the modification of scaffold names to reflect chromosomal assignment. 

import csv
import sys 
import re
from Bio import SeqIO, Seq
from Bio.SeqRecord import SeqRecord


#FUNCTIONS ----

def sex_chr_asn(sex_chr,chr_name): 
    if 'unloc' not in record.id: 
        if sex_chr!=record.id: 
            exit
        else:
            inter_chr_dict[record.id]=((record.id).replace(sex_chr,chr_name))
            record.id=((record.id).replace(sex_chr,chr_name))
    if 'unloc' in record.id:
        if re.sub("_unloc_\d+$","",record.id) == sex_chr:
            inter_chr_dict[record.id]=((record.id)).replace(sex_chr,chr_name)
            record.id=((record.id).replace(sex_chr,chr_name))
        else:
            exit

#MAIN ----

outdir=sys.argv[1]
hap_agp=outdir + "/hap.unlocs.no_hapdups.agp"
hap_sort=outdir + "/hap.sorted.fa"

agp_lines=[]
with open(hap_agp) as file:
    agp = csv.reader(file,delimiter='\t')
    for line in agp:
        agp_lines.append(line)

file.close()

x=0
unlocs_haps={}
chr_list=[]
X_chr=""
Y_chr=""
W_chr=""
Z_chr=""
sex_chr=[]

while x < (len(agp_lines)):
    line = agp_lines[x]
    if "#" in line[0]:
        x+=1 
        continue
    elif line[9]=="Painted" or line[8]=="proximity_ligation":
        if line[10]=="X":
            X_chr=line[0]
            sex_chr.append(line[0])
        elif line[10]=="Y":
            Y_chr=line[0]
            sex_chr.append(line[0])
        elif line[10]=="W":
            W_chr=line[0]
            sex_chr.append(line[0])
        elif line[10]=="Z":
            Z_chr=line[0]
            sex_chr.append(line[0])
        elif line[10]=="Unloc":
            orig_name=re.sub('_unloc_[0-9]+$','',line[0])
            unlocs_haps[line[0]]=orig_name
        else:
            chr_list.append(line[0])          
    x+=1 

chr_list_filter = set([chr for chr in chr_list if chr != X_chr and chr != Y_chr and chr != W_chr and chr != Z_chr])

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
        elif X_chr in record.id and X_chr != "":
            sex_chr_asn(X_chr,"SUPER_X")
        elif Y_chr in record.id and Y_chr != "":
            sex_chr_asn(Y_chr,"SUPER_Y")
        elif W_chr in record.id and W_chr !="":
            sex_chr_asn(W_chr,"SUPER_W")
        elif Z_chr in record.id and Z_chr !="":
            sex_chr_asn(Z_chr,"SUPER_Z")
        elif record.id in unlocs_haps:
            orig_name=unlocs_haps[record.id]
            super_name=inter_chr_dict[orig_name]
            inter_chr_dict[record.id]=re.sub(orig_name,super_name,record.id)
            record.id=(re.sub(orig_name,super_name,record.id))

        new_records.append(SeqRecord(record.seq,id=record.id, description=""))

print (inter_chr_dict)


with open((outdir+"/inter_chr.tsv"),'w') as file: 
    for key in inter_chr_dict.keys():
        file.write("%s\t%s\n"%(key,inter_chr_dict[key]))
    file.close()

# with open((outdir+"/chromosomes.csv")) as file2:
# for value in inter_chr_dict.values():
#     print (value)


handle=open((outdir+"/hap.chr_level.fa"),"w")
SeqIO.write(new_records,handle,"fasta")
handle.close()
    



