# Rapid-curation-2.0
TPF-less rapid curation of genomes 

## Protocol: 

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

## Wishlist/operations to include 
1. A metadata tag for mis-phased scaffolds such that they don't have to be manually removed by name
2. Painting both haplotypes and generating an AGP for each instead of one AGP - may be complicated by the unpainted scaffolds 
3. The rapid-curation scripts replace 'Scaffold' with 'SUPER' for the painted chromosomes, and rename the X and Y as SUPER_X and SUPER_Y - we will need to  replicate this. It doesn't seem like the names can be changed in the AGP prior to imposing the corrected agp on a fasta to generate the final fasta - scaffolds that are joined appear to get lost as a result. 
4. The ability to open two pretextview windows, for comparison of pre-/post-curation maps. I fear my computer would promptly melt though. 
5. Need to sort the fasta before plotting pretextmap - gfastats <fasta> --sort ascending. This will require another file to track these movments. Perhaps just a GFA? Will require a renaming function in that case if we intend to keep to a gfa. 


## FAQ
1. Why won't my PretextMap open in PretextView?

> Hi-res PretextMaps likely require an HPC to generate the map, but will also require a discrete GPU to open the map in PretextView because it requires 16GB of RAM (i./e/ Macbooks with the M1 chip will have this capacity).
