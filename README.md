# EPU beam tilt classes
Very simple script for EPU users which adds beam tilt classes to the Refine3D star file

### Script written by Dawid Zyla, ETH Zurich

This script can be used by the EPU users who didn't change names of mrc files to include the beam tilt classes into
the Refine3D run_data.star file. The newly generated file can be imported with Relion 
and used in the Ctfrefine job which will recognise detected classes

Check if your EPU collected files have a name similar to:

FoilHole_30971252_Data_**30970979**_30970980_20181130_1720-32039.mrc **(beam tilt class)**
