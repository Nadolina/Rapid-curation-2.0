# Rapid-curation-2.0
TPF-less rapid curation of genomes 

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

4. Curate both haplotypes simultaneously. The presence of both haplotypes can be especially useful for identifying sex and microchromosomes, as well as haplotig duplications (mis-phased sequences).
5. Tags: <br>
    * Create "Hap_1" and "Hap_2" tags in PretextView. These tags only need to be created once, PretextView will remember them in other curations. In the PretextView menu, click "Meta Data Tags" and type in the two tags as such: <br>
       <p align="center">
         <img width="400" alt="image" src="https://github.com/Nadolina/Rapid-curation-2.0/assets/73204272/ad08e8fa-9674-4f92-9699-8e1fc63ea48f"\>
         <img width="400" alt="image" src="https://github.com/Nadolina/Rapid-curation-2.0/assets/73204272/1d5e1812-b3d8-4c08-acf7-02a337f87cbd">
       </p>
       <br>
    * Teasing the haplotypes apart gets a little messy, especially if there are sequences moved between haplotypes (i.e./ a scaffold from Hap_1 assigned to a Hap_2 scaffold or vice versa). The unassigned scaffolds can be sorted by the H1 and H2 notations we added prior to mapping. However, we need to use the Hap_1 and Hap_2 tags we just created to sort the chromosomes. For each chromosome, assign the appropriate haplotype tag to the left most scaffold, as such: <br>
       <p align="center">
        <img width="400" height="300" alt="image" src="https://github.com/Nadolina/Rapid-curation-2.0/assets/73204272/1e2c4a3a-2b2c-4d74-8b8a-ae80228e90bc">
        <img width="400" height="300" alt="image" src="https://github.com/Nadolina/Rapid-curation-2.0/assets/73204272/a1531c9a-4159-41fd-8d48-9e78c7fa39d3">
       </p>
       <br>
    * Tag the sex chromosomes as per usual. The current VGP standard is to move the sex chromosomes into Hap_1, so make sure that any sex chromosomes are also tagged with the Hap_1 tag. <br>
    *  Tag any unlocalized sequences as "unloc". Place any unloc sequences at the end (right most side) of their chromosomal assignment. <br>
6. Once done, paint all the scaffolds (from both haplotypes) into chromosomes. The homologs will approximately alternate. With everything painted, generate your AGP. <br>
   
Post-curation:

7. Run the post-scripts. They are designed to process both haplotypes at once and will separate the haplotype files into two folders, "Hap_1 " and "Hap_2".
```
sh curation_2.0_pipe.sh -f <haplotype combined fasta> -a <PretextView generated agp> 
-h help
-f combined haplotype fasta
-a haplotype agp generated from pretextview

Example:
sh curation_2.0_pipe.sh -f rCycPin1.HiC.haps_combined.fasta -a rCycPin1.HiC.haps_combined.pretext.agp
```

8. Run a mashmap or nucmer, or some other brief alignment to doublecheck that Hap_2 chromosomes are in the same order and orientation as Hap_1. Adjust accordingly. 
9. (Suggested) Generate a pretext map for each haplotype to ensure it curated as anctipated.
10. SUCCESS!
  
## Outputs 

ADD THIS 
  
## Wishlist/operations to include 

- [ ] Generating the chromosome file that is necessary for NCBI submissions. Will need to be able to double check for unloc pieces. 
- [ ] Another program for automatically pushing the curated files to VGP S3.  
- [ ] Better way to parse multiple tags 
- [ ] More flexibility in placement of unlocs 
- [ ] Another post-processing script to quick-align and parse the results to adjust the order and orientation of Hap_2 chromosomes to match Hap_1.
- [ ] Script for checking for curation statistics; number of breaks, joins, etc. 

## FAQ
1. Why won't my PretextMap open in PretextView?

> Hi-res PretextMaps likely require an HPC to generate the map, but will also require a discrete GPU to open the map in PretextView because it requires 16GB of RAM (i./e/ Macbooks with the M1 chip will have this capacity).
  
2. Why aren't my unlocalized (unloc) sequences being named correctly?
  
> a. I (at this time) configured the pipeline to process unlocs placed at the end of their respective chromosome assignments. Processing unlocs placed at the beginning of the painted chromosome is more complicated, but is possible - time permitting I will go back and modify this in the future. For now ***place all unlocs at the right end of their painted chromosome***. <br>
> b. The unlocs also have to be painted. Double check to make sure they have been painted along with their assigned chromosome. 
