import os
from shutil import copyfile
import subprocess
import datetime
subprocess.run(['python', '-m',  'openudm', '/data/inputs'])

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

title = os.getenv('TITLE', 'OpenUDM output')
description = ' '
geojson = {}

metadata = f"""{{
  "@context": ["metadata-v1"],
  "@type": "dcat:Dataset",
  "dct:language": "en",
  "dct:title": "{title}",
  "dct:description": "{description}",
  "dcat:keyword": [
    "citycat"
  ],
  "dct:subject": "Environment",
  "dct:license": {{
    "@type": "LicenseDocument",
    "@id": "https://creativecommons.org/licences/by/4.0/",
    "rdfs:label": null
  }},
  "dct:creator": [{{"@type": "foaf:Organization"}}],
  "dcat:contactPoint": {{
    "@type": "vcard:Organization",
    "vcard:fn": "DAFNI",
    "vcard:hasEmail": "support@dafni.ac.uk"
  }},
  "dct:created": "{datetime.datetime.now().isoformat()}Z",
  "dct:PeriodOfTime": {{
    "type": "dct:PeriodOfTime",
    "time:hasBeginning": null,
    "time:hasEnd": null
  }},
  "dafni_version_note": "created",
  "dct:spatial": {{
    "@type": "dct:Location",
    "rdfs:label": null
  }},
  "geojson": {geojson}
}}
"""
with open(os.path.join('/data/outputs/metadata.json'), 'w') as f:
    f.write(metadata)
