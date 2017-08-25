# ACCESS-OM2 pre-release

ACCESS-OM2 is a coupled ice and ocean global model. It is being developed through a collaborate with [COSIMA](www.cosima.org.au), [ARCCSS](www.arccss.org.au) and [CSIRO](www.csiro.au). It builds on the ACCESS-OM model orinially developed at CSIRO [1].

The model consists of [MOM5.1](mom-ocean.science), [CICE5.1](http://oceans11.lanl.gov/trac/CICE), and a file-based atmosphere. The models are coupled together using the [OASIS3-MCT](https://portal.enes.org/oasis) coupler and regridding is done using ESMF_RegridWeightGen from [ESMF](https://www.earthsystemcog.org/projects/esmf/) and [KDTREE2](https://github.com/jmhodges/kdtree2).

ACCESS-OM2 comes with a number of standard experiments. These configurations include ice and ocean at 1, 1/4 and 1/10th degree resolution. [JRA55](http://jra.kishou.go.jp/JRA-55/index_en.html) and [CORE2](http://www.clivar.org/clivar-panels/omdp/core-2) forcing datasets are supported. These instruction are to build and run the 1 degree configration with JRA55 forcing.

This document describes how to download, compile and run the model. The instructions have only been tested on the [NCI](www.nci.org.au) raijin supercomputer.

## Prerequisites

The ACCESS-OM2 depends on the following software:

* [payu](http://payu.readthedocs.io) run management software.
* git distributed version control software.
* a fortran compiler such as gfortran or intel-fc.
* an MPI implementation such as OpenMPI.
* Python and [pytest](https://docs.pytest.org) to run the tests.

To use JRA55 on NCI you need to be a member of the ua8 project - apply via <https://my.nci.org.au>
## Install

Start by downloading the experiment configurations and the source repositories. This should be downloaded to a place which has enough disk space for the model inputs and output. On raijin it should be downloaded to `/short/${PROJECT}/${USER}`.

```{bash}
cd /short/${PROJECT}/${USER}
git clone --recursive https://github.com/OceansAus/access-om2.git
cd access-om2
```

or if you have an existing download and would like to update to the latest version:

```{bash}
cd access-om2
git pull
git submodule update
```

Now set environment variables. This depends on the shell you're using (type `echo $0` to check; if neither bash nor tcsh, switch to bash with `exec /bin/bash`):

In bash:
```{bash}
export ACCESS_OM_DIR=$(pwd)
export OASIS_ROOT=$ACCESS_OM_DIR/src/oasis3-mct/
```
or in tcsh:
```{tcsh}
setenv ACCESS_OM_DIR `pwd`
setenv OASIS_ROOT $ACCESS_OM_DIR/src/oasis3-mct/
```

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

Now to build each model. There are two ways to do this. If you have pytest installed, an easier way to compile all models is to use the build test:

```
python -m pytest test/test_build.py
```

Otherwise, the models can be build individually. Start with OASIS because it is needed by the others:

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

For ice, note that the CICE build is resolution dependent.
```{bash}
cd $ACCESS_OM_DIR/src/cice5
make
```

To build the 1/4 and 1/10th degree:

```{bash}
cd $ACCESS_OM_DIR/src/cice5
make 025deg
make 01deg
```

For atmosphere:
```{bash}
cd $ACCESS_OM_DIR/src/matm
make jra55
```

## Pre-run setup and checks:
First check that the executables exist:

```{bash}
ls $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x
ls $ACCESS_OM_DIR/src/matm/build_jra55/matm_jra55.exe
```

and whichever of the three CICE resolutions you are using:
```{bash}
ls $ACCESS_OM_DIR/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe
ls $ACCESS_OM_DIR/src/cice5/build_auscom_1440x1080_480p/cice_auscom_1440x1080_480p.exe
ls $ACCESS_OM_DIR/src/cice5/build_auscom_3600x2700_1200p/cice_auscom_3600x2700_1200p.exe
```

You will also have a directory `$ACCESS_OM_DIR/control` whose subdirectories are model configurations at 1, 1/4 and 1/10 degree resolution. `config.yaml` within each of these subdirectories gives the PBS specification for the job, including executable names. Details are here: <http://payu.readthedocs.io/en/latest/config.html>

**You will need to edit `config.yaml` to set  `project` and `shortpath` appropriately.** Service units are charged to `project` and output is saved in `shortpath`.

The executables then need to be copied to the directory `$ACCESS_OM_DIR/bin`.

First copy and rename mppnccombine:
```{bash}
mkdir -p $ACCESS_OM_DIR/bin
cp $ACCESS_OM_DIR/src/mom/bin/mppnccombine.nci $ACCESS_OM_DIR/bin/mppnccombine
```

Now for the model executables. As an added complication, they need to be renamed to match the `exe` names used in the experiment configuration file `config.yaml` --- check this with `grep exe $ACCESS_OM_DIR/control/*/config.yaml` (for uniqueness the name of each executable is changed to include the hash/id of the git commit from which they were built).

All three JRA55 models need this (but **you may need to update the hash/ids**):
```{bash}
cp $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x $ACCESS_OM_DIR/bin/fms_ACCESS-OM_160db8a0.x
cp $ACCESS_OM_DIR/src/matm/build_jra55/matm_jra55.exe $ACCESS_OM_DIR/bin/matm_jra55_2318e909.exe
```
plus one of the following:

For the 1 degree JRA55 model (but **you may need to update the hash/id**):
```{bash}
cp $ACCESS_OM_DIR/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe $ACCESS_OM_DIR/bin/cice_auscom_360x300_24p_fe730022.exe
```

For the 1/4 degree JRA55 model (but **you may need to update the hash/id**):
```{bash}
cp $ACCESS_OM_DIR/src/cice5/build_auscom_1440x1080_480p/cice_auscom_1440x1080_480p.exe $ACCESS_OM_DIR/bin/cice_auscom_1440x1080_480p_fe730022.exe
```

For the 1/10 degree JRA55 model (but **you may need to update the hash/id**):
```{bash}
cp $ACCESS_OM_DIR/src/cice5/build_auscom_3600x2700_1200p/cice_auscom_3600x2700_1200p.exe $ACCESS_OM_DIR/bin/cice_auscom_3600x2700_1200p_fe730022.exe
```

For the 1 degree CORE2 model (but **you may need to update the hash/ids**):
```{bash}
cp $ACCESS_OM_DIR/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe $ACCESS_OM_DIR/bin/cice_auscom_360x300_24p_fe730022.exe
cp $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x $ACCESS_OM_DIR/bin/fms_ACCESS-OM_160db8a0.x
cp $ACCESS_OM_DIR/src/matm/build_nt62/matm_nt62.exe $ACCESS_OM_DIR/bin/matm_nt62_b3a80f3b.exe
```

### load payu
[payu](http://payu.readthedocs.io)  needs to be available. On NCI you just do:
```{bash}
module load payu/dev
```

## Run

Each of the model configurations is run by payu from within its respective directory in `$ACCESS_OM_DIR/control/`.

For example, to run the 1 degree JRA55 RYF experiment:
```{bash}
cd $ACCESS_OM_DIR/control/1deg_jra55_ryf/
payu run
```

On NCI, status of submitted runs can be checked with `qstat -u ${USER}`.

See <http://payu.readthedocs.io/en/latest/design.html> for explanation of where run output is stored.

See <http://payu.readthedocs.io/en/latest/usage.html> for how to continue additional runs from restarts.

## Testing

These models and the standard experiments are tested routinely. The test status can be seen here: https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/

## Problems?

Please post an issue describing your problem at: https://github.com/OceansAus/access-om2/issues

## Releases

- pre-release: 5a1f28d56ab06c12a495c21af10cb55913bdba0b
- pre-release bugfix: 8fe4429a46de61c27b74736300cad5998cdc9836
    Containing, among others, the following changes/fixes: https://github.com/mom-ocean/MOM5/issues/175, https://github.com/mom-ocean/MOM5/issues/183, https://github.com/mom-ocean/MOM5/issues/184, https://github.com/OceansAus/access-om2/issues/13, https://github.com/OceansAus/access-om2/issues/12, https://github.com/OceansAus/access-om2/issues/11, https://github.com/mom-ocean/MOM5/issues/187
- pre-release runoff spread: 0588afcb3df1737ae04829609c272ef1e590b807
- pre-release salt fix:

## References

[1] "ACCESS-OM: the Ocean and Sea ice Core of the ACCESS Coupled Model" https://publications.csiro.au/rpr/pub?pid=csiro:EP125880

