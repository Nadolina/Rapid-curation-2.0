#!/bin/sh 

fasta=""
agpfile=""

Help()
{
    # Display help

    echo "Command: sh curation_2.0_pipe.sh -f <original fasta> -a <agp> <options>"
    echo "-h Prints help."
}

while getopts ":hf:a:" option; do
    case $option in 
        h) #display Help
            Help
            exit;;
        f) #Pass original fasta file 
            fasta=$OPTARG;;
        a) #Pass Pretext generated AGP file of curated assembly
            agpfile=$OPTARG;;
    esac
done


printf "Original assembly: ${fasta}\n"
printf "PretextView generated AGP: ${agpfile}\n"

agpcorr_file=`echo $agpfile | sed 's/agp/corrected.agp/g'`

## TO-DO: modify agpcorrect.py to output to a file rather than to stdout
python3 AGPcorrect.py ${fasta} ${agpfile}





