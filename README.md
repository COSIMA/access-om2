# ACCESS-OM

This model consists of MOM5.1, CICE4.1, and a file-based atmosphere called MATM all coupled together with the OASIS3-MCT coupler.

## Prerequisites

The installation of ACCESS-OM depends on the following software:

* git distributed version control software.
* A fortran compiler such as gfortran or intel-fc.
* An MPI implementation such as OpenMPI.
* Python to run the tests.

## Limitations

This software configuration has only been tested on the NCI raijin supercomputer.

## Install

Start by downloading the experiment configurations and the source repositories:

```
git clone --recursive https://github.com/CWSL/access-om.git
cd access-om
```

This should be downloaded to a place which has enough disk space for the model inputs and output.

The next step is to download experiment input data.

```{bash}
./get_input_data.py
```

## Compile

Each model and the OASIS coupler need to be built individually.

Start with OASIS because it is needed by the others:

```
export ACCESS_OM_DIR=$(pwd)
export OASIS_ROOT=$ACCESS_OM_DIR/src/oasis3-mct/
cd $OASIS_ROOT
make
```

Output from the OASIS build can be found in:

```{bash}
less $ACCESS_OM_DIR/src/oasis3-mct/util/make_dir/COMP.log
```

Now compile the ocean, ice and file-based atmosphere.

For ocean:
```{bash}
cd $ACCESS_OM_DIR/src/mom/exp
./MOM_compile.csh --type ACCESS-OM --platform nci
```

For ice:
```{bash}
cd $ACCESS_OM_DIR/src/cice4
./bld/build.sh nci access-om 1440x1080
```

OR, for the 1 deg ocean, ice configuration:

```{bash}
cd $ACCESS_OM_DIR/src/cice4
./bld/build.sh nci access-om 360x300
```

For atm:
```{bash}
cd $ACCESS_OM_DIR/src/matm
./build/build.sh nci
```

Check that the executables exist:

```{bash}
ls $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x
ls $ACCESS_OM_DIR/src/cice4/build_access-om_1440x1080_192p/cice_access-om_1440x1080_192p.exe
ls $ACCESS_OM_DIR/src/matm/build_nt62/matm_nt62.exe
```

## Run

Run the first month of the 0.25 degree CORE2 NYF experiment experiment:

```{bash}
# Make a run script (in this case to run on the NCI HPC system raijin)
cat > run025deg.pbs<<EOF
cd $ACCESS_OM_DIR/025deg/
ln -s ../input/025deg/INPUT ./
cp ../input/025deg/*.nc ./
module load openmpi/1.8.4
mpirun --mca orte_base_help_aggregate 0 -np 960 $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x : -np 192 $ACCESS_OM_DIR/src/cice4/build_access-om_1440x1080_192p/cice_access-om_1440x1080_192p.exe : -np 1 $ACCESS_OM_DIR/src/matm/build_nt62/matm_nt62.exe
EOF
# Submit run script to queuing system (in this case PBSPro)
qsub -P x77 -q normal -v DISPLAY=$DISPLAY,ACCESS_OM_DIR=$ACCESS_OM_DIR -l ncpus=1168,mem=2000Gb,walltime=4:00:00,jobfs=100GB run025deg.pbs 
```

If the run fails or you want to start from scratch for any reason:
```{bash}
qsub -q normal -v DISPLAY=$DISPLAY,ACCESS_OM_DIR=$ACCESS_OM_DIR -l ncpus=1168,mem=2000Gb,walltime=4:00:00,jobfs=100GB run.pbs 
```

To run the 1 degree CORE2 NYF experiment experiment:

```{bash}
# Make a run script (in this case to run on the NCI HPC system raijin)
cat > run1deg.pbs<<EOF
cd $ACCESS_OM_DIR/1deg/
ln -s ../input/1deg/INPUT ./
cp ../input/1deg/*.nc ./
module load openmpi/1.8.4
mpirun --mca orte_base_help_aggregate 0 -np 120 $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x : -np 6 $ACCESS_OM_DIR/src/cice4/build_access-om_360x300_6p/cice_access-om_360x300_6p.exe : -np 1 $ACCESS_OM_DIR/src/matm/build_nt62/matm_nt62.exe
EOF
# Submit run script to queuing system (in this case PBSPro)
qsub -q normal -v DISPLAY=$DISPLAY,ACCESS_OM_DIR=$ACCESS_OM_DIR -l ncpus=128,mem=248Gb,walltime=4:00:00,jobfs=100GB run1deg.pbs 
```

## Verify

TBC.

## Testing

These models and the standard experiments are tested routinely. The test status can be seen here: https://climate-cms.nci.org.au/jenkins/job/ACCESS-CM/

