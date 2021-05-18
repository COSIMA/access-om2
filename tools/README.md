
# Tools

This directory contains a collection of tools which are used to make model input files.


## make\_remap\_weights.py

This tool read the atmosphere and ice/ocean grid definitions and creates remapping weights files. These are used by the coupler to interpolate the fields between the model grids. The tool needs to be invoked once for each pair of grids and by default will create two weights files - one for conservative interpolation and one for patch interpolation.

For example to create 1 deg JRA55 weights on a Gadi (NCI.org.au) head node:

```
module use /g/data3/hh5/public/modules
module load conda/analysis27-18.10
module load nco
module load openmpi
python ./make_remap_weights.py --help
```

Now to create the atmosphere to ice/ocean weights:

```
python ./make_remap_weights.py /g/data/qv56/replicas/input4MIPs/CMIP6/OMIP/MRI/MRI-JRA55-do-1-4-0/atmos/3hr/rsds/gr/v20190429/rsds/rsds_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_195801010130-195812312230.nc JRA55 /g/data/ik11/inputs/access-om2/input_rc/mom_1deg/ MOM1
```

The above should result in two files in the currect directory: `JRA55_MOM1_conserve.nc` and `JRA55_MOM1_patch.nc`

The following will create the weights needed for river runoff:

```
python ./make_remap_weights.py /g/data/qv56/replicas/input4MIPs/CMIP6/OMIP/MRI/MRI-JRA55-do-1-4-0/land/day/friver/gr/v20190429/friver_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_19580101-19581231.nc JRA55_runoff /g/data/ik11/inputs/access-om2/input_rc/mom_1deg/ MOM1
```

The 0.25 deg weights can also be created on the head nodes - this ususally takes a few minutes:

```
python ./make_remap_weights.py /g/data/qv56/replicas/input4MIPs/CMIP6/OMIP/MRI/MRI-JRA55-do-1-4-0/atmos/3hr/rsds/gr/v20190429/rsds_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_195801010130-195812312230.nc JRA55 /g/data/ik11/inputs/access-om2/input_rc/mom_025deg/ MOM025
python ./make_remap_weights.py /g/data/qv56/replicas/input4MIPs/CMIP6/OMIP/MRI/MRI-JRA55-do-1-4-0/land/day/friver/gr/v20190429/friver_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_19580101-19581231.nc JRA55_runoff /g/data/ik11/inputs/access-om2/input_rc/mom_025deg/ MOM025
```

To make the 0.1 deg weights we need to use more PEs and memory, first get an interactive job with lots of memory:

```
qsub -I -P v45 -q normal -lncpus=96 -lmem=348Gb -lwalltime=3:00:00 -lstorage=gdata/ua8+gdata/qv56+gdata/hh5+gdata/ik11
```

Then run the following commands, note the use of `--npes 96`.

```
cd access-om2/tools
module use /g/data3/hh5/public/modules
module load conda/analysis27-18.10
module load nco
module load openmpi
time python ./make_remap_weights.py /g/data/qv56/replicas/input4MIPs/CMIP6/OMIP/MRI/MRI-JRA55-do-1-4-0/atmos/3hr/rsds/gr/v20190429/rsds_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_195801010130-195812312230.nc JRA55 /g/data/ik11/inputs/access-om2/input_rc/mom_01deg/ MOM01 --npes 96

```


