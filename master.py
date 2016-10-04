#!/usr/bin/python
import os
import sys

#usage: python master.py <vcf input file 1> <vcf input file 2> <output file name>
vcf1=sys.argv[1]
vcf2=sys.argv[2]

first="python makeSmallVcf.py "+vcf1+" hg19_refGene.txt our_output.vcf tmp.bed"
second="python makeSmallVcf.py "+vcf2+" hg19_refGene.txt GIAB_output.vcf tmp.bed"
print("Parsing your first vcf file")
os.system(first)
print("Parsing your second vcf file")
os.system(second)
firstlist=[]
secondlist=[]
firsthead=[]
secondhead=[]

f=open(vcf1,"r")
lines=f.readlines()
f.close()
for line in lines:
	if line.startswith("#"):
		firsthead.append(line)

f=open(vcf2,"r")
lines=f.readlines()
f.close()
for line in vcf2:
	if line.startswith("#"):
		secondhead.append(line)

f=open("our_output.vcf","r")
lines=f.readlines()
f.close()
for line in lines:
	firstlist.append(line)

f=open("GIAB_output.vcf","r")
lines=f.readlines()
f.close()
for line in lines:
	secondlist.append(line)

f=open("vcf1.vcf","w")
for line in firsthead:
	f.write(line)
for line in firstlist:
	f.write(line)
f.close()

f=open("vcf2.vcf","w")
for line in secondhead:
	f.write(line)
for line in secondlist:
	f.write(line)
f.close()

ibed="intersectBed -a vcf1.vcf -b vcf2.vcf -header"
os.system(ibed)
