# ACCESS-OM

This model consists of MOM5.1, CICE4.1, and a file-based atmosphere called MATM all coupled together with the OASIS3-MCT coupler.

## Prerequisites

This model needs the following software to run:

* git distributed version control software.
* A fortran compiler such as gfortran or intel-fc.
* An MPI implementation such as OpenMPI.
* Python to run the tests.

## Limitations

This software has only been tested on NCI raijin supercomputer.

## Install

Start by downloading the experiment configurations and the source repositories:

```
$ git clone --recursive https://github.com/CWSL/access-om.git
$ cd access-om
```

This should be downloaded to a place which has enough disk space for the model inputs and output.

The next step is to download experiment input data.

```{bash}
$ ./get_data.py
```

## Compile

Each model and the OASIS coupler need to be built individually.

Start with OASIS because it is needed by the others:

```
$ export ACCESS_OM_DIR=$(pwd)
$ export OASIS_ROOT=$ACCESS_OM_DIR/src/oasis3-mct/
$ cd $OASIS_ROOT
$ make
```

Output from the OASIS build can be found in:

```{bash}
$ less $ACCESS_OM_DIR/src/oasis3-mct/util/make_dir/COMP.log
```

Now compile the ocean, ice and file-based atmosphere.

For ocean:
```{bash}
$ cd $ACCESS_OM_DIR/src/mom/exp
$ ./MOM_compile.csh --type ACCESS-OM --platform nci
```

For ice:
```{bash}
$ cd $ACCESS_OM_DIR/src/cice4
$ ./bld/build.sh nci access-om 1440x1080
```

For atm:
```{bash}
$ cd $ACCESS_OM_DIR/src/matm
$ ./build/build.sh nci
```

Now run check that the executables exist:

```{bash}
$ ls $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x
$ ls $ACCESS_OM_DIR/cice4/build_access-om_1440x1080_192p/cice_access-om_1440x1080_192p.exe
$ ls $ACCESS_OM_DIR/src/matm/build_nt62/matm_nt62.exe
```

## Run

Run an experiment:

```{bash}
$ qsub -I -P x77 -q normal -v DISPLAY=$DISPLAY,ACCESS_OM_DIR=$ACCESS_OM_DIR -l ncpus=1168,mem=2000Gb,walltime=4:00:00,jobfs=100GB
$ cd $ACCESS_OM_DIR/025deg/
$ ln -s ../input/025deg/INPUT ./
$ cp ../input/025deg/*.nc ./
$ module load openmpi/1.8.4
$ mpirun --mca orte_base_help_aggregate 0 -np 960 $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x : -np 192 $ACCESS_OM_DIR/src/cice4/build_access-om_1440x1080_192p/cice_access-om_1440x1080_192p.exe : -np 1 $ACCESS_OM_DIR/src/matm/build_nt62/matm_nt62.exe
```

If the run fails or you want to start from scratch for any reason then it's necessary to copy over the OASIS inputs again because these may have been corrupted/written over:
```{bash}
$ cd $ACCESS_OM_DIR/025deg/
$ cp ../input/025deg/*.nc ./
```

```{bash}


## Verify

TBC.

## Testing

These models and the standard experiments are tested routinely. The test status can be seen here: https://climate-cms.nci.org.au/jenkins/job/ACCESS-CM/

