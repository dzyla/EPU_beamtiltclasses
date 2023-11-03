import pandas as pd
import numpy as np
import re
from gemmi import cif
import argparse
import sys
import os

def parse_star(file_path):
    """Parse a star file and return its contents as a dictionary of dataframes."""
    doc = cif.read_file(file_path)
    star_data = {}

    for data in doc:
        dataframe = pd.DataFrame()
        try:
            for item in data:
                for metadata in item.loop.tags:
                    value = data.find_loop(metadata)
                    dataframe[metadata] = np.array(value)
            star_data[data.name] = dataframe
        except AttributeError:
            continue

    return star_data

def extract_matches_from_filename(filename):
    """Extract three numbers from the filename if the keyword 'FoilHole' is present."""
    if 'FoilHole' in filename:
        matches = re.findall(r'(\d+)', filename)
        if len(matches) >= 3:
            return matches[0:3]
    return [1, 1, 1]


def find_beamtilt_classes(particles_star):
    """Find beamtilt classes from the given star dataframe."""
    mic_names = particles_star.get('_rlnMicrographName', [])
    extracted_values = [extract_matches_from_filename(name) for name in mic_names]
    
    pos1, pos2, pos3 = zip(*extracted_values)
    
    unique_p3 = np.unique(pos3)
    print(f"Found {len(unique_p3)} beamtilt classes at positions 3 in the filenames")
    return pos3


def generate_beamtilt_optics(optics, beamtilt_classes):
    # Get the unique beamtilt classes
    unique_beamtilt_classes = np.unique(beamtilt_classes)
    print(unique_beamtilt_classes)

    # Create a dictionary mapping unique beamtilt classes to optics group numbers
    optics_name_group_dict = {unique_beamtilt_class: n+1 for n, unique_beamtilt_class in enumerate(unique_beamtilt_classes)}

    optics_holder = pd.DataFrame()

    # Iterate over unique beamtilt classes and update optics data
    for n, unique_beamtilt_class in enumerate(unique_beamtilt_classes):
        # If there's only one row in optics, create a copy of it
        if optics.shape[0] == 1:
            new_optics_group = optics.copy()
        else:
            new_optics_group = optics.iloc[n].copy()

        # Update the optics group name and number
        new_optics_group['_rlnOpticsGroupName'] = unique_beamtilt_class
        new_optics_group['_rlnOpticsGroup'] = optics_name_group_dict[unique_beamtilt_class]
        
        # Append the new optics group to the holder dataframe
        optics_holder = pd.concat([optics_holder, new_optics_group], axis=0)

    # Reset the index after concatenation
    optics_holder = optics_holder.reset_index(drop=True)

    return optics_holder, optics_name_group_dict


def update_beamtilt_classes(particles_star, beamtilt_dict):
    """Update the particles star dataframe with the beamtilt classes."""
    mic_names = particles_star['_rlnMicrographName']
    
    beamtilt_classes = [extract_matches_from_filename(name)[2] for name in mic_names]
    optics_group = [beamtilt_dict[cls] for cls in beamtilt_classes]
    
    particles_star['_rlnOpticsGroup'] = optics_group
    return particles_star


def save_star(dicts_of_df, filename='out.star'):
    out_doc = cif.Document()

    for element in dicts_of_df.keys():
        out_particles = out_doc.add_new_block(element, pos=-1)
        
        # Ensure that the object is a DataFrame
        if isinstance(dicts_of_df[element], pd.DataFrame):
            column_names = dicts_of_df[element].columns
        else:
            raise TypeError(f"The object for key '{element}' is not a DataFrame.")
        
        column_names_to_star = [f"{name} #{n + 1}" for n, name in enumerate(column_names)]
        loop = out_particles.init_loop('', column_names_to_star)
        data_rows = dicts_of_df[element].to_numpy().astype(str).tolist()

        for row in data_rows:
            loop.add_row(row)

    out_doc.write_file(filename)
    print(f'Saved star file: {filename}')

def main(args):
    # Check if input and output file names are the same
    if args.i == args.o:
        print("Error: Input and output filenames are the same. Exiting to avoid overwriting.")
        sys.exit(1)
        
    
    print(f"Processing input file: {args.i}")

    data_star = parse_star(args.i)
    particles = data_star['particles']
    optics = data_star['optics']

    per_particle_beamtilt_class = find_beamtilt_classes(particles)
    new_optics, optics_dict = generate_beamtilt_optics(optics, per_particle_beamtilt_class)
    
    new_particles = update_beamtilt_classes(particles, optics_dict)
    
    save_star({'optics': new_optics, 'particles': new_particles}, args.o)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a star file to find beamtilt classes.")
    
    # Input file argument
    parser.add_argument("--i", type=str, required=True, help="Path to the input star file.")
    
    # Output file argument
    parser.add_argument("--o", type=str, required=True, help="Path to the output file.")
    
    args = parser.parse_args()
    main(args)
    
    