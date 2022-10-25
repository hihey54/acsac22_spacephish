This document describes the Artifact of the paper “_SpacePhish: The Evasion-space of Adversarial Attacks against Phishing Website Detectors using Machine Learning_”. We also created a website with additional information: [SpacePhish website](https://spacephish.github.io/)

## Organization

This repository includes four main folders: 

* **documents_folder**: containing the main paper, and other supplementary documents;
* **ml\_folder**: containing the source-code of our main experiments;
* **preprocessing\_folder:** containing the code of our feature extractor and some attacks
* **mlsec_folder**: containing the code of our attacks against the detectors of MLSEC;

In the root folder of this repository, we have also provided a “requirements.txt” file, specifying which Python libraries were used to carry out all our experiments. Moreover, we also provided a document ("get\_data.md") explaining how to retrieve the data for our experiments. This artifact entirely runs on CPU.

In what follows, we will first provide a high-level overview of the _documents_ and _data_ folders, and then explain how to use the corresponding code for a practical evaluation.

## Disclaimer

Our paper tackles the problem of _phishing_ website detection via _machine learning_ (ML). As such, performing our experiments “today” and “from scratch” is likely to yield different results than those shown in the paper. This is due to two main reasons:

1. **The “preprocessing” phase of each sample (i.e., a webpage) requires to make some queries to DNS servers.** Such servers may give a different response _today_ than the one we received when we performed our experiments. 
2. **The “machine learning” phase of our experiments entails the development of 900 ML models** (by randomly _drawing samples_ belonging to different _datasets_ and using diverse ML _algorithms_ analyzing _feature_ sets). The results reported in the paper are the average of all such evaluations. Hence, it is likely that a “novel” experiment may lead to a different outcome (due to the high role played by randomness in the general context of ML)

To account for the above, and to facilitate the reviewing process, we:

* \[data\] report the _preprocessed_ version of each sample (for both its original and adversarial variant) which we used for our ML experiments.
* \[code\] provide three jupyter-notebooks describing a single “run” of our ML experiments (on a single dataset) having a “random seed” whose result match those in our paper.

## Contents

We first explain the documents folder, then the data folder (which must be downloaded separately), and finally the folders containing the source code.

### documents\_folder

This folder contains 6 files:

* _ACSAC_SpacePhish-paper.pdf_, which is the main paper.
* _ACSAC_SpacePhish-supp.pdf_, which is a document explaining (at a high level) some implementation details (this document was provided to the reviewers during the submission). 
* _reference\_tables.png_, which is are three images showing the “range” of the results we obtained during our experiments (one for each algorithm). We expect that any future experiment will achieve results within (or close to) such range (we repeated our experiments 50 times).
* _mlsec\_results.xlsx_, which is a spreadsheet containing the full results of *all* our cheap attacks on the detectors of the MLSEC competition.

### data\_folder

#### Preliminary Information

Let us provide some essential background information for those who are not experts in the specific problem tackled by our paper.

* **Sources.** Our paper entails experiments carried out on two datasets: [DeltaPhish](https://link.springer.com/chapter/10.1007/978-3-319-66402-6_22) and [Zenodo](https://dl.acm.org/doi/abs/10.1145/3465481.3470112) (both of which are publicly available), containing “raw data” of webpages (benign or phishing). For transparency, we include in this repository all such “raw data”, which will be deleted after the review of the artifact (to avoid potential copyright violations). We will, however, maintain the preprocessed version of each webpage. 
* **Attacks**. Our paper entails “adversarial attacks against machine learning”, whose basic principle is to (i) take a sample, (ii) manipulate such sample in some way, and (iii) assess whether the “adversarial sample” evades a given ML model or not. Specifically in our case, we consider a total of 12 adversarial attacks, meaning that we artificially create 12 “adversarial variants” of each “original sample” (i.e., a phishing webpage). Some of these variants are created “at runtime”, whereas the others are created “in advance” (we did this by manually manipulating each raw sample). 

#### Structure

The folder is organized depending on the _dataset_ (Zenodo or Deltaphish), the format (raw or preprocessed). Let us explain both of these:

* _**raw:**_ this folder contains the “original” data as well as the adversarial variants of each sample.
	* _normal_. This folder contains information on the “original” webpages. It contains a JSON file with the URLs of each sample; and an “HTML” folder containing the raw HTML of each sample
	* _wa_. This folder refers to the “cheap” attacks considered in our paper. It contains files including the HTML of phishing webpages after applying the “cheap” HTML manipulation.
	* _wa+_. This folder refers to (a subset of) the “advanced” attacks of our paper. It contains files including the HTML of phishing webpages after applying the “advanced” HTML manipulations.
* _**Preprocessed:**_ this folder includes data describing the “preprocessed” format of each sample in the “raw” folder---after the application of our custom-built feature extractor.
	* _normal_. This folder contains a single JSON file describing the feature representation of each “normal” sample (benign and phishing)
	* _wa_ and _wa+_. These folders contain three subfolders ("u, r, c") each referring to a specific variant of our _wa/wa+_ attacks. Each subfolder has a single JSON file, which contains the feature representation of each (phishing) sample after applying adversarial manipulation.
	* _phish\_sub\_test\_x\_100.pkl._ This is a “pickle” file including the 100 samples used as basis for our our adversarial attacks in the preprocessing space. 

### preprocessing\_folder

This folder contains 4 files:

* _extractor.py_: this python script analyzes a sample (a phishing webpage) and extracts its feature representation. 
* _feature\_extraction.ipynb_: is a (small) notebook showcasing the application of extractor.py on a single sample.
* _PA\_PSP.ipynb_: is a notebook that applies the perturbations related to the preprocessing attacks considered in our paper.

### ml\_folder

This folder contains 4 files, which refer to the experiments performed on the “DeltaPhish” dataset:

* _ML.py_, containing some custom-defined functions for developing our ML models and printing their results
* _RF/CN/LR\_experiments.ipynb_, which are notebooks containing the experiments for each of the 3 main ML algorithms considered in our paper (RF=random forest, LR=logistic regression, CN=convolutional neural network).

### mlsec\_folder

This folder contains the data and code for the attacks against the detectors of MLSEC. It contains one folder and two files:

* _data_, which is a folder containing the “original” webpages provided by MLSEC; as well as a subfolder “wsp” in which the adversarial variants of such originals will be saved (we already included all the variants generated via our WA attacks)
* _mlsec\_artifact\_manipulate.ipynb_, which is a notebook containing _all_ the simple manipulations described in our supplementary material, as well as the queries to the MLSEC API 
* _mlsec\_artifact\_checker.ipynb_, which is a notebook that provides a "bulk" checking of all the webpages (original and adversarial ones) created via the previous notebook

## INSTRUCTIONS

Let us explain how to use our artifact.

1. **Get the data, and install requirements**. This is self explanatory; we recommend creating an ad-hoc virtual environment for this purpose (PyCharm works very well). Important: the _data\_folder_ should be placed in the root directory!
2. **Test the feature extractor.** Simply run the _preprocessing\_folder/feature\_extraction.ipynb_ notebook once. It should prove that the feature extractor “works”.
3. **Create the adversarial samples corresponding to PA**. Simply run the _preprocessing\_folder/PA\_PSP.ipynb_ once.
4. **Test the attacks.** Consider any of the three notebooks (e.g., “ml\_folder/experiments\_RF.ipynb”) and run all of its cells. The LR and RF do not take long to train, whereas the CN can take several minutes (the runtime on our platform is provided in the documentation). Every cell reports the part in the paper in which the corresponding result is “shown”. Due to randomness, the results can differ from those in the paper (which are provided just as the average and std. dev.): please refer to the “reference\_tables.png” file to assess the fidelity of a given result.
5. **Check the MLSEC results.** Simply run the _mlsec\_folder/mlsec\_artifact\_checker.ipynb_ notebook, which will automatically query the MLSEC API and provides the results described in the supplementary material and reported in the _documents\_folder/results.xlsx_ file. The MLSEC API is still active, so these results are 100% reproducible (unless the ML-PWD change at the server side).
6. **Play around with MLSEC notebook.** Run the _mlsec\_folder/mlsec\_artifact\_manipulate.ipynb_ notebook and see its effects on a specific webpage. Feel free to “visually” inspect the adversarial variant of any given webpage, as well as change the amount of links added, or the corresponding string. The MLSEC API is still active.


