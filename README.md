<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/sandipanpaul06/PULSe">
    <img src="images/fau_logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">PULSe Documentation</h3>

  <p align="center">
    A positive-unlabeled learning based tool to find signatures of selection
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/sandipanpaul06/TrIdent/issues">Report Bug</a>
    ·
    <a href="https://github.com/sandipanpaul06/TrIdent/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

* Abstract: 

Identifying genomic regions shaped by natural selection is a central goal in evolutionary genomics. Existing machine learning methods for this task are typically trained using simulated genomic data labeled according to specific evolutionary scenarios. While effective in controlled settings, these models are limited by their reliance on explicit class labels. They can only detect the specific processes they were trained to recognize, making it difficult to interpret predictions for regions influenced by other evolutionary forces. This limitation is especially problematic when analyzing empirical genomes shaped by a mixture of adaptive, demographic, and ecological factors. One-vs.-rest strategies offer a potential alternative, but suffer from the inherent complexity of modeling all other evolutionary and demographic processes as a catch-all "rest" class. Here, we explore positive-unlabeled learning as a more flexible framework for detection of adaptive events. Positive-unlabeled learning is a semi-supervised approach that permits identification of samples of a target class using only positive labels and an unlabeled background, without requiring explicit modeling of negative samples. To assess the utility of this approach, we focus on a binary classification setting for detecting selective sweeps (positive samples) arising from positive natural selection against a mixed background composed of both unlabeled sweeps and neutrally-evolving regions. To accomplish this goal, we introduce PULSe, a method that employs only a set of labeled sweep observations for training while treating all remaining data as unlabeled. By avoiding assumptions about the composition of the background, PULSe enables robust sweep discovery in realistic genomic landscapes. We systematically evaluate its performance across a range of demographic, adaptive, and confounding contexts, including domain shift arising from misspecified demographic models, and find that PULSe delivers high performance and generalizability. To demonstrate a practical application of PULSe, we analyzed European human genomes, treating the empirical genome as the unlabeled set, and recapitulating several previously-identified sweep candidates. Our results show that PULSe provides a powerful, and versatile alternative for detecting adaptive regions, with the potential to generalize across a range of genomic landscapes, including non-model organisms. 
<p align="right">(<a href="#top">back to top</a>)</p>



### Built With



* [![Python][Python.org]][Python-url]

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

Python version 3.11.9 or above is necessary to use this software. Run the following commands to ensure you have the required version.
* check python version
  ```sh
  python --version
  ```

### Installation

Required python packages: Pandas, Numpy, Scikit-Learn, Scikit-Image, Matplotlib, Pulearn, OpenCV

1. Clone the repo
   ```sh
   git clone https://github.com/sandipanpaul06/PULSe.git
   ```
2. Go to project directory
   ```sh
   cd PULSe
   ```
