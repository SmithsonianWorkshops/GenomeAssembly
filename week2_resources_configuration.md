Genome Assembly Workshop Week 2: Resource Allocation and Configuration Files
---

Tutorial Steps:  
1. Getting set on Hydra  
2. Making sure you have the sequence files  
3. Setting up SPAdes Illumina only  
4. Setting up SPAdes Illumina + PacBio
5. Setting up DISCOVAR Illumina only
6. Setting up MaSuRCA Illumina + PacBio

###1. Getting set on Hydra
* Login to Hydra (If you need assistance with Hydra, check the [support wiki](https://confluence.si.edu/display/HPC/High+Performance+Computing)).
* Change to your directory  
    + hint: `cd /pool/genomics/USERNAME` where *USERNAME* is your Hydra login name 
* Change to your workshop directory: e.g. ```cd assembly_tutorial```


###2. Making sure you have the sequence files 
* You should have three fastq files in your directory (If you tried trimming, you can ignore these results as the data are clean, that was just for practice).  
* Last week, we renamed these files:  
``Salmonella_RM_8375_MiSeq_SRR1555312_1.fastq``  
``Salmonella_RM_8375_MiSeq_SRR1555312_2.fastq``   
``Salmonella_RM_8375_PacBio_SRR2181871.fastq``   
* Check to make sure you have these with ```ls```  
* What is the approximate coverage for these data?
	+ *Salmonella* genome size: 4.5Mbp  
	+ Info from SRA: PacBio: 1.6G bp, MiSeq: 491.7M bp  

###3. Setting up SPAdes Illumina only 
* Here is more info about SPAdes: [SPAdes manual](http://bioinf.spbau.ru/spades)  
* Create a job file to run SPAdes:
	+ **Hint:** use the QSub Generator: [QSub Generator](https://hydra-3.si.edu/tools/QSubGen)  
	+ **Queue:** Medium-length, High CPU queue is fine for small genomes  
	+ **Threads & RAM:** I suggest 12 threads, with 4GB RAM for each  
	+ **Module:** ```module load bioinformatics/spades/3.7```    
	+ Make sure you choose the most recent version of SPAdes, 3.7.    
 + For 2X250 Illumina data, they suggest the following commands: 
``-k 21,33,55,77,99,127``    
``--careful``  
	+ You will also need to specify the reads using:   
``-1 Salmonella_RM_8375_MiSeq_SRR1555312_1.fastq``  
``-2 Salmonella_RM_8375_MiSeq_SRR1555312_2.fastq``   
	+ And an output directory:  
``-o SPAdes_Illumina_only``   

* Your commands will look something like this:
```spades.py -k 21,33,55,77,99,127 --careful -1 Salmonella_RM_8375_MiSeq_SRR1555312_1.fastq -2 Salmonella_RM_8375_MiSeq_SRR1555312_2.fastq -o SPAdes_Illumina_only```

* Save your job file with a descriptive name, e.g. ```SPAdes_Illumina_only.job``` and submit it with ```qsub```
  
###4. Setting up SPAdes Illumina + PacBio
* Create another job file, same specifications as above except you will add the PacBio flag, while keeping the rest of the above commands:
```--pacbio Salmonella_RM_8375_PacBio_SRR2181871.fastq```  

* You will also need to specify a different output directory so you don't overwrite your Illumina only assembly:  
```-o SPAdes_Hybrid```

###5. Setting up DISCOVAR Illumina only
* Here is more info about DISCOVAR: [DISCOVAR manual](Discovar manual: https://docs.google.com/document/d/1U_o-Z0dJ0QKiJn86AV2o_YHiFzUtW9c57eh3tYjkINc/edit)  
* Create a job file to run DISCOVAR:
 + **Queue:** Short length, high memory  
 + **Threads & RAM:** 8 threads, 12GB RAM each  
	+ **Module:** ```module load bioinformatics/disocovardenovo/52488```
	+ **Commands:** ```DiscovarDeNovo READS=Salmonella_RM_8375_MiSeq_SRR1555312_1.fastq,Salmonella_RM_8375_MiSeq_SRR1555312_2.fastq OUT_DIR=Salmonella_DISCOVAR MAX_MEM_GB=90 MEMORY_CHECK=TRUE```
	+ **Hint:** DISCOVAR can sometimes produce memory errors - let us know if you get one.

###6. Setting up MaSuRCA Illumina + PacBio
* Here is more info about MaSuRCA: [MaSuRCA manual](http://www.genome.umd.edu/docs/MaSuRCA_QuickStartGuide.pdf)
* First you will need to convert the PacBio fastq to fasta. Create a job file with the following command (make your own decisions about resources and module - ask us if you have questions):  
```sed -n '1~4s/^@/>/p;2~4p' Salmonella_RM_8375_PacBio_SRR2181871.fastq > Salmonella_RM_8375_PacBio_SRR2181871.fasta```  

* MaSuRCA runs with 2 job files. The first uses a configuration file to generate an sh script called assemble.sh. Then you just execute the sh script to complete the actual assembly.  
* Go to the GitHub site to find MaSuRCA_sample.config and open it with a text editor.    
* Edit the file so that it points to your files and familiarize yourself with the parts.    
* To keep things tidy, create a directory for the MaSuRCA assembly.
	+ ```mkdir MaSuRCA_Salmonella```  
* Create a job file for this first part of MaSuRCA.  
	+ **Queue:** Short, high CPU  
	+ **Threads & RAM:** single thread, 2GB RAM  
	+ **Module:** ```module load bioinformatics/masurca/3.2.1_04022016```  
	+ **Commands:** ```masurca MY_CONFIG.config```   
* Save the job file to the ```MaSuRCA_Salmonella``` directory and submit it from there.  
* This job should complete in a few seconds and result in a file called assemble.sh  
* Create a second job file for the second part of MaSuRCA.  
	+ **Queue:** Medium, himem  
	+ **Threads & RAM:** 8 threads, 12GB RAM each  
	+ **Module:** ```module load bioinformatics/gcc/4.9.2```  
	+ **Command:** ```./assemble.sh```  
* Submit this second job.

