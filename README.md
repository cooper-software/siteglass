# Siteglass

Looking for a new solution to managing web assets? No? How about one with features like this:

* Optimize images
* Merge & minify CSS
* CSS merging follows imports
* Images and fonts are inlined in your CSS
* Merge and minify lists of JS files or use AMD or a combination
* Generate cache busting names using MD5 or a managed version number
* Simple command line tool with a single config file. No boilerplate. Set up your files however you like.

You can use any or all of these features. Siteglass makes no assumptions about how your code is set up.

## Example workflow

As mentioned, there are many ways to use siteglass. This is one I like. Here's the directory structure:

    project/
        images/
            foo.png
            bar.jpg
        js/
            main.js
            require.js
            dostuff.js
        css/
            main.css
            type.css
            grid.css
        version
        index.html
        siteglass.json

As you might guess, this fake project is using require.js to resolve AMD calls. Let's look at some of these files. First, the `index.html` file, which is really a jinja2 template.

```jinja
<!DOCTYPE html>
<html>
    <head>
        {% if is_dev %}
            <link rel="stylesheet" type="text/css" href="css/main.css" />
        {% else %}
            <link rel="stylesheet" type="text/css" href="css/main.min.{{ version }}.css" />
        {% endif %}
    </head>
    <body>
        <!-- Content goes here -->
        {% if is_dev %}
            <script src="js/require.js" data-main="js/main.js"></script>
        {% else %}
            <script src="js/main.min.{{ version }}.js"></script>
        {% endif %}
    </body>
</html>
```

We have a template that will load a different css and js file depending on some flag. Also, the production files get a version variable in their name to bust stale cache. And there's just one CSS file and one JS file. Great!

Here's what our `main.css` file looks like:

```css
@import url("type.css");
@import url("grid.css");

body {
    background-image: url(../images/bar.jpg);
}
```

Those imports are bad practice, right? Not really. The reason is because the imports will only be there during development. After we run siteglass, all the imports will be inlined in `main.css` and then it will be minfied. Also, that background image will be optimized and inlined using a data URL. This handy feature means you never have to create a sprite again.

Ok, how about our `main.js` file?

```javascript
require(['dostuff'], function (dostuff)
{
    dostuff()
})
```

Standard AMD. During development, `require.js` will be loaded and it will resolve dependencies and load all the source files. When you run siteglass, it will also resolve the dependencies and then it will merge all the files into one, add [almond.js](https://github.com/jrburke/almond) and minify it.

To recap, during dev, we write normal CSS and javascript without giving any thought to optimization. After we run siteglass we have one file with all our minfied CSS--referenced images and fonts inlined--and one javascript file with all dependencies resolved, minified. Sweet!

What about that `version` file? This file is managed by siteglass. Each time siteglass is run, it will increment the version number and use that when naming the files it creates. The file can be read on the server side and passed to templates so they can use it to generate the correct file names. This behavior can be controlled in the configuration file.

Speaking of which, let's see it!

```json
{
    "global": {
        "encoding": "utf-8",
        "cache_bust": {
            "enabled": true,
            "versioning": {
                "method": "file",
                "filename": "version"
            }
        }
    },
    
    "amd": [{
        "source": "js/main.js",
        "target": "js/main.min.js"
    }],
    
    "css": [{
        "source": "css/main.css",
        "target": "css/main.min.css"
    }],
    
    "images": [{
        "source": [
            "images/*.png",
            "images/*.jpg"
        ]
    }]
}
```

That's it! Have a look at the configuration reference to see what else siteglass can do.

## Configuration

The configuration file is in JSON format. It can be called anything but the `siteglass` `--config` argument defaults to "siteglass.json".

All settings are optional. Only the build tasks that are configured will run. If you don't want image compression, don't specify an `"images"` section.

Any setting that takes a path actually takes a variety of input. A path argument can be a simple path like `"/foo/bar"`, a glob like `"/baz/*.qux"` or a list of paths and globs like `["/foo/bar", "/baz/*.qux"]`.

The list below describes the properties of the configuration object. Hopefully, the nesting is clear.

* `global` - Settings that affect all build tasks
    * `encoding` - The encoding used when reading and writing text files. Defaults to `"utf-8"`
    * `cache_bust` - Settings for generating cache-busting file names.
        * `enabled` - Set to `true` to enable cache busting names. The default is `false`.
        * `versioning` - Settings for how to version names.
            * `method` - This can be either `"hash"` or `"file"`. The hash setting will generate file names based on a hash of the file's contents. Setting this option to `"file"` will cause siteglass to use a version number stored in a text file. The number will be used in the names of all generated files of a build. This number will be managed by siteglass. There is no need to manually increment the version number. Defaults to `"file"`.
            * `filename` - This is the name of the file, if the file method is being used. Defaults to `"version"`
* `amd` - Settings for the AMD build. This is a list of objects with the following properties:
    * `source` - Path to a main module--a single JS file.
    * `target` - Path to output the merged and minified file.
* `css` - Settings for the CSS build. A list of objects with the following properties:
    * `source` - Path to CSS files.
    * `target` - Path to output the merged and minified file.
    * `resolve_imports` - If `true`, resolve `@import` statements and inline the contents. Defaults to `true`.
    * `inline_assets` - If `true`, inline WOFF fonts, PNGs, JPGs and SVGs using data URLs. Defaults to `true`.
    * `paths_relative_to` - Can be either `"source"` or `"target"`. If set to `"target"`, paths to fonts and images within the CSS source files will be relative to the target's directory, otherwise they will be relative to the source's directory. Defaults to `"source"`
* `images` - Settings for the image optimization build. A list of objects with the following properties:
    * `source` - Path to some images.
    * `target` - A target output directory. If not set, source files will be overwritten.