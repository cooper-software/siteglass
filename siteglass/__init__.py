from siteglass.config import Config
from siteglass.js import JSBuilder
from siteglass.css import CSSBuilder
from siteglass.amd import AMDBuilder
from siteglass.images import ImagesBuilder

builders = ['images', 'css', 'js', 'amd']
builders_by_name = {
    'images': ImagesBuilder,
    'css': CSSBuilder,
    'js': JSBuilder,
    'amd': AMDBuilder
}

def build(to_build, config_path):
    config = Config.from_json_file(config_path)
    
    if not to_build:
        to_build = builders
    
    print
    
    for n in to_build:
        b = builders_by_name[n](config)
        b.build()
        print


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Merge & compress javascript, css and images.")
    parser.add_argument('--js', action="store_true", help="Run javascript rules")
    parser.add_argument('--amd', action="store_true", help="Run AMD rules")
    parser.add_argument('--css', action="store_true", help="Run CSS rules")
    parser.add_argument('--images', action="store_true", help="Run rules for images")
    parser.add_argument('--config', metavar="CONFIG", default="./siteglass.json", help="Location of the config file")
    args = parser.parse_args()
    
    to_build = [x for x in builders if getattr(args, x)]
    build(to_build, args.config)