#!/usr/bin/env python
import sys
import os
import argparse


parser = argparse.ArgumentParser(description="this program uses your hg19_refGene.txt and 2 vcf files to make a merged vcf file with regions of interest from a list of given genes")
parser.add_argument('-a','--vcf1', type=str,required=True, help="Your first vcf file to be compared")
parser.add_argument('-b','--vcf2', type=str,required=True, help="Your second vcf file to be compared")
parser.add_argument('-g','--genelist', type=str,required=True, help="Name of file with list of genes of interest: needs to have NM numbers in 2nd column")
parser.add_argument('-o','--output', type=str,default="output.vcf", help="Name of output file")

args = parser.parse_args()

vcf1=args.vcf1
vcf2=args.vcf2
genelist=args.genelist
out=args.output

makebed="python hg19-2-bed.py "+genelist+" hg19_refGene.txt interest.bed"
firstcut="bedtools intersect -header -wa -a "+vcf1+" -b interest.bed > foundVariants1.vcf"
secondcut="bedtools intersect -header -wa -a "+vcf2+" -b interest.bed > foundVariants2.vcf"
merg="bedtools intersect -header -a foundVariants1.vcf -b foundVariants2.vcf > "+out
print("making a bed file from your genelist and hg19_refGene.txt")
os.system(makebed)
print("taking subset of your first vcf in the region of interest")
os.system(firstcut)
print("taking subset of your second vcf in the region of interest")
os.system(secondcut)
print("intersecting your vcf files")
os.system(merg)
