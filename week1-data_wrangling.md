Genome Assembly Workshop Week 1: Data Wrangling
---

Tutorial Steps:  
1. Getting set on Hydra  
2. Downloading data with SRA toolkit  
3. Running FastQC on raw data  
4. Trimming adapters with TrimGalore  

###1. Getting set on Hydra
* login to Hydra (If you need assistance with Hydra, check the [support wiki](https://confluence.si.edu/display/HPC/High+Performance+Computing)).
* change to your directory  
    + hint: `cd /pool/genomics/USERNAME` where *USERNAME* is your Hydra login name
* create a project directory: ```mkdir assembly_tutorial```  
* change to that directory: ```cd assembly_tutorial```

###2. Downloading data with SRA toolkit 
We are downloading PacBio and Illumina MiSeq data to Hydra from the NCBI Sequence Read Archive (SRA). The SRA numbers we need are: SRR2181871 & SRR1555312. We have to convert these to fastq using the SRA toolkit. We'll need two job files, one for each SRA entry. 

* First, go to the NCBI SRA website to check out the SRA and search for the files we need:  
http://www.ncbi.nlm.nih.gov/sra  
 
* Create a job file to download the PacBio data and convert to fastq format:  
	+ hint: use the QSub Generator: ```https://hydra-3.si.edu/tools/QSubGen```
    + *Remember Chrome works best with this and to accept the security warning message*  
    + **CPU time:** short *(we will be using short for all job files in this tutorial)*
    + **memory:** 2GB
    + **PE:** serial
    + **shell:** sh *(use for all job files in the tutorial)*
    + **modules:** ```bioinformatics/sratoolkit/2.5.4```
    + **command:** 
    ```fastq-dump SRR2181871```  
    + **job name:** SRA-PacBio *(or name of your choice)*  
    + **log file name:** SRA-PacBio.log  
    + **change to cwd:** Checked *(keep checked for all job files)*  
    + **join stderr & stdout** Checked *(Keep checked for all job files)*  
    + hint: either use ```nano``` or upload your job file using ```scp``` from your local machine into the `assembly_tutorial` directory. See [here](https://confluence.si.edu/display/HPC/Disk+Space+and+Disk+Usage) and [here](https://confluence.si.edu/display/HPC/Transferring+files+to+or+from+Hydra) on the Hydra wiki for more info.  
    + hint: submit the job on Hydra using ```qsub```   
    + important: SRA creates a cache in ~/ncbi that can get big and needs to be manually removed
    + if you happen to get an error from NCBI as can sometimes occur with outside URLs, ```cp``` the data to your directory: ```cp /pool/scratch/genomics/dikowr/SRR2181871.fastq <YOUR_PATH>``` 


* Create a job file to download the Illumina MiSeq data and convert to fastq format:  
 + here we need an additional argument to split the SRA file into forward and reverse since the data are paired-end.
 + **command:** 
```fastq-dump --split-files SRR1555312```  
+ see above about using ```cp``` if you get an error. These files will be named ```SRR1555312_1.fastq``` and ```SRR1555312_2.fastq```

* It's probably useful to rename these files so that the names are meaningful. Try something like this:  
	+ ```ls``` to see the current names of the files you just downloaded   
	+ use ```mv``` to rename them, e.g. ```mv SRR1555312_1.fastq Salmonella_RM_8375_MiSeq_SRR1555312_1.fastq```  
	+ rename the other two files similarly  

	
###3. Running FastQC on raw data

* FastQC is a program that can quickly scan your raw data to help figure out if there are adapters or low quality reads present. Create a job file to run FastQC on one of the three files you downloaded.
  
	+ **module**: ```bioinformatics/fastqc/0.11.5```
	+ **command**: ```fastqc <FILE.fastq>```
	+ after your job finishes, find the results and download some of the images, e.g. ```per_base_quality.png``` to your local machine using ```scp```
	+ Try with the other two files to compare

###4. Trimming adapters with TrimGalore 
* PacBio data will be error-corrected solely by the assembler, but Illumina data trimming and thinning are common.
* Most assemblers these days don't want you to trim/thin for quality before assembling, but we do want to make sure we look for adapters. TrimGalore will auto-detect what adapters are present and remove very low quality reads (quality score <20) by default.  
* Run TrimGalore on Illumina data to trim adapters. I think the data we downloaded are clean, but it's a good exercise! Create a job file to trim adapters and very low quality reads for the Illumina data.
	+ **command**: ```trim_galore --paired --retain_unpaired <FILE_1.fastq> <FILE_2.fastq>```  
	+ **module**: ```bioinformatics/trimgalore/0.4.0```
	+ You can then run FastQC again to see if anything has changed.

###Next week we will talk about resource allocation and configuration files for the actual assemblies!


