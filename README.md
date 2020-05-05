
| Build | Fast Run | Full Run | Repro | Tools | Release | PEP8 |
|:-------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|
| [![Build Status](https://accessdev.nci.org.au/jenkins/buildStatus/icon?job=ACCESS-OM2/build)](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/build/) | [![Fast Run Status](https://accessdev.nci.org.au/jenkins/buildStatus/icon?job=ACCESS-OM2/fast_run)](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/fast_run/) | [![Full Run Status](https://accessdev.nci.org.au/jenkins/buildStatus/icon?job=ACCESS-OM2/full_run)](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/full_run/) | [![Repro Status](https://accessdev.nci.org.au/jenkins/buildStatus/icon?job=ACCESS-OM2/reproducibility)](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/reproducibility/) | [![Tools Status](https://accessdev.nci.org.au/jenkins/buildStatus/icon?job=ACCESS-OM2/tools)](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/tools/) | [![Release Status](https://accessdev.nci.org.au/jenkins/buildStatus/icon?job=ACCESS-OM2/release)](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/release/) | [![PEP8](https://travis-ci.org/a-parkinson/access-om2.svg?branch=master)](https://travis-ci.org/a-parkinson/access-om2) |

# ACCESS-OM2

ACCESS-OM2 is a global coupled ocean - sea ice model being developed by [COSIMA](http://www.cosima.org.au). Version 1.0 of the model is described in [Kiss et al. (2020)](https://doi.org/10.5194/gmd-13-401-2020). 

ACCESS-OM2 consists of the [MOM 5.1](https://mom-ocean.github.io) ocean model, [CICE 5.1.2](https://github.com/CICE-Consortium/CICE-svn-trunk/tree/cice-5.1.2) sea ice model, and a file-based atmosphere called [YATM](https://github.com/COSIMA/libaccessom2) coupled together using the [OASIS3-MCT v2.0](https://portal.enes.org/oasis) coupler. Regridding is done using [ESMF](https://www.earthsystemcog.org/projects/esmf/) and [KDTREE2](https://github.com/jmhodges/kdtree2). ACCESS-OM2 builds on the ACCESS-OM ([Bi et al., 2013](http://www.bom.gov.au/jshess/docs/2013/bi2_hres.pdf)) and AusCOM ([Roberts et al., 2007](https://50years.acs.org.au/content/dam/acs/50-years/journals/jrpit/JRPIT39.2.137.pdf); [Bi and Marsland, 2010](https://www.cawcr.gov.au/technical-reports/CTR_027.pdf)) models originally developed at [CSIRO](http://www.csiro.au).

ACCESS-OM2 comes with a number of standard configurations in the [control](https://github.com/COSIMA/access-om2/tree/master/control) directory. These include sea ice and ocean at a nominal 1.0, 0.25 and 0.1 degree horizontal grid spacing, forced by [JRA55-do](https://doi.org/10.1016/j.ocemod.2018.07.002) atmospheric reanalyses.

ACCESS-OM2 is being used for a growing number of research projects. A partial list of publications using the model is given [here](https://scholar.google.com/citations?hl=en&view_op=list_works&gmla=AJsN-F5gp3-wpXzF8odo9cFy-9ajlgIeqwrOq_7DvPS1rkETzqmPk1Sfx-gAmIs9kFfRflOR3HqNV_85pJ2j4LljHks1wQtONqiuOVgii-UICb9q2fmTp_w&user=inVqu_4AAAAJ).

# Where to find information

The v1.0 model configurations and performance are described in [Kiss et al. (2020)](https://doi.org/10.5194/gmd-13-401-2020), with further details in the [ACCESS-OM2 technical report](https://github.com/COSIMA/ACCESS-OM2-1-025-010deg-report). Be aware that the latest configurations differ from v1.0 in a number of ways - consult their git histories for details.

Model output can be accessed by [NCI](http://nci.org.au) users via the [COSIMA Cookbook](https://github.com/COSIMA/cosima-cookbook).

For information on downloading and running the model, see the [ACCESS-OM2 wiki](https://github.com/COSIMA/access-om2/wiki). 

**NOTE:** All ACCESS-OM2 model components and configurations are undergoing continual improvement. We strongly recommend that you "watch" this repo (see button at top of screen; ask to be notified of all conversations) and also watch all the [component models](https://github.com/COSIMA/access-om2/tree/master/src), whichever [configuration(s)](https://github.com/COSIMA/access-om2/tree/master/control) you are using, and  [payu](https://github.com/payu-org/payu) to be kept informed of updates, problems and bug fixes as they arise.

Requests for help and other issues associated with the model, tools or configurations can be registered as [ACCESS-OM2 issues](https://github.com/COSIMA/access-om2/issues).
