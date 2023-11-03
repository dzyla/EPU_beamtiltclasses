import argparse
import shutil
import os
import numpy as np
import re

def extract_matches_from_filename(filename):
    """Extract numbers from the filename if the keyword 'FoilHole' is present."""
    if 'FoilHole' in filename:
        matches = re.findall(r'(?<!\d)\d{6,8}(?!\d)', filename)
        # If there is a leading number in the particle name
        if len(matches) == 6:
            return matches[3]
        # If there is no leading number in the particle name
        elif len(matches) == 5:
            return matches[2]
    return '1'

def make_backup(file_path):
    """Create a backup of the file."""
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    # Generate the backup filename
    base_name, ext = os.path.splitext(file_path)
    backup_name = f"{base_name}_bak{ext}"
    shutil.copy(file_path, backup_name)
    print(f"Backup created: {backup_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a cs file and save with .cs extension.')
    parser.add_argument('--i', type=str, required=True, help='Path to the cs file that needs processing.')

    args = parser.parse_args()
    cs_file_for_ctf = args.i
    
    cs_optics = np.load(cs_file_for_ctf)
    example = cs_optics['blob/path'][0].decode('utf-8')
    example_exp_group = extract_matches_from_filename(os.path.basename(example))
    print(f'Example path: {example}, using: {example_exp_group}')

    exp_groups = np.array([extract_matches_from_filename(os.path.basename(filename.decode('utf-8'))) for filename in cs_optics['blob/path']])
    unique_exp_groups = np.unique(exp_groups)

    print(f'Found {len(unique_exp_groups)} beamtilt classes: {unique_exp_groups}')
    
    exp_group_dict = {unique_exp_group: n+1 for n, unique_exp_group in enumerate(unique_exp_groups)}
    new_exp_groups = np.array([exp_group_dict[exp_group] for exp_group in exp_groups])

    cs_optics['ctf/exp_group_id'] = new_exp_groups

    make_backup(cs_file_for_ctf)

    # Save with the `.cs` extension
    np.save(cs_file_for_ctf, cs_optics, allow_pickle=False)
    os.rename(cs_file_for_ctf+'.npy', cs_file_for_ctf)
    print(f"Saved file as: {cs_file_for_ctf}")