
| Build | Fast Run | Full Run | Repro | Tools | Release | PEP8 |
|:-------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|
| [![Build Status](https://accessdev.nci.org.au/jenkins/buildStatus/icon?job=ACCESS-OM2/build)](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/build/) | [![Fast Run Status](https://accessdev.nci.org.au/jenkins/buildStatus/icon?job=ACCESS-OM2/fast_run)](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/fast_run/) | [![Full Run Status](https://accessdev.nci.org.au/jenkins/buildStatus/icon?job=ACCESS-OM2/full_run)](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/full_run/) | [![Repro Status](https://accessdev.nci.org.au/jenkins/buildStatus/icon?job=ACCESS-OM2/reproducibility)](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/reproducibility/) | [![Tools Status](https://accessdev.nci.org.au/jenkins/buildStatus/icon?job=ACCESS-OM2/tools)](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/tools/) | [![Release Status](https://accessdev.nci.org.au/jenkins/buildStatus/icon?job=ACCESS-OM2/release)](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/release/) | [![PEP8](https://travis-ci.org/a-parkinson/access-om2.svg?branch=master)](https://travis-ci.org/a-parkinson/access-om2) |

# ACCESS-OM2

ACCESS-OM2 is a global coupled ice ocean model. It is being developed by [COSIMA](http://www.cosima.org.au). It builds on the [ACCESS-OM](https://publications.csiro.au/rpr/pub?pid=csiro:EP125880) model originally developed at [CSIRO](http://www.csiro.au).

The model consists of the [MOM](https://mom-ocean.github.io) ocean model, [CICE](http://oceans11.lanl.gov/trac/CICE) ice model, and a file-based atmosphere called [YATM](https://github.com/OceansAus/libaccessom2) coupled together using the [OASIS3-MCT](https://portal.enes.org/oasis) coupler. Regridding is done using [ESMF](https://www.earthsystemcog.org/projects/esmf/) and [KDTREE2](https://github.com/jmhodges/kdtree2).

ACCESS-OM2 comes with a number of standard configurations. These include ice and ocean at 1.0, 0.25 and 0.1 degree resolution forced by [JRA-55](http://jra.kishou.go.jp/JRA-55/index_en.html)
and [CORE2](http://www.clivar.org/clivar-panels/omdp/core-2) atmospheric reanalyses.

# Where to find information

To find information, start at the [ACCESS-OM2 wiki](https://github.com/OceansAus/access-om2/wiki).

Requests for help and other issues associated with the model, tools or configurations can be registered as [ACCESS-OM2 issues](https://github.com/OceansAus/access-om2/issues).
