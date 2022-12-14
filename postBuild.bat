#!/bin/bash
set -e

make devready
source activate test_dev_vrs_installation
python -m ipykernel install --user --name=3.9 --display-name="ED_kernel"