# Overview

## Features

* Uses [Singularity](https://sylabs.io/) containers for the execution of all 
tools.

When possible (i.e. the image is not larger than a few `G`s), tools **and** 
their dependencies are bundled in the same container. This means
you do not need to get models or any other external databases, unless 
otherwise specified.

* Intermediate processing steps are handled by [Conda](https://conda.io/en/latest/) 
environments, to ensure smooth and reproducible execution.


* Outputs the Last Common Ancestor of all tools, per contig, based on the 
predicted taxonomy.

## Tools

|Tool (source) | Publication/Preprint | Comments |
|:------|:------|:------:|
[HTP](https://github.com/wojciech-galan/viruses_classifier)|[Gałan W. et al., 2019](https://www.nature.com/articles/s41598-019-39847-2)|ok
[RaFAh](https://sourceforge.net/projects/rafah/)|[Coutinho F. H. et al., 2020](https://www.biorxiv.org/content/10.1101/2020.09.25.313155v1?rss=1)|ok
[vHuLK](https://github.com/LaboratorioBioinformatica/vHULK)|[Amgarten D. et al., 2020](https://www.biorxiv.org/content/10.1101/2020.12.06.413476v1)|ok
[VirHostMatcher-Net](https://github.com/WeiliWw/VirHostMatcher-Net)|[Wang W. et al., 2020](https://doi.org/10.1093/nargab/lqaa044)|ok
[WIsH](https://github.com/soedinglab/WIsH)|[Galiez G. et al., 2017](https://academic.oup.com/bioinformatics/article/33/19/3113/3964377)|ok (unnecessary?)


