# Siteglass

Siteglass is a tool for bundling and compressing your Javascript, CSS and images for the web. It aims to provide advanced features like AMD support and cache-busting in a simple, standalone package that works with any framework.

## Installation

Siteglass is written in python with one little C extension so you'll need a C compiler and the Python headers installed. Then it's a snap:

```bash
$ git clone git@github.com:cooper-software/siteglass.git
$ cd siteglass
$ python setup.py install
```

This will install the siteglass python module as well as an executable `siteglass` script that's used to invoke siteglass.

## Example

The source distribution contains a simple example that shows off CSS, Javascript and image compression within a project using [require.js](http://requirejs.org/). To run the example…

```bash
$ cd /path/to/siteglass/example
$ siteglass
```

This will read the configuration file `siteglass.json`, create a new `dist` directory, copy all the source files, merge and minify the Javascript and CSS, optimize the images and rewrite the paths inside `index.html` to their cache-busting counterparts.

Have a look at the configuration file.

## Command line usage

The `siteglass` command is very simple. Most of the control over how siteglass runs is defined in the configuration file. By default, all the build phases that are configured will run. However, the script options allow you to run only specific build phases, if that's what you need. Run `siteglass -h` for this:

```
usage: siteglass [-h] [--copy] [--js] [--amd] [--css] [--images] [--config CONFIG]

Merge & compress javascript, css and images.

optional arguments:
  -h, --help       show this help message and exit
  --copy           Run copy rules
  --js             Run javascript rules
  --amd            Run AMD rules
  --css            Run CSS rules
  --images         Run rules for images
  --config CONFIG  Location of the config file
 ```

## Configuration file

The configuration file is a JSON formatted file that sets global options for siteglass and defines various build phases. By default, when `siteglass` is run it will look for a `siteglass.json` file in the current director. You can name your config file something else and put it anywhere you like by calling `siteglass` with the `--config=` option.

A configuration file looks like this:

```json
{
    "global": {
        "cache_bust": {
            "enabled": true,
            "versioning": {
                "method": "hash",
                "rewrite": "dist/*.html"
            }
        }
    },
    
    "copy": {
        "src": "dist"
    },
    
    "amd": [{
        "source": "dist/js/main.js",
        "target": "dist/js/main.min.js"
    }],
    
    "css": [{
        "source": "dist/css/main.css",
        "target": "dist/css/main.min.css"
    }],
    
    "images": [
        {
            "source": [
                "dist/images/*.png",
                "dist/images/*.jpg"
            ]
        }
    ]
}
```

Each entry in the root object, except for `"global"` is a build phase configuration. The order they are defined in doesn't matter. Only build phases that are defined in the file will run, i.e., there are no default options for any build phases.

### A note about paths

Paths can get tricky pretty quick. Unless otherwise specified in settings-specific documentation, all paths are relative to the directory where the configuration file is found. So if your config file is `/foo/bar/siteglass.json` and it contains a path `"baz/qux.js"`, the full path is `"/foo/bar/baz/qux.js"`.

Any of the settings that take a path value can actually take a number of different forms. The value can be a single path string (`"foo/bar"`), a glob (`"foo/*.bar"`) or a list of paths and globs (`["foo/bar", "foo/*.bar"]`).

### Reference

* `global` - this section is for settings that affect more than one build phase. This is the only section that does not trigger a build phase.
    * `encoding` - the default text encoding. All text files will be read using this encoding. It defaults to utf-8.
    * `base_path` - the path against which relative URLs within the configuration will be resolved. This defaults to the directory where the configuration file is found.
    * `cache_bust` - if present, merge and min tasks will generate files that have cache busting names. There are two schemes: hash and versioning. The hash method will append an MD5 of the file's contents to the file name. This is the most effective method since only files that actually have changes will bust the cache. There is also a method that uses a version number file. This will increment the version number each build and append it to the names of all merge & min'd files. Siteglass can also find and replace paths with their cache-busted versions within text files.
	* `enabled` - set to `true` to enable cache busting.
	* `versioning` - settings for the versioning scheme
	    * `method` - must be either `"hash"` or `"file"`.
	    * `filename` - *file method only*. Path to the version file, if file versioning is being used.
	    * `rewrite` - *hash method only*. Paths of files that contain references to cache-busted files and should have the references rewritten.
	    * `relative_to` - *hash method only*. A base path against which paths in rewrite files should be resolved. Defaults to the directory in which the rewrite file is located.
* `copy` - copies directories. This should be an object where the keys are the source paths and the values are the destination paths.
* `js` - Merge and minify javascript files. There is no dependency resolution or smart ordering here. See `amd` for that. Pass a list of objects with the following properties:
    * `source` - path to the javascript sources, e.g, `"js/*.js"`
    * `target` - path to the minified, compressed output, e.g, `"min.js"`
* `amd` - Resolves AMD dependencies, merges and minifies everything and adds almond.js. To define AMD entry points use a list of objects with these properties:
    * `source` - path to a javascript file that loads other javascript files, e.g, `"main.js"`.
    * `target` - path to the minified, compressed output, e.g. `"js/main.min.js"`
* `css` - settings for the CSS merge and min build phase. Use a list of objects with the following properties:
    * `source` - path to CSS files, e.g. `"css/main.css"`.
    * `target` - path to the merged and minified output, e.g., "`css/main.min.css`".
    * `resolve_imports` - if `true`, resolve `@import` statements and inline the contents. Defaults to `true`.
    * `inline_assets` - if `true`, inline WOFF fonts, PNGs, JPGs and SVGs using data URLs. Defaults to `true`.
    * `relative_to` - can be either `"source"` or `"target"`. If set to `"target"`, paths to fonts and images within the CSS source files will be relative to the target's directory, otherwise they will be relative to the source's directory. Defaults to `"source"`
* `images` - settings for the image optimization build. A list of objects with the following properties:
    * `source` - path to some images.
    * `target` - a target output directory. If not set, source files will be overwritten.