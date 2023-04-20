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

## Wishlist 
1. A metadata tag for mis-phased scaffolds such that they don't have to be manually removed by name
2. Painting both haplotypes and generating an AGP for each instead of one AGP - may be complicated by the unpainted scaffolds 


## FAQ
1. Why won't my PretextMap open in PretextView?

> Hi-res PretextMaps likely require an HPC to generate the map, but will also require a discrete GPU to open the map in PretextView because it requires 16GB of RAM (i./e/ Macbooks with the M1 chip will have this capacity).
