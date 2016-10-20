#!/bin/bash
BASE=/home/vagrant/ahcg_pipeline
JAR=$BASE/lib/GenomeAnalysisTK.jar
REF=$BASE/resources/genome/hg19.fa
VARIANTS=$BASE/minh.vcf
RECAL=$BASE/output.recal
TRANCH=$BASE/output.tranches
java -jar $JAR \
-T ApplyRecalibration \
-R $REF \
-input $VARIANTS \
-mode SNP \
--ts_filter_level 99.0 \
-recalFile $RECAL \
--tranches_file $TRANCH \
-o final_recal.vcf