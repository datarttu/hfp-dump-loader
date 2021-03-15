"""
Functions for handling YAML configuration for dataset listing and downloading.
"""

import yaml

def read_configuration_file(yaml_path):
    """Read and validate YAML configuration file from `path`."""
    with open(yaml_path, 'r') as yamlfile:
        conf = yaml.load(yamlfile, Loader=yaml.FullLoader)

    assert isinstance(conf, dict), 'YAML configuration must be key: value, not a list'
    for key in ['storage_url', 'field_mapping', 'target_dir', 'csvname_template']:
        assert key in conf.keys(), f'{key} is missing from YAML configuration'
    assert isinstance(conf['field_mapping'], dict), 'field_mapping must be key: value, not a list'

    return conf
