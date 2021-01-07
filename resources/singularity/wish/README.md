# WIsH 

Available from `library://papanikos_182/default/wish:1.0`

* Note that data dependencies are not included in the container.
Models from  [VirHostMatcher-Net](https://github.com/WeiliWw/VirHostMatcher-Net#downloading)
are used

## Procedure

1. Build the image with the definition file
```
$ sudo singularity build wish.sif wish.def
```

3. [Optional] Sign the image
```
$ singularity sign wish.sif
```

4. Push it on the cloud
```
$ singulairty push wish.sif library://papanikos_182/default/wish:0.1
```

## Usage

```
$ singularity run library://papanikos_182/default/wish:1.0 \
  WIsH -h
```

