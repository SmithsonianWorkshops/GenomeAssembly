Assembly Workshop Week 3: Monitoring assembly progress and troubleshooting errors  
---

Tutorial steps:  
1. Getting set on Hydra  
2. Troubleshooting errors  
3. Different ways to run MaSuRCA  
4. Find the assembly output files   
5. Run Paul's fasta metadata parser to get statistics  
6. Run Genomescope  

###1. Getting set on Hydra
* Login to Hydra (If you need assistance with Hydra, check the [support wiki](https://confluence.si.edu/display/HPC/High+Performance+Computing)).
* Change to your directory  
    + hint: `cd /pool/genomics/USERNAME` where *USERNAME* is your Hydra login name 
* Change to your workshop directory: e.g. ```cd assembly_tutorial```

###2. Troubleshooting errors
* I made a mistake last week with SPAdes: by default, it uses 16 threads. Please update your job files to include the following in the commands for SPAdes: 
```-t $NSLOTS```  

* What is ```$NSLOTS``` and why is it better than ```-t 12```?  

* Did anyone get a ```no suitable queues``` error when trying to submit a job with ```qsub```?  

* Help with parameters: head to ```/share/apps/bioinformatics``` to see all software installed. If you call up a program and include -h or -help, you will usually get a list of options, which can help you figure out what commands to run. The software manuals have this information as well. 
	+ Note: there is a huge range in documentation quality, and even quality in the kinds of errors you get.

* Let's try to tally up how much RAM everyone's assemblies used.
	+ If you know your JOBID, try ```qacct -j JOBID```

###3. Different ways to run MaSuRCA  
* Remember from last week that MaSuRCA has an issue where it grab all the CPUs on a node even when you request fewer. Remember, Hydra is a heterogeneous cluster where we have nodes with 12, 24, 40, and 64 CPUs each. Sylvain has defined these sets of nodes with N CPUs so that you can request a node with a certain number of CPUs. This is one way to get around the problem with MaSuRCA.  
	+  Instead of ```-q mThC.q```, you can do: ```-q mThC.q@@12c-hosts```  If you request 12 threads, the job scheduler will wait for a 12-CPU node to be free, then put your job there (and you will be the only one using it).  
* Sylvain also spent some time this week fixing MaSuRCA so it won't grab all the CPUs on a node. We think it should be OK to run now as is, without the above trick. But feel free to try it.
* Now, try submitting your MaSuRCA assembly. Create two job files as detailed in last week's tutorial.
* You can run a hybrid MaSuRCA assembly with both PacBio and Illumina data and also an Illumina-only assembly. Note that MaSuRCA on Illumina-only data uses a different (older) version of the Celera assembler than the hybrid assembly uses. You will need to remove two options from your config file in otder to run MaSuRCA on Illumina-only data:  
```utgGraphErrorRate=0.05``` and ```utgMergeErrorRate=0.05```

###4. Find the assembly output files
If you didn't complete all of the assemblies, you can use ```cp``` to copy the results from my directory (/pool/genomics/dikowr/assembly_tutorial) to yours:

* SPAdes Illumina only: ```SPAdes_Illumina_contigs.fasta```  
* SPAdes Hybrid: ```SPAdes_hybrid_contigs.fasta``` & ```SPAdes_hybrid_scaffold.fasta```  

* DISCOVAR: ```DISCOVAR_a.lines.fasta```  

* MaSuRCA Hybrid: ```MaSuRCA_hybrid_genome.ctg.fasta``` & ```MaSuRCA_hybrid_genome.scf.fasta```  
* MaSuRCA Illumina only: ```MaSuRCA_Illumina_genome.ctg.fasta```    

* Why are there scaffold files for some and not others?

* Locations of output files: 
	+ DISCOVAR: ```a.final/```  
	+ SPAdes: directly in the SPAdes output directory you specified  
	+ MaSuRCA: ```CA.../9-terminator/```  
	
###5. Run Paul's fasta metadata parser to get statistics
Paul wrote a python script to grab some statistics from contig and scaffold files. These are the stats:  

Total number of base pairs:    
Total number of contigs:   
N90:  
N80:  
N70:  
N60:  
N50:  
L90:  
L80:  
L70:  
L60:  
L50:  
GC content:  
Median contig size:  
Mean contig size:  
Longest contig is:  
Shortest contig is: 

* Create job files to run this script for each assembly file. There are 7 assembly files.  
	+ The script is here: ```/scratch/genomics/frandsenp/fasta_metadata_parser/fasta_meta_data_parser.py```
	+ Usage: ```python fasta_meta_data_parser.py <genome_filename> <statistics_output_name.txt>```  
	+ Module: ```bioinformatics/anaconda/2.2.0```

* Which is the "best" assembly?  
* Which is the "worst" assembly?
* Is there any variation across the class?  

* Some notes about DISCOVAR: You may notice that DISCOVAR produced a ton of contigs and a poor N50. Because it attempts to deal with multiple paths, bubbles in the graph, lots of these are output as separate contigs. There may be ways to deal with them, and we're interested to see the results of the w2rap-contigger, which we are currently testing, stay tuned until next week. Feel free to try it yourself! 
	+ [w2rap-contigger](https://github.com/bioinfologics/w2rap-contigger)
* DISCOVAR outputs a stats file, which has a different N50 than that generated by Paul's script. It's likely ignoring the small edges. Find this file and compare the N50s.  
* From the DISCOVAR manual:  
A DISCOVAR de novo assembly is a graph whose edges represent DNA sequences. Within any assembly one can find regions that are essentially linear. We call these lines.   
	+ a.fasta = fasta file of edges
	+ a.lines.fasta = standard scaffold fasta file, obtained by taking the highest coverage path through each cell; LOSES INFORMATION
	
![](http://www.broadinstitute.org/software/discovar/blog/wp-content/uploads/2014/08/line0.png)

* We can remove small contigs using bioawk:
	+ Module: bioinformatics/bioawk/0.0
	+ Command: ```bioawk -c fastx '{ if(length($seq) > 200) { print ">"$name; print $seq }}' <ORIGINAL.fasta> > <NEW.fasta>```
* Check how many contigs were removed.

###6. Run Genomescope

* Genomescope is a new program written by Mike Schatz's group that can be used to estimate genome size from short read data: 
	+ [Genomescope](http://qb.cshl.edu/genomescope/) 

* To run Genomescope, first you need to generate a Jellyfish histogram.

* You'll need two job files for Jellyfish, one to count the kmers and the second to generate a histogram to give to Genomescope:  

* First job file: kmer count:
	+ Module: ```bioinformatics/jellyfish/2.2.3```
	+ Commands: ```jellyfish count -C -m 21 -t $NSLOTS -s 800000000 *.fastq -o reads.jf```
	+ ```-m``` = kmer length  
	+ ```-s``` = RAM  
	+ ```-C``` = "canonical kmers" don't change this  

* Second job file: histogram:
	+ Module: ```bioinformatics/jellyfish/2.2.3```
	+ Commands: ```jellyfish histo -t $NSLOTS reads.jf > reads.histo```

* Download the histogram to your computer, and put it in the Genomescope webservice: [Genomescope](http://qb.cshl.edu/genomescope/) 






