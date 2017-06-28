# ACCESS-OM2 pre-release

ACCESS-OM2 is a coupled ice and ocean global model. It is being developed through a collaborate with [COSIMA](www.cosima.org.au), [ARCCSS](www.arccss.org.au) and [CSIRO](www.csiro.au). It builds on the ACCESS-OM model orinially developed at CSIRO [1].

The model consists of [MOM5.1](mom-ocean.science), [CICE5.1](http://oceans11.lanl.gov/trac/CICE), and a file-based atmosphere. The models are coupled together using the [OASIS3-MCT](https://portal.enes.org/oasis) coupler and regridding is done using ESMF_RegridWeightGen from [ESMF](https://www.earthsystemcog.org/projects/esmf/) and [KDTREE2](https://github.com/jmhodges/kdtree2).

ACCESS-OM2 comes with a number of standard experiments. These configurations include ice and ocean at 1, 1/4 and 1/10th degree resolution. [JRA55](http://jra.kishou.go.jp/JRA-55/index_en.html) and [CORE2](http://www.clivar.org/clivar-panels/omdp/core-2) forcing datasets are supported.

This document describes how to download, compile and run the model. The instructions have only been tested on the [NCI](www.nci.org.au) raijin supercomputer.

## Prerequisites

The ACCESS-OM2 depends on the following software:

* [payu](http://payu.readthedocs.io) run management software.
* git distributed version control software.
* a fortran compiler such as gfortran or intel-fc.
* an MPI implementation such as OpenMPI.
* Python and pytest to run the tests.

## Install

Start by downloading the experiment configurations and the source repositories:

```{bash}
cd /short/${PROJECT}/${USER}
git clone --recursive https://github.com/OceansAus/access-om2.git
cd access-om2
```

This should be downloaded to a place which has enough disk space for the model inputs and output. On raijin it should be downloaded to `/short/${PROJECT}/${USER}

The next step is to create the 'lab' by downloading experiment input data and creating directories.

```{bash}
./get_input_data.py
mkdir -p bin
```

If the above script does not work for any reason the input can be setup manually with:

```{bash}
cp /short/public/access-om2/input_b8053e87.tar.gz ./
tar zxvf input_b8053e87.tar.gz
```

## Compile

Now to build each model. Start with OASIS because it is needed by the others:

```
export ACCESS_OM_DIR=$(pwd)
export OASIS_ROOT=$ACCESS_OM_DIR/src/oasis3-mct/
cd $OASIS_ROOT
make
```

Now compile the ocean, ice and file-based atmosphere.

For ocean:
```{bash}
cd $ACCESS_OM_DIR/src/mom/exp
./MOM_compile.csh --type ACCESS-OM --platform nci
```

For ice:
```{bash}
cd $ACCESS_OM_DIR/src/cice5
make
```

Note that the CICE build is resolution dependent. To build the 1/4 and 1/10th degree:

```{bash}
cd $ACCESS_OM_DIR/src/cice5
make 025deg
make 01deg
```

For atm:
```{bash}
cd $ACCESS_OM_DIR/src/matm
make jra55
```

Alternatively, if you have pytest installed, an easier way to compile all models is to use the build test:

```
python -m pytest test/test_build.py
```

Now check that the executables exist:

```{bash}
ls $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x
ls $ACCESS_OM_DIR/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe
ls $ACCESS_OM_DIR/src/matm/build_jra55/matm_jra55.exe
```

These then need to be copied to the bin directory created above. Also, as an added complication, they need to be renamed to match the names used in the experiment configuration file `config.yaml`. The name of each executable is changed to include the hash/id of the git commit from which they were built. The following should do the trick:

```{bash}
ls $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x $ACCESS_OM_DIR/bin/fms_ACCESS-OM_55a1bd92.x
ls $ACCESS_OM_DIR/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe $ACCESS_OM_DIR/bin/cice_auscom_360x300_24p_fb3693fe.exe
ls $ACCESS_OM_DIR/src/matm/build_jra55/matm_jra55.exe $ACCESS_OM_DIR/bin/matm_jra55_77ca58ce.exe
```

## Run

To run the 1 degree JRA55 RYF experiment:

```{bash}
cd $ACCESS_OM_DIR/1deg_jra55_ryf/
payu run
```

## Testing

These models and the standard experiments are tested routinely. The test status can be seen here: https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/

## Problems?

Please contact post an issue describing your problem at: https://github.com/OceansAus/access-om2/issues

## References

[1] "ACCESS-OM: the Ocean and Sea ice Core of the ACCESS Coupled Model" https://publications.csiro.au/rpr/pub?pid=csiro:EP125880

