[![Build Status](https://travis-ci.org/a-parkinson/access-om2.svg?branch=master)](https://travis-ci.org/a-parkinson/access-om2)

# ACCESS-OM2

ACCESS-OM2 is a coupled ice and ocean global model. It is being developed through a collaboration with [COSIMA](http://www.cosima.org.au), [ARCCSS](http://www.arccss.org.au) and [CSIRO](http://www.csiro.au). It builds on the ACCESS-OM model originally developed at CSIRO [1].

The model consists of [MOM5.1](http://mom-ocean.science), [CICE5.1](http://oceans11.lanl.gov/trac/CICE), and a file-based atmosphere called [YATM](https://github.com/OceansAus/libaccessom2) coupled together using the [OASIS3-MCT](https://portal.enes.org/oasis). Regridding is done using [ESMF](https://www.earthsystemcog.org/projects/esmf/) and [KDTREE2](https://github.com/jmhodges/kdtree2).

ACCESS-OM2 comes with a number of standard configurations, these include ice and ocean at 1, 1/4 and 1/10th degree resolution forced by [JRA-55](http://jra.kishou.go.jp/JRA-55/index_en.html)
and [CORE2](http://www.clivar.org/clivar-panels/omdp/core-2) atmospheric reanalyses.

# Where to find information

To find information, start at the [ACCESS-OM2 wiki](https://github.com/OceansAus/access-om2/wiki)

Requests for help and other issues associated with the model, tools or configurations can be registered as [ACCESS-OM2 issues](https://github.com/OceansAus/access-om2/issues)

# References

[1] "ACCESS-OM: the Ocean and Sea ice Core of the ACCESS Coupled Model" https://publications.csiro.au/rpr/pub?pid=csiro:EP125880

