import os
from shutil import copyfile
import subprocess
subprocess.run(['python', '-m',  'openudm', '/data/inputs/data'])

# move files to output dir
result_data_dir = '/data/inputs/data'
output_data_dir = '/data/outputs/data'
buildings_data_dir = '/data/outputs/buildings'

# make output dir if not exists
os.makedirs(output_data_dir, exist_ok=True)

# copy the listed output files to the output location
files_to_copy = ['out_cell_dev.asc','out_cell_dph.asc', 'out_cell_suit.asc']
for file_name in files_to_copy:
    copyfile(os.path.join(result_data_dir, file_name), os.path.join(output_data_dir, file_name))


# make output dir if not exists
os.makedirs(buildings_data_dir, exist_ok=True)
urban_fabric_raster = os.path.join(output_data_dir, 'out_uf.asc')
subprocess.run(['generate_urban_fabric', '-i', '/data/inputs/data/out_cell_dph.asc', '-o', urban_fabric_raster])
subprocess.run(['raster_to_vector', '-i', urban_fabric_raster, '-o',
                os.path.join(buildings_data_dir, "urban_fabric.gpkg"), '-f' 'buildings'])
