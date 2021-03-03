# OpenUDM on DAFNI
[![build](https://github.com/OpenCLIM/udm-dafni/workflows/build/badge.svg)](https://github.com/OpenCLIM/udm-dafni/actions)


## Description
This repository establishes a docker container for running the UDM Model (https://github.com/geospatialncl/openudm).

## Usage
A second model, udm-setup (https://github.com/geospatialncl/udm-setup), has been designed and enabled to handle the inputs for UDM and make them available in the correct format. Please see this model to understand the required inputs and the structure and format of these.

### Running this container
`docker run --name udmdafni -v <your local path>/data:/data/inputs/data -t udmdafni`

Outputs from the UDM model are currently written to the same directory.

