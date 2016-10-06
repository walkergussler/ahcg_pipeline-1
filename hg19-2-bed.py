#!/usr/bin/python
import os
import sys

#usage: python <hg19-2-bed.py> <gene list> <hg19_refGene.txt> <output file>
#the gene list file needs to have NM numbers in the second column with no whitespace

def createbed(ref,out,genelist):
	#target_list=['NM_032043','NM_007294','NM_000059','NM_004675','NM_001005862','NM_001080124','NM_000660','NM_000249','NM_000251','NM_000179','NM_000535','NM_002354','NM_000546','NM_000314','NM_000455','NM_004360','NM_024675','NM_001005735','NM_000044','NM_000051','NM_002485','NM_000465','NM_032043','NM_005732','NM_001164269','NM_058216','NM_002878']
	target_list=genelist
	f=open(ref,"r")
	lines=f.readlines()
	f.close()
	f=open(out,"w")
	for line in lines:
		for target in target_list:
			if target in line:
				splitline=line.split("\t")
				starts=splitline[9]
				ends=splitline[10]
				startlist=starts.split(",")
				endlist=ends.split(",")			
				if len(endlist) != len(startlist):
					print("exon lists are of incompatible length, exiting.")
				for index in range(len(startlist)-1):
					st=int(startlist[index])-20
					en=int(endlist[index])+20
					wri=splitline[2]+"\t"+str(st)+"\t"+str(en)+"\n"
					f.write(wri)

def getgenes(inf):
	fline=0
	f=open(inf,"r")
	lines=f.readlines()
	f.close()
	glist=[]
	for line in lines:
		if fline==0:
			fline+=1
			continue
		splitline=line.split("\t")
		glist.append(splitline[1])
	return glist

print("getting your genes")
glist=getgenes(sys.argv[1])
print("creating your bed file from hg19_refgene.txt")
createbed(sys.argv[2],sys.argv[3])
