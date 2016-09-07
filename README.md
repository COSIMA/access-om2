ACCESS-OM
=========

This model consists of MOM5.1, CICE4.1, and a file-based atmosphere called MATM all coupled together with the OASIS3-MCT coupler.

Prerequisites
-------------

This model needs the following software to run:

* git distributed version control software.
* A Python installation.
* A fortran compiler such as gfortran or intel-fc.
* An MPI implementation such as OpenMPI.

Install
-------

Start by downloading the experiment configurations and the source repositories:

```
$ git clone --recursive https://github.com/CWSL/access-om.git
```

This should be downloaded to a place which has enough disk space for the model inputs and output.

The next step is to download experiment input data.

```
$ setup.py --download_input_data
```

Then run some tests to make sure the above steps suceeded.

```
$ nosetests test/test_download.py
```

Compile
-------

Each model and the OASIS coupler need to be built individually.

Start with OASIS because it is needed by the others:

```
$ export ACCESS_OM_DIR=<full path to access-om dir>
$ export OASIS_ROOT=$ACCESS_OM_DIR/src/oasis3-mct/
$ cd $OASIS_ROOT
$ make
```

Now compile the ocean, ice and file-based atmosphere. These can be done in parallel. It's probably best to do them in separate terminals in case there is an error.

For ocean:
```
$ cd $ACCESS_OM_DIR/src/mom/exp
$ ./MOM_compile.csh --type ACCESS_OM --platform ubuntu
```

For ice:
```
$ cd $ACCESS_OM_DIR/src/cice4
$ ./bld/build.sh ubuntu access-om 360x300
```
or for another platform:
```
$ ./bld/build.sh nci access-om 360x300
```

For atm:
```
$ cd $ACCESS_OM_DIR/src/matm
$ ./build/build.sh ubuntu
```

Once this has finished check that the mom, cice and matm executables exist.

If the build fails then it is probably because the build process is not configured for your particular platform. You may have to edit the individual build configurations in src/\<model\>/.

Now run tests to ensure that this step succeeded:

```
$ nosetests test/test_build.py
```

Run
---

Then to run an experiment:

    $ cd 025deg
    $ mkdir RESTART
    $ mpirun -


Verify
------

To verify a successful run from above...

```
$ nosetests test/test_run.py
```

Testing
-------

These models and the standard experiments are tested routinely. The test status can be seen here: https://climate-cms.nci.org.au/jenkins/job/ACCESS-CM/

