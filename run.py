import os
from shutil import copyfile
import subprocess
import datetime
from zipfile import ZipFile
import pandas as pd

from os import getenv, walk, mkdir, remove, listdir
from os.path import join, isdir, isfile
import zipfile

import csv

def zip_file(path, file):
    """
    Zips a file and deletes the un-archived version
    """
    zipObj = ZipFile(f'{join(path,file)}.zip', 'w')
    zipObj.write(join(path,file))

    zipObj.close()

    os.remove(join(path, file))
    return

def find_metadata_files():
    """
    Search all directories for any metadata files (metadat.csv)
    """

    suitable_extension_types = ['csv','']

    files_ = []

    for root, dirs, files in walk('/data/inputs'):
        print(root, files)
        for file in files:
            if file == 'metadata.csv':
                files_.append(join(root, file))

    print(files_)
    return files_
    
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

# setting file paths
result_data_dir = '/data/inputs'
output_dir = '/data/outputs'
output_data_dir = '/data/outputs/data'
buildings_data_dir = '/data/outputs/buildings'

# get environment values
# fetch UFG value
run_ufg = getenv('RUN_UFG')
if run_ufg is None:
    run_ufg = False
elif run_ufg.lower() == 'true' or run_ufg == True:
    run_ufg = True
else:
    run_ufg = False

# make output dir if not exists
os.makedirs(output_data_dir, exist_ok=True)

# check for any meta data files
metadata_files = find_metadata_files() #search for any existing metadata files (expect to find at least one from the population data)
print('Metadata files', metadata_files)

# write a metadata file recording key parameters
year = None
ssp = None
print('Saving metadata file')
if len(metadata_files) == 1: # if one metadata file found
    df = pd.read_csv(metadata_files[0]) # read in the file into a dataframe
    #print(df.head())
    df.to_csv(join(output_data_dir, 'metadata.csv'), index=False) # write dataframe to csv
    #print(df.columns)
    # set some parameters which can be used later
    #year = df.loc[df['PARAMETER'] == 'YEAR', 'VALUE']
    #ssp = df.loc[df['PARAMETER'] == 'SSP', 'VALUE']
    
elif len(metadata_files) == 0:
    print('No metadata files found')
else:
    print('Multiple metadata files found. This functionality has not been added yet')


# run UDM
subprocess.run(['python', '-m',  'openudm', '/data/inputs'])
print('*** Ran UDM ***')

print('*** Output files ***')
print(find_files())

# move files to output dir

# copy the listed output files to the output location
files_to_copy_1 = ['attractors.csv', 'constraints.csv', 'parameters.csv', 'population.csv']
for file_name in files_to_copy_1:
    copyfile(os.path.join(result_data_dir, file_name), os.path.join(output_data_dir, file_name))

files_to_copy_2 = ['out_cell_dev.asc', 'out_cell_suit.asc', 'out_cell_pph.asc', 'out_cell_dph.asc']
for file_name in files_to_copy_2:
    copyfile(os.path.join(result_data_dir, file_name), os.path.join(output_data_dir, file_name))

files_to_copy_3 = ['out_cell_density_band.asc', 'out_cell_build_type.asc', 'out_cell_tile_type.asc']
for file_name in files_to_copy_3:
    copyfile(os.path.join(result_data_dir, file_name), os.path.join(output_data_dir, file_name))

files_to_copy_4 = ['out_cell_roads_cov.asc', 'out_cell_green_cov.asc', 'out_cell_build_cov.asc', 'out_cell_overflow.csv']
for file_name in files_to_copy_4:
    copyfile(os.path.join(result_data_dir, file_name), os.path.join(output_data_dir, file_name))

print('*** Moved UDM output files ***')

# zip output dir

#name = '/data/outputs/data'
#zip_name = name + '.zip'

#with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
#    for folder_name, subfolders, filenames in os.walk(name):
#        for filename in filenames:
#            file_path = os.path.join(folder_name, filename)
#            zip_ref.write(file_path, arcname=os.path.relpath(file_path, name))

#zip_ref.close()

#print('*** Zipped UDM output files ***')

# if we want to rename any file output by UDM do this here.....
#
#

# run ufg tool if set by user
if run_ufg:
    
    # run urban fabric generator tool
    build_type_ras = os.path.join(result_data_dir, 'out_cell_build_type.asc')
    tile_type_ras = os.path.join(result_data_dir, 'out_cell_tile_type.asc')
    urban_fabric_raster = os.path.join(output_data_dir, 'out_uf.asc')

    subprocess.run(['ufg_fabric', '-b', build_type_ras, '-t', tile_type_ras, '-f', urban_fabric_raster])    

    print('*** Ran UFG ***')

    # make output dir if not exists
    os.makedirs(buildings_data_dir, exist_ok=True)

    # run raster to vector tool
    subprocess.run(['raster_to_vector', '-i', '/data/outputs/data/out_uf.asc', '-o',
                    os.path.join(buildings_data_dir, "urban_fabric.gpkg"), '-f' 'buildings,roads,greenspace'])

    # in an old version the data is stored in the wrong place. zip into a suitable output location
    zipObj = ZipFile('/data/outputs/data/urban_fabric.zip', 'w')

    print('searching for output')
    for root, dirs, files in walk('/'):
        #print(root, files)
        for file in files:
            file_extension = file.split('.')[-1]
            if file_extension == 'gpkg':
                if 'buildings.gpkg' or 'roads.gpkg' or 'greenspace.gpkg' or 'urban_fabric.gpkg' in file:
                    print(join(root, file))
                    zipObj.write(join(root, file))
                    os.remove(join(root, file))
    zipObj.close()

    # to save disk space, zip out_uf.asc and delete the raw file
    zip_file(output_data_dir, 'out_uf.asc')

    print('*** Ran R2V ***')

# zip output dir

metadata_tbl = '/data/outputs/data/metadata.csv'
ssp = ''
year = ''  
with open(metadata_tbl) as csvfile:
    reader = csv.DictReader(csvfile)        
    for row in reader:        
        if row['PARAMETER'] == 'SSP':  
            ssp = row['VALUE']          
        elif row['PARAMETER'] == 'YEAR':
            year = row['VALUE']
print(ssp)  
print(year)   

z_name1 = 'ssp' + ssp + '-' + year 
print(z_name1)

print( "Metadata file imported.")

name = '/data/outputs/data'
z_name2 = '/data/outputs/' + z_name1
zip_name = z_name2 + '.zip'

with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
    for folder_name, subfolders, filenames in os.walk(name):
        for filename in filenames:
            file_path = os.path.join(folder_name, filename)
            zip_ref.write(file_path, arcname=os.path.relpath(file_path, name))

zip_ref.close()

print('*** Zipped UDM output files ***')
