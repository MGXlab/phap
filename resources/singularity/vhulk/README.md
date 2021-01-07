# RaFaH

Available from `library://papanikos_182/default/vhulk:0.1`

## Procedure

0. Create a new dir for build context and get in there

1. Grab source from the 
[vHULK repo](https://github.com/LaboratorioBioinformatica/vHULK)


```
$ git clone https://github.com/LaboratorioBioinformatica/vHULK.git
```

2. Create a conda env as per 
[their suggestions](https://github.com/LaboratorioBioinformatica/vHULK#dependencies)
and export it explicitly with
```
$ conda list -n vhulk --explicit > vhulk_explicit.txt
```
This can be used for running stuff

3. Grab its data dependencies with the auxiliary script they provide 
```
$ conda activate vhulk
(vhulk) $ python ./download_and_set_models.py
```

4. Extract (for testing) and rebundle under `vhulk_resources.tar.gz`. This 
archive contains
```
$ tar -tvf vhulk_resources.tar.gz

drwxr-xr-x nikos/binf        0 2020-12-15 12:21 models/
-rw-r----- nikos/binf 70143964 2020-09-15 00:52 models/model_species_total_fixed_relu_08mar_2020.h5
-rw-r----- nikos/binf 70165848 2020-09-15 00:52 models/model_genus_total_fixed_relu_08mar_2020.h5
-rw-r--r-- nikos/binf 175382277 2020-12-15 12:19 models/all_vogs_hmm_profiles_feb2018.hmm.h3f
-rw-r----- nikos/binf  70165848 2020-09-15 00:52 models/model_genus_total_fixed_softmax_01mar_2020.h5
-rw-r----- nikos/binf  70143964 2020-09-15 00:52 models/model_species_total_fixed_softmax_01mar_2020.h5
-rw-r--r-- nikos/binf    333265 2020-12-15 12:19 models/all_vogs_hmm_profiles_feb2018.hmm.h3i
-rw-r--r-- nikos/binf 374382899 2020-12-15 12:19 models/all_vogs_hmm_profiles_feb2018.hmm.h3p
-rw-r--r-- nikos/binf 767855419 2020-12-15 12:19 models/all_vogs_hmm_profiles_feb2018.hmm
-rw-r--r-- nikos/binf 317721714 2020-12-15 12:19 models/all_vogs_hmm_profiles_feb2018.hmm.h3m
```

5. Modify the `vHULK-v0.1.py` to mainly point to the appropriate locations 
in the container. The rest is aesthetics done with 
[black](https://github.com/psf/black). Also make it executable. 
The copy in here is the one used in the container.

6. Build the image with the definition file
```
$ sudo singularity build vhulk.sif vhulk.def
```

7. [Optional] Sign the image
```
$ singularity sign vhulk.sif
```

8. Push it on the cloud
```
$ singulairty push vhulk.sif library://papanikos_182/default/vhulk:0.1
```

## Usage

```
$ singularity run library://papanikos_182/default/vhulk:0.1 vHULK_v0.1.py -h
```

