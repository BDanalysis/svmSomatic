##Basic Environment

Linux operation system

Python3.6.0

##Depend Tools

[Bwa]

a. Download:

wget https://sourceforge.net/projects/bio-bwa/files/bwa-0.7.17.tar.bz2/download ./

b. Unzip the file:

$ tar -xvf bwa-0.7.17.tar.bz2

c. Add Bwa into profile

$ vim .bashrc

$ export Dir_Bwa/bwa-0.7.17:$PATH #Dir_Bwa is the abosulte directory of Bwa

$ source .bashrc

[SAMtools]

a. Download:

wget https://sourceforge.net/projects/samtools/files/samtools/1.7/samtools-1.7.tar.bz2/download ./

b. Unzip the file:

$ tar -xvf samtools-1.7.tar.bz2

c. Add SAMTools into profile:

$ vim .bashrc

$ export Dir_SAMtools/samtools-1.7:$PATH #Dir_SAMtools is the abosulte directory of SAMTools

$ source .bashrc


##svmSomatic

a. Download:

$ git clone https://github.com/BDanalysis/svmSomatic.git

b.Install:

This software can be used directly when the corresponding python environment is provided

##Extra Python Library
collections、re、sys

joblib 0.12.0

Numpy 1.15.4


##Usage of svmSomatic

[Input]

We need four files:
A BAM file of tumor,a reference sequence FASTA file, SNV result file and CNV result file.

SNV result file needs to have three columns, separated by tabs：
(1):Chromosome number
(2):SNV variant location
(3):Allele frequency

CNV result file needs to hanve five columns, separated by tabs:
(1):Chromosome number
(2):CNV mutation start position
(3):CNV mutation end position
(4):Copy number
(5):Variation type(gain or loss)


[Run]

Program execution command:
bash run.sh tumor.bam ref.fa STICresult.txt FREECresult.txt

The somatic mutations result is svmSomaticresult.txt

[Output] svmSomaticresult.txt has two columns:

(1) The position where the mutation occurred

(2) Label of variant site
