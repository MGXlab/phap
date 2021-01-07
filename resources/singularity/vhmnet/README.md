# VirHostMatcher-Net

Available from `library://papanikos_182/default/vhmnet:0.1`

* Note that data dependencies are not included in the container.
You need to get them with 
```
wget -c http://www-rcf.usc.edu/~weiliw/VirHostMatcher-Net/data_VirHostMatcher-Net_both_modes.tar.gz    
tar xf data_VirHostMatcher-Net_both_modes.tar.gz
```
The models and genomes unpacked are 125G.

* [My fork](https://github.com/papanikos/VirHostMatcher-Net)
is used for grabbing source. It mainly allows to define a directory 
where the data are located

## Procedure

0. Create a new dir for build context and get in there

1. Create a conda env with its requirements, verify it is working and export
it explicitly

```
$ conda env create -n vhmnet numpy pandas biopython blast
...
...Test it runs...
...
$ conda list -n vhmnet --explicit > environment.txt
```

2. Build the image with the definition file
```
$ sudo singularity build vhmnet.sif vhmnet.def
```

3. [Optional] Sign the image
```
$ singularity sign vhmnet.sif
```

4. Push it on the cloud
```
$ singulairty push vhmnet.sif library://papanikos_182/default/vhmnet:0.1
```

## Usage

```
$ singularity run library://papanikos_182/default/vhmnet:0.1 \
  VirHostMatcher.py -h
```

