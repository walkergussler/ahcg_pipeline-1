Open up virtual box
Select basespace machine
Log in with username/password ‘basespace’
Once logged in and you get the ‘$’, you can start up putty
Use putty to connect to basespace@localhost:2222
Use password: basespace 
wget https://www.python.org/download/releases/3.4.1/
wget http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.36.zip
wget https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.2.9/
wget https://github.com/broadinstitute/picard/releases/download/2.6.0/picard.jar
wget https://software.broadinstitute.org/gatk/download/
sudo apt-get install unzip
unzip Trimmomatic-0.36.zip
unzip bowtie2-2.2.9.zip
Sudo apt-get install samtools
Samtools faidx hg19.fa
java -jar picard.jar CreateSequenceDictionary R=hg19.fa O=hg19.dict
^ it is important that all three hg19 files be kept in the same directory^
Sudo apt-get install openjdk-8-jre-headless
gunzip dbsnip_138.hg19.vcf.gz

reads files and bowtie references should be in the same directory as the python program

Direct the pipeline properly, e.g.:
python ahcg_pipeline.py -t lib/Trimmomatic-0.36/trimmomatic-0.36.jar -b lib/bowtie2-2.2.9/bowtie2 -p lib/picard.jar -g lib/GenomeAnalysisTK.jar -i r1.fastq r2.fastq -w hg19 -d resources/dbsnp/dbsnp_138.hg19.vcf -r resources/genome/hg19.fa -a lib/Trimmomatic-0.36/adapters/TruSeq3-PE.fa -o out/

Ran into error with the ordering of the contigs: says to reorder them in accordance with the reference. I attempted this, but it reordersam says it cannot reconcile the differences between he 2 files. There are about 20 contigs with strange names which arent found in the reference. I should've reached this point earlier so that I could've emailed someone before midnight on monday/tuesday. 

##### ERROR   reads contigs = [chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13, chr14, chr15, chr16, chr17, chr18, chr19, chr20, chr21, chr22, chrX, chrY, chrM, chr1_gl000191_random, chr1_gl000192_random, chr4_gl000193_random, chr4_gl000194_random, chr7_gl000195_random, chr8_gl000196_random, chr8_gl000197_random, chr9_gl000198_random, chr9_gl000199_random, chr9_gl000200_random, chr9_gl000201_random, chr11_gl000202_random, chr17_gl000203_random, chr17_gl000204_random, chr17_gl000205_random, chr17_gl000206_random, chr18_gl000207_random, chr19_gl000208_random, chr19_gl000209_random, chr21_gl000210_random, chrUn_gl000211, chrUn_gl000212, chrUn_gl000213, chrUn_gl000214, chrUn_gl000215, chrUn_gl000216, chrUn_gl000217, chrUn_gl000218, chrUn_gl000219, chrUn_gl000220, chrUn_gl000221, chrUn_gl000222, chrUn_gl000223, chrUn_gl000224, chrUn_gl000225, chrUn_gl000226, chrUn_gl000227, chrUn_gl000228, chrUn_gl000229, chrUn_gl000230, chrUn_gl000231, chrUn_gl000232, chrUn_gl000233, chrUn_gl000234, chrUn_gl000235, chrUn_gl000236, chrUn_gl000237, chrUn_gl000238, chrUn_gl000239, chrUn_gl000240, chrUn_gl000241, chrUn_gl000242, chrUn_gl000243, chrUn_gl000244, chrUn_gl000245, chrUn_gl000246, chrUn_gl000247, chrUn_gl000248, chrUn_gl000249]
##### ERROR   reference contigs = [chrM, chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13, chr14, chr15, chr16, chr17, chr18, chr19, chr20, chr21, chr22, chrX, chrY]

java -jar lib/picard.jar ReorderSam I=out/r1_trimmed_FM.bam O=reordered_FM.bam R=resources/genome/hg19.fa CREATE_INDEX=TRUE
New reference sequence does not contain a matching contig for chr1_gl000191_random
