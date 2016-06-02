#This script converts the output of Kraken translate to the RDP file format accepted by Krona Tools.
#To call the program, type "python rename_Kraken_output_for_Krona.py <Kraken_file>"
#Rebecca Dikow 2016

import fileinput
import re

for line in fileinput.input():    
    line = re.sub(r'root',r'\troot', line.rstrip())
    line = re.sub(r'd__',r'\t\tRoot\trootrank\t1.0\tdomain\t1.0\t', line.rstrip())
    line = re.sub(r'\|p__',r'\tphylum\t1.0\t', line.rstrip())
    line = re.sub(r'\|c__',r'\tclass\t1.0\t', line.rstrip())
    line = re.sub(r'\|o__',r'\torder\t1.0\t', line.rstrip())
    line = re.sub(r'\|f__',r'\tfamily\t1.0\t', line.rstrip())
    line = re.sub(r'\|g__',r'\tgenus\t1.0\t', line.rstrip())
    line = re.sub(r'\|s__',r'\tspecies \t 1.0\t', line.rstrip())
    line = re.sub(r'Viruses',r'"Viruses"', line.rstrip())
    line = re.sub(r'Archaea',r'"Archaea"', line.rstrip())
    line = re.sub(r'Bacteria',r'"Bacteria"', line.rstrip())
    print(line)