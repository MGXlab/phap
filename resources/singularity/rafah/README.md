# RaFaH

Available from `library://papanikos_182/default/rafah:0.1`

## Procedure

0. Create a new dir for build context and get in there

1. Grab necessary dependencies from the 
[RaFaH repo](https://sourceforge.net/projects/rafah/files/RaFAH_v0.1_Files/)

```
$ wget https://sourceforge.net/projects/rafah/files/RaFAH_v0.1_Files
$ tar -xzvf whatever_is_downloaded
```

> wgetting is slow, I used another copy, locally available

2. Edit RaFaH script to point to appropriate locations in the container
  - Replace shebang (line 1) with `#!/usr/bin/env perl`
  - Change line 37 to `my $valid_domains_file = "/opt/resources/HP_Ranger_Model_3_Valid_Cols.txt";`
  - Change line 38 to `my $hmm_models_prefix = "/opt/resources/HP_Ranger_Model_3_Filtered_0.9_Valids.hmm";`
  - Change line 39 to `my $r_script_file_name = "/src/Predict_Host_RF.R";`
  - Change line 40 to `my $r_model_file_name = "/opt/resources/MMSeqs_Clusters_Ranger_Model_1+2+3_Clean.RData";`

3. Make RaFah_v0.1.pl executable
```
$ chmod +x RaFaH_v0.1.pl
```

4. Bundle tables and models in a tar archive (not the perl and R script) and 
not the `HP_Ranger_Model_3_Valid_Cols.txt`
```
$ tar -czvf rafah_resources.tar.gz ./*hmm* MMSeqs_Clusters_Ranger_Model_1+2+3_Clean.RData
```

5. Build the image with the definition file
```
$ sudo singularity build rafah.sif rafah.def
```

6. [Optional] Sign the image
```
$ singularity sign rafah.sif
```

7. Push it on the cloud
```
$ singulairty push rafah.sif library://papanikos_182/default/rafah:0.1
```

## Usage

```
$ singularity run library://papanikos_182/default/rafah:0.1 RaFaH_v0.1.pl -h
```

