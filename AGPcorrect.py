#!/usr/bin/env python3

import sys
import gzip
from Bio import SeqIO
from binascii import hexlify

if len(sys.argv) == 1 or (sys.argv[1] in ("-h", "--help")):
    print(
        "Usage: AGPCorrect ref.fa(.gz) scaffs.agp >corrected_scaffs.agp",
        file=sys.stderr,
    )
    sys.exit(0)

if len(sys.argv) != 3:
    sys.exit("Usage: AGPCorrect ref.fa(.gz) scaffs.agp >corrected_scaffs.agp")


def Open(file_name):
    with open(file_name, "rb") as f:
        isgzip = hexlify(f.read(2)) == b"1f8b"
    return gzip.open(file_name, "rt") if isgzip else open(file_name, "r")


print("Reading fasta...", file=sys.stderr)
with Open(sys.argv[1]) as f:
    seqs = {seq.id: len(seq) for seq in SeqIO.parse(f, "fasta")}
# print(
#     f"Read fasta, {len(seqs)} sequences",
#     *(f"{s}: {n} bp" for s, n in seqs.items()),
#     "\n",
#     file=sys.stderr,
#     sep="\n",
# )

seen = {}
with open(sys.argv[2], "r") as f:
    for line in f:
        if not line.startswith("#"):
            line = line.split("\t")
            if line[4] == "W":
                #seen[line[-4]] = max(seen.setdefault(line[-4], 0), int(line[-2]))
                # print (line)
                # print (line [5], line[7])
                seen[line[5]] = max(seen.setdefault(line[5],0), int(line[7]))
                
with open(sys.argv[2], "r") as f:
    curr_scaff = None
    maxn = 1
    for line in f:
        line = line[:-1]
        if not line.startswith("#"):
            line = line.split("\t")
            if curr_scaff != line[0]: ## Okay this seems to be checking whether the current scaffold name matches the scaffold name in the previous line
            ## If the current scaffold name does not match the previous, then it print ths scaffold name and the "correction" (which I assume is the BP difference between the )
                # if curr_scaff:
                #     print(f"{curr_scaff}: {correct} bp correction", file=sys.stderr)
                curr_scaff = line[0]
                # print (line, curr_scaff, "<- AGP")
                correct = 0 # Where is this correct coming from? nvm it looks like its coming from the previous iteration of this loop? (line 65)

            line[1] = str(int(line[1]) + correct)

            if line[4] == "W" and ((this_l := int(line[7])) == seen[line[5]]):
                correct += (acc_l := seqs[line[5]]) - this_l ##seems like this is where we are getting negative values from - but it could be that the right "correction isn't matched with the right scaffold "
                # print (seqs[line[5]], line[5]) 
                # print (this_l, correct, '\n')
                ## Seqs is a dictionary of scaffolds and their lengths generated from the original fasta file 
                ## So line[5] is the name of the current scaffold and seqs[line[5]] goes to the dict and produces the true length of the scaffold 

                if int(line[6]) >= acc_l:  ##line[6] is the start position of each segment - seems to be checking whether the start position is greater than the actual length of the scaffold?
                    sys.exit(
                        "Error with line: {}\n{} > {}".format(
                            "\t".join(line), line[6], acc_l
                        )
                    )

                line[7] = str(acc_l)

            line[2] = str(int(line[2]) + correct)

            print("\t".join(line))
            maxn = max(maxn, int(line[0].split("_")[-1]))
        else:
            if line.startswith("# DESCRIPTION"):
                line += "\tModified by PretextView_AGPCorrect"
            print(line)

    # if curr_scaff:
    #     print(f"{curr_scaff}: {correct} bp correction", file=sys.stderr)

maxn += 1
print(
    *(
        "\t".join((f"Scaffold_{maxn + k}", "1", str(n), "1", "W", s, "1", str(n), "+")) ## also need to fix this line to account for the paint/sex chr info
        for k, (s, n) in enumerate(
            (s, n) for s, n in seqs.items() if s not in set(seen.keys())
        )
    ),
    sep="\n",
)
