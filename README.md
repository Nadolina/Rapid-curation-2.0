# Rapid-curation-2.0
TPF-less rapid curation of genomes 

## Manual Protocol: 

1. Modify scaffold names to reflect origin haplotype (i.e./ H1.scaffold_1, H2.scaffold_1) 
2. Concatenate assemblies with modified scaffold names into a single fasta file; generate PretextMap
3. Curate higher contiguity haplotype within haplotype combined PretextMap; paint autosomes and sex chromosomes 
4. Generate AGP from PretextView 
5. Use AGPcorrect.py to correct the scaffold sizes in the AGP that were reduced to standardized texel sizes. 
```
python3 AGPcorrect.py <original fasta> <PrextView AGP> 
  ```
4. Separate haplotypes from corrected AGP 
```
grep -E '#|proximity_ligation|Painted|<haplotype identifier (H1, H2)>.scaffold|<XYZW>' <corrected AGP> > main_haplotype.agp 

grep <other hap identifier (H1, H2)> > other_haplotype.agp 
```
5. Relocate any misphased scaffolds (see wishlist item 1) 
    - create bed file of names of misphased scaffolds and pass to gfastats --exclude 
    - manually edit AGPs to move scaffolds 
6. Impose corrected AGP on original fasta 

```
gfastats <original haplotypes combined fasta> --agp-to-path <main haplotype corrected agp> -ofa 
```
7. Plot new PretextMap to ensure curation worked as anticipated. 

## Requirements

Biopython v1.81

gfastats v1.2.6 

pandas 

## Getting started 

Before curating: 

1. Decontaminate the haplotypic assemblies. 
2. Modify the names in the decontaminated assemblies; H1.scaffold_1 for hap1 and H2.scaffold_2. The post-scritps are designed to accept this H1 and H2 notation. 
3. Concatenate the assemblies into a single fasta; plot a pretext map. 

Curation:

4. Curate one haplotype at a time: <br>
    a. Label sex chromosomes, haplotigs and unlocs with metadata tags. Label any mis-phased scaffolds with the haplotig tag. <br>
    b. Paint the chromosomes for the main haplotype as well as sex chromosomes; generate an agp. Do not paint haplotigs, just leave them with metadata tags. <br>
    c. Remove the painting and curate the other haplotype. Keep in mind there may need to be haplotig tags removed from the first haplotype curation, or you may need to add tags. <br>
    d. Paint the second haplotype but do not include sex chromosomes. Generate a second AGP. 

Post-curation:

5. Run the post-scripts. You'll have to run this once for each haplotype using the same haplotype combined fasta, but with each agp once and their corresponding haplotype (ID'd by 1 or 2)
```
sh curation_2.0_pipe.sh -f <haplotype combined fasta> -a <haplotype agp> -p <haplotype in question 1 or 2> 
-h help
-f combined haplotype fasta
-a haplotype agp generated from pretextview
-p (p for primary) pass 1 for hap 1 and 2 for hap 2

Example:
sh curation_2.0_pipe.sh -f rCycPin1.HiC.haps_combined.fasta -a rCycPin1.HiC.haps_combined.pretext.agp_hap2 -p 2 
```
6. Generate a pretext map for each haplotype to ensure it curated as anctipated. 
  
## Outputs 

ADD THIS 
  
## Wishlist/operations to include 
1. A metadata tag for mis-phased scaffolds such that they don't have to be manually removed by name
2. Painting both haplotypes and generating an AGP for each instead of one AGP - may be complicated by the unpainted scaffolds 
3. The rapid-curation scripts replace 'Scaffold' with 'SUPER' for the painted chromosomes, and rename the X and Y as SUPER_X and SUPER_Y - we will need to  replicate this. It doesn't seem like the names can be changed in the AGP prior to imposing the corrected agp on a fasta to generate the final fasta - scaffolds that are joined appear to get lost as a result. DONE (Names are substituted at the fasta level and a tsv tracks this)
4. The ability to open two pretextview windows, for comparison of pre-/post-curation maps. I fear my computer would promptly melt though. 
5. Need to sort the fasta before plotting pretextmap - gfastats <fasta> --sort largest. This will require another file to track these movments. Perhaps just a GFA? Will require a renaming function in that case if we intend to keep to a gfa. DONE (performed with seqkit instead because it permits piping)
6. Generating the chromosome file that is necessary for NCBI submissions. Will need to be able to double check for unloc pieces. DONE.
7. Another program for automatically pushing the curated files to S3. 
8. Require an operation to remove haplotypic duplications - mind you, I don't know if this will be an issue in a dual curation setting? DONE. 
9. what does the agp look like with multiple tags/ modify to parse that


## FAQ
1. Why won't my PretextMap open in PretextView?

> Hi-res PretextMaps likely require an HPC to generate the map, but will also require a discrete GPU to open the map in PretextView because it requires 16GB of RAM (i./e/ Macbooks with the M1 chip will have this capacity).
  
2. Why aren't my unlocalized (unloc) sequences being named correctly?
  
> a. I (at this time) configured the pipeline to process unlocs placed at the end of their respective chromosome assignments. Processing unlocs placed at the beginning of the painted chromosome is more complicated, but is possible - time permitting I will go back and modify this in the future. For now ***place all unlocs at the right end of their painted chromosome***. <br>
> b. The unlocs also have to be painted. Double check to make sure they have been painted along with their assigned chromosome. 
