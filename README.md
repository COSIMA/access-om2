[![Build Status](https://travis-ci.org/a-parkinson/access-om2.svg?branch=master)](https://travis-ci.org/a-parkinson/access-om2)

# ACCESS-OM2 pre-release

ACCESS-OM2 is a coupled ice and ocean global model. It is being developed through a collaboration with [COSIMA](http://www.cosima.org.au), [ARCCSS](http://www.arccss.org.au) and [CSIRO](http://www.csiro.au). It builds on the ACCESS-OM model originally developed at CSIRO [1].

The model consists of [MOM5.1](http://mom-ocean.science), [CICE5.1](http://oceans11.lanl.gov/trac/CICE), and a file-based atmosphere. The models are coupled together using the [OASIS3-MCT](https://portal.enes.org/oasis) coupler and regridding is done using ESMF_RegridWeightGen from [ESMF](https://www.earthsystemcog.org/projects/esmf/) and [KDTREE2](https://github.com/jmhodges/kdtree2).

ACCESS-OM2 comes with a number of standard experiments. These configurations include ice and ocean at 1, 1/4 and 1/10th degree resolution. [JRA-55 v1.3](http://jra.kishou.go.jp/JRA-55/index_en.html) forcing is supported at all three resolutions and [CORE2](http://www.clivar.org/clivar-panels/omdp/core-2) forcing is supported at 1 degree resolution. JRA-55 repeat-year forcing forcing (RYF) and CORE normal-year forcing (NYF) are currently supported, and interannual forcing will be supported soon.

This document describes how to download, compile and run the model. The instructions have only been tested on the [NCI](http://www.nci.org.au) raijin supercomputer.

## Quick start for NCI Raijin users

The following 8 steps will run the 0.25 degree JRA55 RYF experiment.

```{bash}
cd /short/${PROJECT}/${USER}/
mkdir -p access-om2/control
cd access-om2/control
git clone https://github.com/OceansAus/025deg_jra55_ryf.git
cd 025deg_jra55_ryf
```

Edit the `shortpath` line in the `config.yaml` to reflect your ${PROJECT}. Then:

```{bash}
module load payu/dev
payu run
```

It may be necessary to add the `module load payu/dev' to your .bashrc


## Problems?

Please post an issue describing your problem at: https://github.com/OceansAus/access-om2/issues

## References

[1] "ACCESS-OM: the Ocean and Sea ice Core of the ACCESS Coupled Model" https://publications.csiro.au/rpr/pub?pid=csiro:EP125880

