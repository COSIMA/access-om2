ACCESS-OM
=========

The Australian Community Coupled Earth System Simulator Climate Model (ACCESS-CM) is a coupled climate model with several configurations:

- An ocean only configuration consisting of MOM (www.mom-ocean.org), CICE (http://oceans11.lanl.gov/drupal/CICE) and a data driven atmosphere coupled together with OASIS3-MCT (https://verc.enes.org/oasis).
- A climate configuration as above but with a dynamic atmosphere component.

This repository contains the ocean only configuration, which is called ACCESS-OM. To run the climate configuration visit the Climate and Weather Science Laboratory at cwslab.nci.org.au

Prerequisites
-------------

This model needs the following software to run:
    * the Payu experiment management tool (http://payu.readthedocs.org/en/latest/).
    * a fortran compiler such as gfortran or intel-fc
    * an MPI implementation such as OpenMPI.

Install
-------

The first step to installing this model is to create the directory structure and download standard experiments and their input data. The setup.py script can do this for you:

    $ setup.py --download_input_data

Then run some tests to make sure the above step suceeded and the prerequisite software exists.

    $ nosetests test/test_prerequisites.py

Compile
-------

Payu will download and compile the model components based on information provided in the experiment configs. To compile the models for a particular experiment:

    $ cd experiments/access/<experiment>
    $ payu build --laboratory <full_path_to_lab_directory>

Once this has finished check that you have mom, cice and matm executables in lab/bin.

Run
---

Testing
-------


