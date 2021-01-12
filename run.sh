#!/bin/basg
bam=$1
ref=$2
STICresult=$3
FREECresult=$4

samtools sort $bam tumor.sort
samtools mpileup -f $ref tumor.sort.bam > tumor.pileup

python svmSomatic.py $STICresult $FREECresult




