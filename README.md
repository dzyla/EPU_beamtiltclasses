# EPU beam tilt classes
Very simple script (Python 3+) for EPU users who would like to add beam tilt classes to the Refine3D star file

### Script written by Dawid Zyla, ETH Zurich

This script can be used by the EPU users who didn't change names of mrc (mrcs) files. Script adds the particle beam tilt classes into
the Refine3D run_data.star file extracted from the EPU recorded mrc file names. The newly generated file can be imported with Relion 
and used in the Ctfrefine job that should recognise detected classes

Check if your EPU collected files have a name similar to:

FoilHole_30971252_Data_**30970979**_30970980_20181130_1720-32039.mrc **(beam tilt class)**


![alttext](https://github.com/dzyla/EPU_beamtiltclasses/blob/master/btc_EPU.jpg)
