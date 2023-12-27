#!/usr/bin/env python3

# ----

"""
"""
    
# ---

import os
from types import SimpleNamespace

from tools import parser_interface
from utils.decorator_interface import cli_wrapper, script_wrapper

# ----

DESCRIPTION = "Observation processing interfaces."
SCHEMA_FILE = os.path.join(
    parser_interface.enviro_get("OBS_ROOT"),
    "scripts", "schema", "compute_obs.schema.yaml",
)
SCRIPT_NAME = os.path.basename(__file__)

@cli_wrapper(description=DESCRIPTION, schema_file=SCHEMA_FILE, script_name=SCRIPT_NAME)
@script_wrapper(script_name=SCRIPT_NAME)
def main(options_obj: SimpleNamespace()) -> None:
    """

    """
    

    
# ----

if __name__ == "__main__":
    main()