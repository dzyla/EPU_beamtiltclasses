# EPU beam tilt classes
A simple (updated) script that uses the third position in the EPU micrograph file name (e.g., FoilHole_10218182_Data_10216707_**10216709**_20231010_225333_fractions.tiff) for beam tilt class. The script updates the optics part of the Relion 3+ data star file and saves a new modified star. Whether this modification affects the resolution is yet to be determined.

# Requirements
* Python
* Particle star file
* EPU recorded micrographs that have the original name

# Included: 
Python script and Jupyter Notebook.

# Not tested:
* Initial multiple optic groups
* ?

# Usage: 
`python find_beamtilt_classes.py --i /mnt/gpu_scratch/Extract/job027/particles.star --o /mnt/gpu_scratch/Extract/job027/particles_beamtilt.star`

# Requirements:
`pip install pandas gemmi numpy`

# Proof-of-Principle
X and Y values obtained from XML files

Color from the 3rd number in the EPU

![beatilt_class](https://github.com/dzyla/EPU_beamtiltclasses/assets/20625527/099c368c-6eae-42ef-a4b8-4c347994b6f9)


# Author:
Dawid Zyla, La Jolla Institute for Immunology
