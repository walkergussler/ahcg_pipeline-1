#github stuff
www.github.com/
sign in/make an account
git clone https://github.com/shashidhar22/ahcg_pipeline #clones base repository - gives Trimmomatic, Bowtie, Picard, and GATK

#actual stuff
download virtualbox as well as .ova file for virtual box system
https://da1s119xsxmu0.cloudfront.net/sites/developer/native/nativeappsvm/BaseSpace%20Native%20App%20VM%20(phix%20only)%20v9.ova
https://www.virtualbox.org/wiki/Downloads
https://developer.basespace.illumina.com/docs/content/documentation/native-apps/setup-dev-environment
install virtualboxin the virtualbox window, select file -> Import Appliance
use the .ova file as your appliance
login: vagrant 
password: vagrant
open putty
log into vagrant@localhost, user/pass=vagrant, port=2222
sudo apt-get update
sudo apt-get install unzip
sudo apt-get install samtools
sudo apt-get install git
sudo apt-get install openjdk-7-jre-headless 
sudo apt-get install bedtools
git clone https://github.com/shashidhar22/ahcg_pipeline
(already had python)
wget ftp://ftp-trace.ncbi.nih.gov/giab/ftp/data/NA12878/Garvan_NA12878_HG001_HiSeq_Exome/NIST7035_TAAGGCGA_L001_R1_001.fastq.gz
wget ftp://ftp-trace.ncbi.nih.gov/giab/ftp/data/NA12878/Garvan_NA12878_HG001_HiSeq_Exome/NIST7035_TAAGGCGA_L001_R2_001.fastq.gz
gunzip NIST7035_TAAGGCGA_L001_R1_001.fastq.gz
gunzip NIST7035_TAAGGCGA_L001_R2_001.fastq.gz
head -100000 NIST7035_TAAGGCGA_L001_R1_001.fastq > test_r1.fastq
head -100000 NIST7035_TAAGGCGA_L001_R2_001.fastq > test_r2.fastq
wget www.prism.gatech.edu/~sravishankar9/resources.tar.gz
tar -zxvf resources.tar.gz
gunzip dbsnp_138.hg19.vcf.gz
Samtools faidx hg19.fa
got circulating bowtie files in the interest of time, can be built with the following
bowtie2-build -f hg19.fa hg19
java -jar picard.jar CreateSequenceDictionary R=hg19.fa O=hg19.dict
#it is important that all three hg19 files be kept in the same directory, reads files and bowtie references should be in the same directory as the python program

Direct the pipeline properly, e.g.:
python ahcg_pipeline.py -t lib/Trimmomatic-0.36/trimmomatic-0.36.jar -b lib/bowtie2-2.2.9/bowtie2 -p lib/picard.jar -g lib/GenomeAnalysisTK.jar -i test_r1.fastq test_r2.fastq -w hg19 -d resources/dbsnp/dbsnp_138.hg19.vcf -r resources/genome/hg19.fa -a lib/Trimmomatic-0.36/adapters/TruSeq3-PE.fa -o out/

#Java installation workflow:
https://docs.oracle.com/javase/8/docs/technotes/guides/install/linux_jre.html#CFHIEGAA

#fork?
fork repository into my own repository
update .git/config to change user
update .gitignore file to exclude all the files we don't want to track
git config --global user.email 'email@domain.edu'
git config --global user.name 'name'
git commit -m 'message here'
git push origin master
#brca stuff -most common one, has all the exons we care about


#getting BRCA1 fasta 
wget http://vannberg.biology.gatech.edu/data/ahcg2016/reference_genome/hg19_refGene.txt
grep BRCA1 hg19_refGene.txt
use last one
convert 23 part block list into 23 line bed file
	python script 
use getfasta to obtain fasta file from appropriately designed bed file: http://bedtools.readthedocs.io/en/latest/content/tools/getfasta.html
bedtools getfasta -s -fo results.fa -fi hg19.fa -bed brca1.bed

wget http://vannberg.biology.gatech.edu/data/ahcg2016/fq/NA12878_brca_r{1,2}.fastq
samtools view -L <bed file> -b -o <output bam> <input bam>
bedtools bamtofastq -i <bam file> -fq <fastq r1> <fastq r2>

 
