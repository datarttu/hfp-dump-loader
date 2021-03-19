"""
Functions for handling YAML configuration for dataset listing and downloading.
"""

import yaml
from .utils import TYPE_CASTS

def read_conf_for_listing(yaml_path):
    """Read and validate YAML configuration file from `path` for dataset listing."""
    with open(yaml_path, 'r') as yamlfile:
        conf = yaml.load(yamlfile, Loader=yaml.FullLoader)

    assert isinstance(conf, dict), 'YAML configuration must be key: value, not a list'
    for key in ['storage_url', 'prefix']:
        assert key in conf.keys(), f'{key} is missing from YAML configuration'

    return conf

def read_conf_for_downloading(yaml_path):
    """Read and validate YAML configuration file from `path` for dataset downloading."""
    with open(yaml_path, 'r') as yamlfile:
        conf = yaml.load(yamlfile, Loader=yaml.FullLoader)

    assert isinstance(conf, dict), 'YAML configuration must be key: value, not a list'
    for key in ['storage_url', 'expected_n_fields', 'field_mapping', 'target_dir', 'csvname_template']:
        assert key in conf.keys(), f'{key} is missing from YAML configuration'

    assert isinstance(conf['expected_n_fields'], int) and conf['expected_n_fields'] > 0, 'expected_n_fields must be an integer > 0'
    assert isinstance(conf['field_mapping'], dict), 'field_mapping must be key: value, not a list'
    for k, v in conf['field_mapping'].items():
        assert isinstance(k, int) and k <= conf['expected_n_fields'], f'field_mapping {k}: keys must be integers <= expected_n_fields'
        assert isinstance(v, str) or isinstance(v, dict), f'field_mapping {k}: values must be string or key: value'
        if isinstance(v, dict):
            for key in ['name', 'type']:
                assert key in v.keys(), f'field_mapping {k}: {key} is missing'
            assert isinstance(v['name'], str), f'field_mapping {k}: name must be a string'
            assert v['type'] in TYPE_CASTS.keys(), f'field_mapping {k}: type must be one of {", ".join(TYPE_CASTS.keys())}'

    return conf