3. Package installation
   ```sh
   pip install pandas numpy scikit-learn scikit-image matplotlib pulearn opencv-python-headless
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

**Sample data Provided with the software**

* *Discoal* .ms output fles:

  * *../PULSe/Datasets* contains three sample subfolders: *CEU_Neut*, *CEU_Sweep* and *Constant_Sweep*. The user can have as many subfolders as they like with thier choice of names.
  
  * *CEU_Neut* subfolder (*../PULSe/Datasets/CEU_Neut*) contains 15 sample neutral replicates with prefix 'neut' (*neut_1.ms, neut_2.ms ... Neut_15.ms*)
  * *CEU_Sweep* subfolder (*../PULSe/Datasets/CEU_Sweep*) contains 15 sample sweep replicates with prefix 'Sweep' (*Sweep_1.ms, Sweep_2.ms ... Sweep_15.ms*)
  * *Constant_Sweep* subfolder (*../PULSe/Datasets/Constant_Sweep*) contains 15 sample sweep replicates with prefix 'Sweep' (*Sweep_1.ms, Sweep_2.ms ... Sweep_15.ms*)
* Sample .vcf file:
  * *VCF_datasets* folder (*../PULSe/VCF_datasets*) contains gzipped vcf file of chromosome 22 from the CEU genome: *chrom22.vcf.gz*

**Modes**

The *PULSe* software has 6 modes:
* **image_gen_ms**: generate input image dataset from simulated replicates
* **HOG**: compute Histogram of Oriented Gradients from image dataset file
* **train**: train and test the *PULSe* model
* **calibrate**: calibrate predictions using *PULSe* calibration technique
* **preprocess_vcf**: extract gzipped .vcf.gz file > convert .vcf file to .csv file > breakdown the .csv file into 500 SNP subfiles
* **image_gen_vcf**: geneate image dataset from parsed vcf file


## Training with simulated replicates as unlabeled data

* Mode: **image_gen_ms**

* 1.1.1. Arguments:
  * -pref: .ms file prefix
  * -nHap: number of haplotypes
  * -subFolder: Name of the subfolder (that contains the simulations)
  * -n: Number of .ms files of the chosen class
  * -start: Start number of .ms files
  * -out: Output filename

* 1.1.2. Example run with sample .ms files:

   ```sh
   python PULSe.py -mode image_gen_ms -pref Sweep -nHap 198 -subFolder Constant_Sweep -n 15 -start 1 -out consweep
   ```
   ```sh
   python PULSe.py -mode image_gen_ms -pref Sweep -nHap 198 -subFolder CEU_Sweep -n 15 -start 1 -out ceusweep
   ```
   ```sh
   python PULSe.py -mode image_gen_ms -pref neut -nHap 198 -subFolder CEU_Neut -n 15 -start 1 -out ceuneut
   ```

* 1.1.3. Output file will be saved in *Image_datasets* folder (*../PULSe/Image_datasets*). The output files from the above commands would be: *consweep.npy*, *ceusweep.npy* and *ceuneut.npy*.


* Mode: **HOG**

* 1.2.1. Arguments:
  * -fileName: Image filename prefix
  * -pipeline: P1 or P2

* 1.2.2. Example run with sample image dataset file:

   ```sh
   python PULSe.py -mode HOG -fileName consweep -pipeline P2
   ```
   ```sh
   python PULSe.py -mode HOG -fileName ceusweep -pipeline P2
   ```
   ```sh
   python PULSe.py -mode HOG -fileName ceuneut -pipeline P2
   ```


* 1.2.3. Output files will be saved in *HOG_datasets* folder (*../PULSe/HOG_datasets*). The output files from the above commands would be: *consweep_HOGfeatures_0_6163.npy*, *ceusweep_HOGfeatures_0_6163.npy* and *ceuneut_HOGfeatures_0_6163.npy*.
* If alternate feature extraction pipeline chosen, please trail the filename with *HOGfeatures_1_9163.npy* or *HOGfeatures_0_6163.npy*

* Mode: **train**

* 1.3.1. Arguments:
  * -u: Number of samples on the unlabeled set
  * -l: Number of samples on the labeled set
  * -lp: Labeled positive filename prefix
  * -pipeline: P1 or P2
  * -testcase: 0: simulated unlabeled set, 1: empirical unlabeled set
  * -testname: Test name

  * --p: Percentage of positives in the unlabeled set (testcase 0 only)
  * --up: Unlabeled positive filename prefix (testcase 0 only)
  * --un: Unlabeled negative filename prefix (testcase 0 only)

* 1.3.2. Example run with sample image dataset file:

   ```sh
   python PULSe.py -mode train -u 28 -l 14 -lp consweep -pipeline P2 -testcase 0 -testname simTest --p 50 --up ceusweep --un ceuneut
   ```
**Warning: due to low number of images in this sample run, it sometimes fails. Re-run a few times if necessary. With enough samples (at least 100 each for labeled and unlabeled), this issue will not occur.**

* 1.3.3. Output predictions and true labels will be saved in *Predictions* folder (*../PULSe/Predictions*). The output files from the above commands would be: *PULSe_P2_simTest_predictions_raw.txt*, *PULSe_P2_simTest_labeled_predictions.txt* and *PULSe_P2_simTest_trueLabels.txt*. Users can use these values for empirical testcase(s).

* Mode: **calibrate**

* 1.4.1. Arguments:
  * -fileName: Image filename prefix
  * -testname: Test name
  * -pipeline: P1 or P2
  * testcase: 0: simulated unlabeled set, 1: empirical unlabeled set'
  * -T: Calibration threshold

* 1.4.2. Example run with sample image dataset file:

   ```sh
   python PULSe.py -mode calibrate -testname simTest -pipeline P2 -testcase 0 -T 0.3
   ```


* 1.4.3. Output calibrated predictions will be saved in *Predictions* folder (*../PULSe/Predictions*). The output files from the above commands would be: *PULSe_P2_simTest_predictions_calibrated.txt*

## Training with empirical genome as unlabeled data

* Mode: **preprocess_vcf** 


* 2.1.1. Arguments are:
  * -fileNameVCF: file name (gzipped .vcf)
  * -outFolder: Output folder name

* 2.1.2.  Example run with sample file:

   ```sh
   python PULSe.py -mode preprocess_vcf -fileNameVCF chrom22.vcf.gz -outFolder chr22
   ```

* 2.1.3 Output smaller .csv files containing 500 SNP chunks will be saved in user-defined subfolder in the *VCF_datasets* folder (*../PULSe/VCF_datasets*). From the command above, smaller .csv files with prefix 'chrom22' (example: *chrom22_1.csv*, chrom22_1.csv*, ..) will be saved in the *chr22* subfolder (*../PULSe/VC_datasetsF/chr22*).




* Mode: **image_gen_vcf**


* 2.2.1. Arguments are:
  * -pref: .ms file prefix
  * -nHap: number of haplotypes
  * -subFolder: Name of the subfolder (that contains the simulations)
  * -n: Number of .ms files of the chosen class
  * -start: Start number of .ms files
  * -out: Output filename

* 2.2.2.  Example run with sample file:

   ```sh
   python PULSe.py -mode image_gen_vcf -pref chrom22 -nHap 198 -subFolder chr22 -n 20 -start 1 -out empTestImg
   ```

* 2.2.3 Output will be saved in *Image_datasets* (*../PULSe/VCF_datasets*) folder. From command above, image dataset *empTestImg.npy* and corresponding positions in the genome *empTestImg_pos.txt* will be saved in *../PULSe/Image_datasets*.

* Mode: **HOG**

* 2.3.1. Arguments:
  * -fileName: Image filename prefix
  * -pipeline: P1 or P2

* 2.3.2. Example run with sample image dataset file:

   ```sh
   python PULSe.py -mode HOG -fileName empTestImg -pipeline P2
   ```
* 2.3.3. Output files will be saved in *HOG_datasets* folder (*../PULSe/HOG_datasets*). The output file from the above commands would be: *empTestImg_HOGfeatures_0_6163.npy*.
  
* Mode: **train**

* 2.4.1. Arguments:
  * -u: Number of samples on the unlabeled set
  * -l: Number of samples on the labeled set
  * -lp: Labeled positive filename prefix
  * -pipeline: P1 or P2
  * -testcase: 0: simulated unlabeled set, 1: empirical unlabeled set
  * -testname: Test name

  * --emp: Empirical filename (testcase 1 only)

* 2.4.2. Example run with sample image dataset file:

   ```sh
   python PULSe.py -mode train -u 20 -l 14 -lp consweep -pipeline P2 -testcase 1 -testname empTest --emp empTestImg
   ```
**Warning: due to low number of images in this sample run, it sometimes fails. Re-run a few times if necessary. With enough samples (at least 100 each for labeled and unlabeled), this issue will not occur.**

* 2.4.3. Output predictions and true labels will be saved in *Predictions* folder (*../PULSe/Predictions*). The output files from the above commands would be: *PULSe_P2_empTest_predictions_raw.txt* and *PULSe_P2_empTest_labeled_predictions.txt*.

* Mode: **calibrate**

* 2.5.1. Arguments:
  * -fileName: Image filename prefix
  * -pipeline: P1 or P2
  * -testname: Test name
  * -pipeline: P1 or P2
  * testcase: 0: simulated unlabeled set, 1: empirical unlabeled set'
  * -T: Calibration threshold

* 2.5.2. Example run with sample image dataset file:

   ```sh
   python PULSe.py -mode calibrate -testname empTest -pipeline P2 -testcase 1 -T 0.3
   ```
* 2.5.3. Output calibrated predictions will be saved in *Predictions* folder (*../PULSe/Predictions*). The output files from the above commands would be: *PULSe_P2_empTest_predictions_calibrated.txt*
<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Sandipan Paul Arnab - sarnab2020@fau.edu



<p align="right">(<a href="#top">back to top</a>)</p>







<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Python.org]: https://data-science-blog.com/wp-content/uploads/2022/01/python-logo-header-1030x259.png
[Python-url]: https://www.python.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
