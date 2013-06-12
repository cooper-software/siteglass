import json
import os.path
from siteglass.config import Config
from siteglass.js import JSBuilder
from siteglass.css import CSSBuilder
from siteglass.amd import AMDBuilder
from siteglass.images import ImagesBuilder
from siteglass.copy import CopyBuilder

builders = ['copy', 'images', 'css', 'js', 'amd']
builders_by_name = {
    'copy': CopyBuilder,
    'images': ImagesBuilder,
    'css': CSSBuilder,
    'js': JSBuilder,
    'amd': AMDBuilder
}

def build(to_build, config_path):
    config = Config.from_json_file(config_path)
    
    if not to_build:
        to_build = builders
    
    versioned_files_map = {}
    
    for n in to_build:
        b = builders_by_name[n](config, versioned_files_map)
        b.run()
    
    if config.get('global.cache_bust.versioning.method') == 'lookup' and \
        config.get('global.cache_bust.versioning.file') is not None:
        versions_path = config.get('global.cache_bust.versioning.file')
        versions_path = versions_path if os.path.isabs(versions_path) else os.path.join(config['global.base_path'], versions_path)
        json.dump(versioned_files_map, open(versions_path, 'w'))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Merge & compress javascript, css and images.")
    parser.add_argument('--copy', action="store_true", help="Run copy rules")
    parser.add_argument('--js', action="store_true", help="Run javascript rules")
    parser.add_argument('--amd', action="store_true", help="Run AMD rules")
    parser.add_argument('--css', action="store_true", help="Run CSS rules")
    parser.add_argument('--images', action="store_true", help="Run rules for images")
    parser.add_argument('--config', metavar="CONFIG", default="./siteglass.json", help="Location of the config file")
    args = parser.parse_args()
    
    to_build = [x for x in builders if getattr(args, x)]
    build(to_build, args.config)