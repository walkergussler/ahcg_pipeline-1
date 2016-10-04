#!/usr/bin/python
import os
import sys

#usage: python master.py <vcf input file> <hg19_refgene.txt> <output file> <temporary bed file name>

def bedvariants(bed,variants):	
	#parse bed file
	f=open(bed,"r")
	lines=f.readlines()
	f.close()
	d=[]
	for line in lines:
		if len(line)<3:
			continue
		splitline=line.split("\t")
		d.append([splitline[0],int(splitline[1]),int(splitline[2].strip())])
	#parse vcf file
	f=open(variants,"r")
	lines=f.readlines()
	f.close()
	varlist=[]
	for line in lines:
		if line.startswith("#"):
			continue
		splitline=line.split("\t")
		for item in d:
			if item[0] in splitline[0] or splitline[0] in item[0]:
				if int(splitline[1])> item[1] and int(splitline[1])<item[2]:
					varlist.append(line)
	varset=set(varlist)
	return varset

def createbed(my_file):
	#list of targets
	target_list=['NM_032043','NM_007294','NM_000059','NM_004675','NM_001005862','NM_001080124','NM_000660','NM_000249','NM_000251','NM_000179','NM_000535','NM_002354','NM_000546','NM_000314','NM_000455','NM_004360','NM_024675','NM_001005735','NM_000044','NM_000051','NM_002485','NM_000465','NM_032043','NM_005732','NM_001164269','NM_058216','NM_002878']
	#buffer to add/subtract to end/start of cds
	buffer = 20
	#other variables
	coord_list = []
	init_start = 0
	current_start = 0
	current_end = 0
	text = ""
	revised_text = ""
	i = 1
	q = 1
	firstline = True
	with open(my_file) as f:
		the_text = f.readlines()
	#iterate through target list
	for target in target_list:
		for line in the_text:
			if target in line:
				splitline = line.split('\t')
				chrom = splitline[2]
				cds_start = splitline[6]
				cds_end = splitline[7]
				strand = splitline[3]
				coord_1 = splitline[9].strip()
				coord_2 = splitline[10].strip()
				all_coords = coord_1 + coord_2
		cds_s = int(cds_start)
		cds_e = int(cds_end)
		for coord in sorted(all_coords.split(',')):
			if coord.strip() == '':
				continue
			if i == 1:
				current_start = coord
				i = 2
				continue
			if i == 2:	
				current_end = coord
				i = 1
				text += chrom + "\t" + current_start + "\t" + current_end + "\n"
				continue
		#grab cds start and stop and replace start and end of gene coordinates with respective
		for line in text.split("\n"):
			if line.strip() != "":
				start = str(int(line.split("\t")[1])-buffer)
				stop = str(int(line.split("\t")[2])+buffer)
				chr = line.split("\t")[0]
				if cds_s > int(start) and cds_s < int(stop):
					revised_text += chr + "\t" + str(cds_s) + "\t" + stop + "\n"
					continue
				if cds_e > int(start) and cds_e < int(stop):
					revised_text += chr + "\t" + start + "\t" + str(cds_e) + "\n"
					break
				else:
					revised_text += chr + "\t" + start + "\t" + stop + "\n"		
	f=open(sys.argv[4],"w")
	for line in revised_text:
		f.write(line)
	
createbed(sys.argv[2])
varset=bedvariants(sys.argv[4],sys.argv[1])
f=open(sys.argv[2],"w")
for var in varset:
	f.write(var)
	
os.system("