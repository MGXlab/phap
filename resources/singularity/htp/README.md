# Host Taxon Predictor (HTP) 

Available from `library://papanikos_182/default/htp:1.0.2`

## Procedure

1. Build the image with the definition file
```
$ sudo singularity build htp.sif htp.def
```

3. [Optional] Sign the image
```
$ singularity sign htp.sif
```

4. Push it on the cloud
```
$ singulairty push htp.sif library://papanikos_182/default/htp:1.0.2
```

## Usage

```
$ singularity run library://papanikos_182/default/htp:1.0.2 \
  viruses_classifier -h
```

