## For modifying the AGP to accomodate unlocalized pieces once in the haplotype-specific and corrected state. 
## and also to remove haplotig duplications from their origin haplotype - if they are painted it shouldn't be a problem to incorporate them into their correct haplotype. They just need to be removed from the original. 

import csv 
import pandas as pd
#import numpy as np

corr_agp="hap.agp"

header=[]
agp_lines=[]
with open(corr_agp) as file:
    agp = csv.reader(file,delimiter='\t')
    for line in agp:
        if "#" in line[0]:
            header.append(line)
        else: 
            agp_lines.append(line)
file.close()

maxlen=max([len(entry) for entry in agp_lines])

if maxlen < 11:
    ## Checking for presence of metadata tags - if no unlocs or haplotigs present, the script just generates a replicate agp and exits.
    print ("No metadata tags used. Are you sure there are no unlocs, haplotigs or sex chromosomes to label?")
    with open ('hap.unlocs.no_hapdups.agp','w',newline='\n') as f:
        writer=csv.writer(f,delimiter='\t')
        writer.writerows(header)
        writer.writerows(agp_lines)
    f.close() 
    exit()
elif maxlen == 11:
    agp_df=pd.DataFrame(agp_lines,columns=['chr','chr_start','chr_end','#_scaffs','W','scaff','scaff_start','scaff_end','ori','painted','tag'])
else:
    agp_df=pd.DataFrame(agp_lines,columns=['chr','chr_start','chr_end','#_scaffs','W','scaff','scaff_start','scaff_end','ori','painted','tag','blank'])

unlocs=(agp_df.index[agp_df['tag']=='Unloc']).to_list()


prox_lig_hap_ind=set()
scaffs_with_unlocs=[]
unloc_num=1
for index in unlocs: ##This assumes unlocs are placed at the end of scaffolds 
    scaff=(agp_df.iloc[index].to_list())[0]
    # scaff_lines=(agp_df.loc[agp_df['chr']==scaff])
    # ind_list=scaff_lines.index.to_list()
    # unlocs_inds_inter=list(set(ind_list).intersection(unlocs))
    agp_df.loc[index,'chr_start']=1
    agp_df.loc[index,'chr_end']=agp_df.loc[index,'scaff_end']
    if scaff in scaffs_with_unlocs:
        unloc_num+=1
        agp_df.loc[index,'chr']=agp_df.loc[index,'chr']+"_unloc_"+str(unloc_num)
    else:
        agp_df.loc[index,'chr']=agp_df.loc[index,'chr']+"_unloc_"+str(unloc_num)
        scaffs_with_unlocs.append(scaff)
    if (agp_df.loc[index-1,'ori']) == 'proximity_ligation':
        prox_lig_hap_ind.add(index-1)

haplotigs=(agp_df.index[agp_df['painted']=='Haplotig'])
prox_lig_hap_ind.update(haplotigs)
agp_df_mod=agp_df.drop(list(prox_lig_hap_ind))


with open ('hap.unlocs.no_hapdups.agp','w',newline='\n') as f:
    writer=csv.writer(f,delimiter='\t')
    writer.writerows(header)
    writer.writerows(agp_df_mod.values.tolist())
f.close()


#---------------------------------------------------


    # # I WAS TRYING TO CONFIGURE THIS CODE SUCH THAT UNLOCS CAN BE PLACED AT THE BEGINNING OR END BUT THERE IS A LOT OF FINAGLING INVOLVED THAT IS NOT PERTINENT RIGHT NOW. 
    # if any(ind >= index for ind in ind_list):
    #     print ("Unlocalized sequences at beginning of chromosome assignment.")
    #     if any(unloc != index and unloc in ind_list for unloc in unlocs):
    #         print ("Other unloc found")
    #         unlocs_inds_inter=list(set(ind_list).intersection(unlocs))
    #         index = max(unlocs_inds_inter)
    #         end_unloc_pos=scaff_lines.loc[index,'chr_end']
    #         print (scaff_lines)
    #         ind = index+2
    #         while ind < max(ind_list)+1:
    #             print (ind)
    #             print (agp_df.loc[ind])
    #             agp_df.at[ind,'chr_start']=(agp_df.at[ind,'chr_start']-end_unloc_pos)
    #             print (agp_df.loc[ind])


    #         unlocs.remove(index)
    # elif any(ind <= index for ind in ind_list):
    #     print ("Unlocalized sequences at end of chromosome assignment.")
    





