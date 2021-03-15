import argparse
from hfp_dump_loader import list_datasets as ld
from hfp_dump_loader import configuration as cf

def main(args):
    assert args.n > 0, '--n must be greater than 0'

    conf = cf.read_configuration_file(yaml_path=args.config)
    storage_url = conf['storage_url']
    prefix = conf['prefix']

    if args.csv:
        pass
    else:
        ld.browse_datasets_interactively(storage_url=storage_url, prefix=prefix, n=args.n)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List and download HFP datasets')
    parser.add_argument('--csv',
                        action='store_true',
                        help='Output results as plain csv, not interactively')
    parser.add_argument('--n',
                        type=int,
                        default=10,
                        metavar='<max n of lines>',
                        help='Max N of results to download at a time (defaults to 10)')
    parser.add_argument('--config',
                        default='config.yml',
                        metavar='<yaml config file>',
                        help='Path of the YAML configuration file (defaults to config.yml)')
    args = parser.parse_args()
    main(args)
