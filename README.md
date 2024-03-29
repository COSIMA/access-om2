<img src="https://github.com/COSIMA/logo/blob/master/png/logo_word.png" width="800"/>
<br/> <br/>

# ACCESS-OM2

ACCESS-OM2 is a global coupled ocean - sea ice model being developed by [COSIMA](http://www.cosima.org.au).

ACCESS-OM2 consists of the [MOM 5.1](https://mom-ocean.github.io) ocean model, [CICE 5.1.2](https://github.com/CICE-Consortium/CICE-svn-trunk/tree/cice-5.1.2) sea ice model, and a file-based atmosphere called [YATM](https://github.com/COSIMA/libaccessom2) coupled together using [OASIS3-MCT v2.0](https://portal.enes.org/oasis). ACCESS-OM2 builds on the ACCESS-OM ([Bi et al., 2013](http://www.bom.gov.au/jshess/docs/2013/bi2_hres.pdf)) and AusCOM ([Roberts et al., 2007](https://50years.acs.org.au/content/dam/acs/50-years/journals/jrpit/JRPIT39.2.137.pdf); [Bi and Marsland, 2010](https://www.cawcr.gov.au/technical-reports/CTR_027.pdf)) models originally developed at [CSIRO](http://www.csiro.au).

ACCESS-OM2 comes with a number of standard configurations in the [control](https://github.com/COSIMA/access-om2/tree/master/control) directory. These include sea ice and ocean at a nominal 1.0, 0.25 and 0.1 degree horizontal grid spacing, forced by [JRA55-do](https://doi.org/10.1016/j.ocemod.2018.07.002) atmospheric reanalyses.

ACCESS-OM2 is being used for a growing number of research projects. A partial list of publications using the model is given [here](https://scholar.google.com/citations?hl=en&view_op=list_works&gmla=AJsN-F5gp3-wpXzF8odo9cFy-9ajlgIeqwrOq_7DvPS1rkETzqmPk1Sfx-gAmIs9kFfRflOR3HqNV_85pJ2j4LljHks1wQtONqiuOVgii-UICb9q2fmTp_w&user=inVqu_4AAAAJ).

# Downloading

This repository contains many submodules, so you will need to clone it with the `--recursive` flag:
```
git clone --recursive https://github.com/COSIMA/access-om2.git
```

To update a previous clone of this repository to the latest version, you will need to do 
```
git pull
```
followed by
```
git submodule update --init --recursive
```
to update all the submodules.

# Where to find information

The v1.0 model code, configurations and performance were described in [Kiss et al. (2020)](https://doi.org/10.5194/gmd-13-401-2020), with further details in the draft [ACCESS-OM2 technical report](https://github.com/COSIMA/ACCESS-OM2-1-025-010deg-report). The current code and configurations differ from v1.0 in a number of ways (biogeochemistry, updated forcing, improvements and bug fixes), as described by [Solodoch et al. (2022)](https://doi.org/10.1029/2021GL097211), [Hayashida et al. (2023)](https://dx.doi.org/10.1029/2023JC019697), [Menviel et al. (2023)](https://doi.org/10.5194/egusphere-2023-390) and [Wang et al. (2023)](https://doi.org/10.5194/gmd-2023-123).
 
Model output can be accessed by [NCI](http://nci.org.au) users via the [COSIMA Cookbook](https://github.com/COSIMA/cosima-cookbook).

For information on downloading, building and running the model, see the [ACCESS-OM2 wiki](https://github.com/COSIMA/access-om2/wiki). 

**NOTE:** All ACCESS-OM2 model components and configurations are undergoing continual improvement. We strongly recommend that you "watch" this repo (see button at top of screen; ask to be notified of all conversations) and also watch all the [component models](https://github.com/COSIMA/access-om2/tree/master/src), whichever [configuration(s)](https://github.com/COSIMA/access-om2/tree/master/control) you are using, and [`payu`](https://github.com/payu-org/payu) to be kept informed of updates, problems and bug fixes as they arise.

Requests for help and other issues associated with the model, tools or configurations can be registered as [ACCESS-OM2 issues](https://github.com/COSIMA/access-om2/issues).

## Conditions of use

We request that users of this or other ACCESS-OM2 model code:
1. consider citing Kiss et al. (2020) ([http://doi.org/10.5194/gmd-13-401-2020](http://doi.org/10.5194/gmd-13-401-2020)), and also the other [papers above](https://github.com/COSIMA/access-om2#where-to-find-information) detailing more recent improvements to the model
2. include an acknowledgement such as the following:

   *The authors thank the Consortium for Ocean-Sea Ice Modelling in Australia (COSIMA; [http://www.cosima.org.au](http://www.cosima.org.au)) for making the ACCESS-OM2 suite of models available at [https://github.com/COSIMA/access-om2](https://github.com/COSIMA/access-om2).*
3. let us know of any publications which use these models or data so we can add them to [our list](https://scholar.google.com/citations?hl=en&user=inVqu_4AAAAJ).
