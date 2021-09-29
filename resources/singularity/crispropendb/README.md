# CrisprOpenDB

Available from `library://dcarrillo/default/crispropendb:0.1`

* A [fork](https://github.com/dcarrillox/CrisprOpenDB) of the [original CrisprOpenDB](https://github.com/edzuf/CrisprOpenDB) is used to build this container. It mainly allows to define a directory
where the SQLite database is located. Check out the fork to see the specific changes in the source code.

* Databases used by CrisprOpenDB are not included in the container. You need to download them with
```
wget http://crispr.genome.ulaval.ca/dash/PhageHostIdentifier_DBfiles.zip
unzip PhageHostIdentifier_DBfiles.zip
```

## Procedure

1. Build the image with the definition file
```
$ sudo singularity build crispropendb.sif crispropendb.def
```

2. [Optional] Sign the image
```
$ singularity sign crispropendb.sif
```

3. Push it on the cloud
```
$ singulrity push crispropendb.sif library://dcarrillo/default/crispropendb:0.1
```

## Usage

```
$ singularity run library://dcarrillo/default/crispropendb:0.1 python /CrisprOpenDB/CL_Interface.py -h
```
