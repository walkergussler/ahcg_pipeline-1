#!/bin/bash
BASE=/home/vagrant/ahcg_pipeline
JAR=$BASE/lib/GenomeAnalysisTK.jar
REF=$BASE/resources/genome/hg19.fa
VARIANTS=$BASE/minh.vcf
HAPMAP=$BASE/resources/BUNDLE/hapmap_3.3.hg19.sites.vcf.gz
OMNI=$BASE/resources/BUNDLE/1000G_omni2.5.hg19.sites.vcf.gz
PHASE=$BASE/resources/BUNDLE/1000G_phase1.snps.high_confidence.hg19.sites.vcf.gz
DBSNP=$BASE/resources/dbsnp/dbsnp_138.hg19.vcf
java -Xmx4g -jar $JAR \
-T VariantRecalibrator \
-R $REF \
-input $VARIANTS \
-resource:hapmap,known=false,training=true,truth=true,prior=15.0 $HAPMAP \
-resource:omni,known=false,training=true,truth=false,prior=12.0 $OMNI \
-resource:1000G,known=false,training=true,truth=false,prior=10.0 $PHASE \
-resource:dbsnp,known=true,training=false,truth=false,prior=2.0 $DBSNP \
-an DP \
-an QD \
-an FS \
-an SOR \
-an MQ \
-an MQRankSum \
-an ReadPosRankSum \
-mode SNP \
-recalFile output.recal \
-tranchesFile output.tranches \-rscriptFile output.plots.R