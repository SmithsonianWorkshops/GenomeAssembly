Assembly Workshop Week 4: Generating Assembly Metrics  
---

Tutorial steps: 
1. How to most effectively get help  
2. Run Genomescope  
3. Run QUAST  
4. Genome alignments with LASTZ  
5. BUSCO  
6. Metagenomic classification with Kraken  
  

###1. How to most effectively get help
* These hints may seem obvious, but can save you time if figuring out why something went wrong.
	+ Is your job running? ```qstat```
	+ Did it complete with an error? ```ls``` to see if a log file was created.
	+ If you don't see a log file, either the job was not submitted or you are in the wrong directory.
	+ If you have a question about why something failed and need further consultation, email us as a group! ```si-hpc@si.edu```
	+ PLEASE include your job file, log file, and path to your working directory in your email. We can help you much faster that way.

###2. Run Genomescope
* This is from last week...if everyone completed it already, we can move on.
* [Genomescope](http://qb.cshl.edu/genomescope/) is a new program written by Mike Schatz's group that can be used to estimate genome size from short read data: 
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
* Download the histogram to your computer, and put it in the Genomescope webservice: [Genomescope](http://qb.cshl.edu/genomescope) 
![](/Users/rebeccadikow/Desktop/genomescope.tiff)

###Run QUAST
* [QUAST](http://bioinf.spbau.ru/quast) is a program that allows you to compare your assembly (or assemblies) to one another or to a reference. 
* Since the *Salmonella* genome is assembled to chromosome, we can use that as a reference.
* Copy it from my directory to yours with ```cp```
	+ It's called ```Salmonella_complete_genome.fasta``` and is in ```/pool/genomics/dikowr/assembly_tutorial```
* If you need any of the assemblies from previous weeks, they are also in ```/pool/genomics/dikowr/assembly_tutorial```
* Running QUAST
	+ **Module:** ```bioinformatics/quast/3.1```
	+ **Command:** ```quast.py```
	+ **Arguments:** ```-o```= output directory, ```--threads```= number of threads, ```-R``` = reference genome 
	+ List the contig fasta assembly files after your other arguments
	+ You will need to add the ```--scaffolds``` argument if including scaffold files
	+ Lots of other options in the QUAST manual
	+ **Resource recommendations:** Serial, 4GB RAM, short. Note: for larger genomes, QUAST will need much more RAM.
* After it completes, check out some of the graphs it produces, *e.g.*
![](http://www.github.com/SmithsonianWorkshops/GenomeAssembly/Nx_quast.png?raw=true)

###4. Genome alignments with LASTZ
* [LASTZ](http://www.bx.psu.edu/~rsharris/lastz/) is a pairwise genome alignment program.
*  We're going to use it to align our genomes to the *Salmonella* reference and then view in Geneious.
*  You tell it the reference and contig/scaffold file, and it generates a SAM file. LASTZ is different than a multiple sequence alignment program because it allows the query matches to not be in the same order as the reference genome. 
	+ **Module**: ```bioinformatics/lastz/1.03```
	+ **Command**: ```lastz```
	+ **Arguments**: ```<REFERENCE GENOME> <QUERY GENOME> ambiguous=iupac --chain --nogapped hspthresh=2500 --seed=12of19 --step=10 --format=sam > <ALIGNMENT.sam>```
	+ **Resource recommendations**: Serial, 4GB RAM, short.
	+ There are many additional parameters in the LASTZ documentation, I've chosen the above because they seem to provide the appropriate sensitivity, but read more about them when you have time.
* After it completes, download the SAM file and the *Salmonella* reference genome fasta file to your computer and open them in Geneious. To import a SAM file in Geneious, you always need the reference file too.

###5. BUSCO
* [BUSCO](http://busco.ezlab.org), Assessing genome assembly and annotation completeness with Benchmarking Universal Single-Copy Orthologs, is a way to check assembly completeness.
* Using a known conserved gene set for your taxon of interest, you assess completeness for those conserved genes.
	+ **Module**: ```bioinformatics/busco/1.1b1```
	+ **Command**: ```BUSCO_v1.1b1.py```
	+ **Arguments**: ``-o``= output directory, ```-in```= your assembly, ```-l```= BUSCO gene set, ```-c``` = CPUs, ```-m```= indicates this is a genome assessment.
	+ **Resource recommendations**: Serial, 4GB RAM, short.
	+ The bacteria BUSCO gene set is here: ```/pool/genomics/dikowr/assembly_tutorial/Bacteria```
* After it completes, check the short_summary for results.

###6. Metagenomic classification with Kraken
* [Kraken](https://ccb.jhu.edu/software/kraken/) is a metagenomic classifier that can be used on reads, contigs, or really any DNA sequence using 31bp exact kmer matches.
* It uses the Bacterial, Archaeal, and Viral RefSeq database (finished genomes) or you can create a custom database.
* Kraken can be used to classify true metagenomic sequences, or can be used to detect contamination in Eukaryote genomes.
* There is also a Kraken base space app that looks interesting.
* Today, we will use it to see if there is any contamination in an assembled Eukaryotic genome.
* First, think of a genome of interest to you that is available on GenBank (either raw reads or assembled genome).
* If you want to use raw reads, use SRAtoolkit (week 1) to download the data to Hydra.
* If you want to look at an assembly, download the contig or scaffold file.
* There are two parts to running Kraken, first classifying the reads and then assigning names.
* Classifying the reads:
	+ **Module**: ```bioinformatics/kraken/0.10.5```
	+ **Command**: ```kraken```
	+ **Arguments***: ```--preload```= preload the database, ```--db```= path to database, ```--threads```= number of threads, ```<YOUR_FILE.fasta>```
	+ The Kraken database is here: ```/pool/scratch/genomics/dikowr/KrakenDB```
	+ **Resource recommendations**: you will need approximately 100GB RAM, so divide that across the number of threads you want to request. This has to be run on the himem queue, short.
* Assigning names:
	+ + **Module**: ```bioinformatics/kraken/0.10.5```
	+ **Command**: ```kraken-translate```
	+ **Arguments***: ```--db```= path to database, ```<YOUR_LOG_FILE_FROM_STEP_1.log>```
	+ **Resource recommendations**:  Serial, 4GB RAM, short.


