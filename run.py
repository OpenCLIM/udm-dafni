import os
from shutil import copyfile
import subprocess
import datetime
subprocess.run(['python', '-m',  'openudm', '/data/inputs'])

from os import getenv, walk, mkdir, remove, listdir
from os.path import join, isdir, isfile

def find_files():
    """
    Search all directories for any input files
    """

    suitable_extension_types = ['asc', 'tiff', 'geotiff', 'gpkg', 'csv']

    input_files = []

    for root, dirs, files in walk('/data'):
        print(root, files)
        for file in files:

            # check if extension acceptable
            #extension = file.split('.')[-1]
            #if extension in suitable_extension_types:
                # file is good and what we are looking for
            input_files.append(join(file))

    print(input_files)
    return input_files


print(find_files())


# move files to output dir
result_data_dir = '/data/inputs'
output_data_dir = '/data/outputs/data'
buildings_data_dir = '/data/outputs/buildings'

# make output dir if not exists
os.makedirs(output_data_dir, exist_ok=True)

# copy the listed output files to the output location
files_to_copy = ['out_cell_dev.asc', 'out_cell_pph.asc', 'out_cell_dph.asc', 'out_cell_suit.asc']
for file_name in files_to_copy:
    copyfile(os.path.join(result_data_dir, file_name), os.path.join(output_data_dir, file_name))


# make output dir if not exists
os.makedirs(buildings_data_dir, exist_ok=True)
urban_fabric_raster = os.path.join(output_data_dir, 'out_uf.asc')
subprocess.run(['generate_urban_fabric', '-i', '/data/inputs/out_cell_dph.asc', '-o', urban_fabric_raster])
subprocess.run(['raster_to_vector', '-i', urban_fabric_raster, '-o',
                os.path.join(buildings_data_dir, "urban_fabric.gpkg"), '-f' 'buildings'])
