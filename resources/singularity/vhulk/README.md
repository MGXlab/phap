# vHULK 

Available from `library://papanikos_182/default/vhulk:1.0.0`

Required models and hmm databases are downloaded when building.
These are stored in `/opt/vHULK/models`, along with the script, hence no need 
to specify the models path

## Procedure

1. Build the image with the definition file
```
$ sudo singularity build vhulk.sif vhulk.def
```

2. [Optional] Sign the image
```
$ singularity sign vhulk.sif
```

3. Push it on the cloud
```
$ singulrity push vhulk.sif library://papanikos_182/default/vhulk:1.0.0
```

## Usage

```
$ singularity run library://papanikos_182/default/vhulk:1.0.0 vHULK.py -h
```
