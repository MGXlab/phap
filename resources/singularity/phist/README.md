# PHIST

Available from `library://dcarrillo/default/phist:1.0.0`

* An already compiled version 1.0.0 of [PHIST](https://github.com/refresh-bio/PHIST)
is used to build this container.

* For the analysis, users need to define and create a database with the genomes
of the putative hosts. This container does not contain such database, but check
out the documentation to create a comprehensive database from RefSeq.

## Procedure

1. Build the image with the definition file
```
$ sudo singularity build phist.sif phist.def
```

2. [Optional] Sign the image
```
$ singularity sign phist.sif
```

3. Push it on the cloud
```
$ singulrity push phist.sif library://dcarrillo/default/phist:1.0.0
```

## Usage

```
$ singularity run library://dcarrillo/default/phist:1.0.0 python /PHIST/phist.py -h
```
