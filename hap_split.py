## for splitting the haplotypes
## After AGPcorrect but prior to unloc assignment 

import csv 
import pandas as pd



corr="corrected.agp"

header=[]
agp_lines=[]
with open(corr) as file:
    agp = csv.reader(file,delimiter='\t')
    for line in agp:
        if "#" in line[0]:
            header.append(line)
        else: 
            agp_lines.append(line)
file.close()


current_hap=''
current_scaff=''
H1_lines=[]
H2_lines=[]
for line in agp_lines:
    
    if 'proximity_ligation' in line or 'Painted' in line:
        if 'Hap_1' in line:
            H1_lines.append(line)
            current_hap='Hap_1'
        elif 'Hap_2' in line: 
            H2_lines.append(line)
            current_hap='Hap_2'
        elif current_hap=='Hap_1':
            H1_lines.append(line)
        elif current_hap=='Hap_2':
            H2_lines.append(line)
    else:
        if 'H1' in line[5]:
            H1_lines.append(line)
        elif 'H2' in line[5]:
            H2_lines.append(line)


with open ('Hap_1/hap.agp','w',newline='\n') as file1:
    writer=csv.writer(file1,delimiter='\t')
    writer.writerows(header)
    writer.writerows(H1_lines)
file1.close()

with open ('Hap_2/hap.agp', 'w', newline='\n') as file2:
    writer=csv.writer(file2,delimiter='\t')
    writer.writerows(header)
    writer.writerows(H2_lines)
file2.close()
