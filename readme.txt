## github account creation

www.github.com/
sign in/make an account
git clone https://github.com/shashidhar22/ahcg_pipeline #clones base repository - gives Trimmomatic, Bowtie, Picard, and GATK

## fork repository into my own repository

update .git/config to change user
update .gitignore file to exclude all the files we don't want to track
git config --global user.email 'email@domain.edu'
git config --global user.name 'name'
git commit -m 'message here'
git push origin master

## adding changes to github

```{sh}
git add file_name
git rm file_name (as needed)
git commit -m 'commit message goes here'
git push origin master
```

## actual stuff

download virtualbox as well as .ova file for virtual box system
https://da1s119xsxmu0.cloudfront.net/sites/developer/native/nativeappsvm/BaseSpace%20Native%20App%20VM%20(phix%20only)%20v9.ova
https://www.virtualbox.org/wiki/Downloads
https://developer.basespace.illumina.com/docs/content/documentation/native-apps/setup-dev-environment
install virtualbox in the virtualbox window, select file -> Import Appliance
use the .ova file as your appliance
login: vagrant 
password: vagrant
open putty
log into vagrant@localhost, user/pass=vagrant, port=2222

## basic setup

```{sh}
sudo apt-get update
sudo apt-get install unzip
sudo apt-get install samtools
sudo apt-get install git
sudo apt-get install openjdk-7-jre-headless 
sudo apt-get install bedtools
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
bowtie2-build -f hg19.fa hg19
java -jar picard.jar CreateSequenceDictionary R=hg19.fa O=hg19.dict
```

#it is important that all three hg19 files be kept in the same directory, reads files and bowtie references should be in the same directory as the python program

Direct the pipeline properly, e.g.:

```{sh}
python ahcg_pipeline.py -t lib/Trimmomatic-0.36/trimmomatic-0.36.jar -b lib/bowtie2-2.2.9/bowtie2 -p lib/picard.jar -g lib/GenomeAnalysisTK.jar -i test_r1.fastq test_r2.fastq -w hg19 -d resources/dbsnp/dbsnp_138.hg19.vcf -r resources/genome/hg19.fa -a lib/Trimmomatic-0.36/adapters/TruSeq3-PE.fa -o out/
```

# Java installation workflow:

https://docs.oracle.com/javase/8/docs/technotes/guides/install/linux_jre.html#CFHIEGAA

## getting BRCA1 fasta 

```{sh}
wget http://vannberg.biology.gatech.edu/data/ahcg2016/reference_genome/hg19_refGene.txt
grep BRCA1 hg19_refGene.txt
```

use last one
convert 23 part block list into 23 line bed file
	python script 
use getfasta to obtain fasta file from appropriately designed bed file: http://bedtools.readthedocs.io/en/latest/content/tools/getfasta.html
bedtools getfasta -s -fo results.fa -fi hg19.fa -bed brca1.bed

wget http://vannberg.biology.gatech.edu/data/ahcg2016/fq/NA12878_brca_r{1,2}.fastq
samtools view -L <bed file> -b -o <output bam> <input bam>
bedtools bamtofastq -i <bam file> -fq <fastq r1> <fastq r2>

download various bam files from ncbi:

```{sh}
ftp://ftp-trace.ncbi.nih.gov/giab/ftp/data/NA12878/Garvan_NA12878_HG001_HiSeq_Exome/project.NIST_NIST7035_H7AP8ADXX_TAAGGCGA_1_NA12878.bwa.markDuplicates.bam
ftp://ftp-trace.ncbi.nih.gov/giab/ftp/data/NA12878/Garvan_NA12878_HG001_HiSeq_Exome/project.NIST_NIST7035_H7AP8ADXX_TAAGGCGA_2_NA12878.bwa.markDuplicates.bam
ftp://ftp-trace.ncbi.nih.gov/giab/ftp/data/NA12878/Garvan_NA12878_HG001_HiSeq_Exome/project.NIST_NIST7086_H7AP8ADXX_CGTACTAG_1_NA12878.bwa.markDuplicates.bam
ftp://ftp-trace.ncbi.nih.gov/giab/ftp/data/NA12878/Garvan_NA12878_HG001_HiSeq_Exome/project.NIST_NIST7086_H7AP8ADXX_CGTACTAG_2_NA12878.bwa.markDuplicates.bam

samtools merge output.bam <bam1> <bam2> <bam3> <bam4>
```

#to edit vcf files in which entries begin with '#' instead of 'chr#'
awk '{if($0 !~ /^#/) print "chr"$0; else print $0}' NA12878_GIAB.vcf > GIAB_goldStandard.vcf

#bedtools intersect is a useful tool to be able to combine a bed file with a vcf or with two vcf files
#to take a subset of a vcf file according to regions prescribed in a bed file, use a command like
bedtools intersect -header -wa -a variants.vcf -b cancerGenes.bed > foundVariants.vcf
#to combine two vcf files and take the intersection of the two, use 
bedtools intersect -header -a foundVariants.vcf -b goldCancerVariants.vcf > overlappingVariants.vcf 

we can use combineVCF-master.py to compare any two vcf files given a gene list

to get files for GATK resource bundle:
```{sh}
wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/2.8/hg19/hapmap_3.3.hg19.sites.vcf.gz
wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/2.8/hg19/1000G_omni2.5.hg19.sites.vcf.gz
wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/2.8/hg19/1000G_phase1.snps.high_confidence.hg19.sites.vcf.gz
wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/2.8/hg19/dbsnp_138.hg19.vcf.gz
```

With all 3 of these files, perform the following (example file called XXX)
gunzip XXX
bgzip XXX
tabix -p vcf XXX


# matching variants from vcf with clinical risks

```{sh}
python3 compare_clin_with_vcf.py final_variants_trimmed_and_interected.vcf BRCA1_brca_exchange_variants.csv BRCA2_brca_exchange_variants.csv \
| tee brca_clinical_xref.txt
grep -vi benign brca_clinical_xref.txt > brca_clinical_nonbenign_xref.txt
cat brca_clinical_nonbenign_xref.txt \
| awk 'BEGIN {FS="\t"} {
split($1, coord, ":")
printf("%s\t%s\t%s\t%s\n", coord[1], coord[2], coord[2], $2)}' \
| sed -E -e 's/^([^c].*)/chr\1/' > brca_clinical_nonbenign_xref.bed
```

# coverage calculator

```{sh}
grep 'NM_007298' bcoc_padded.bed > brca1.bed
samtools view -L brca1.bed data/project.NIST_NIST7035_H7AP8ADXX_TAAGGCGA_1_NA12878.bwa.markDuplicates.bam -b > new.bam
bedtools genomecov -ibam new.bam -bga na12878.bga.bed
bedtools intersect -split -a brca1.bed -b na12878.bga.bed -bed > brca1.final.bed
awk '{printf("%s\t%s\t%s\t%s\t%s\t%s\n",$1,$2,$3,$4,$10,$6)}' brca1.coverage_joined.bed > brca1.coverage_final.bed
bedtools intersect -a brca1.final.bed -b brca_clinical_nonbenign_xref.bed -wo > brca_clinical_nonbenign_final.bed
cat brca_clinical_nonbenign_final.bed | cut -f4,5,7,8,10
```