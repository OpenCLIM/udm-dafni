import os
from shutil import copyfile
os.system('python -m openudm /data/inputs/data')

# move files to output dir
result_data_dir = '/data/inputs/data'
output_data_dir = '/data/ouputs/data'

# make output dir if not exists
os.makedirs(output_data_dir, exist_ok=True)

# copy the listed output files to the output location
files_to_copy = ['out_cell_dev.asc','out_cell_dph.asc', 'out_cell_suit.asc']
for file_name in files_to_copy:
    copyfile(os.path.join(result_data_dir, file_name), os.path.join(output_data_dir, file_name))
