import re

'''
Script written by Dawid Zyla, ETH Zurich

This script can be used by the EPU users who didn't change names of mrc (mrcs) files. Script adds the particle beam tilt 
classes into the Refine3D run_data.star file extracted from the EPU recorded mrc file names. The newly generated file 
can be imported with Relion and used in the Ctfrefine job that should recognise detected classes

Check if your EPU collected files have a name similar to:

FoilHole_30971252_Data_30970979_30970980_20181130_1720-32039.mrc
                       ********
                       BeamTiltClass
'''

# place here the path of the last refinement run_data.star file
_3drefine_run_data_path = 'Refine3D/job001/run_data.star'

try:
    with open(_3drefine_run_data_path, 'r') as particles:
        out = open('run_data_beamtilt_classes.star', 'w+')

        print('Reading {}...'.format(_3drefine_run_data_path))

        header = True
        for n, particle in enumerate(particles):

            # to skip the first lines of the star file
            if n > 3:

                # Get the line numbers from the descriptions
                if particle[:1] == '_':
                    particle_ = particle.replace(' ', '').replace('\n', '')
                    header = True
                    last_line = int(particle_[-2:].replace('#', ''))

                else:
                    if header == True:
                        # save beamtiltclass header and indicate that the header is over
                        print('_rlnBeamTiltClass #{}'.format(last_line + 1), file=out)
                        header = False

                if header == False:

                    # You might want to change the number for the proper location of the filename
                    try:
                        mrc_file_name = particle.split()[10]
                    except IndexError:
                        pass

                    # find the 8 digit pattern in the file name
                    pattern = re.compile('[\d]{8}')

                    # if found the 8 digit pattern, take the second which indicated the beam tilt classes
                    beam_tilt_class = pattern.findall(mrc_file_name)[1]

            if header:

                # save header lines
                print(particle.replace('\n', ''), file=out)

            else:
                if len(particle) > 10:

                    # save lines with the beam tilt classes
                    print(particle.replace('\n', '') + '    {}'.format(beam_tilt_class), file=out)

                else:
                    print(particle.replace('\n', ''), file=out)

except FileNotFoundError:
    print('\nRefine3D file path is wrong. Please provide the proper path')

print('\n\nAdding beam tilt classes finished! Now import run_data_beamtilt_classes.star with Relion and run CtfRefine')
