from hfp_dump_loader import list_datasets as ld
from hfp_dump_loader import configuration as cf

def main():

    conf = cf.read_configuration_file(yaml_path='config.yml')
    storage_url = conf['storage_url']

    ld.browse_datasets_interactively(storage_url=storage_url, n=10)

if __name__ == '__main__':
    main()
