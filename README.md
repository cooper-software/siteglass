# Siteglass

The goal of this project is to free web developers from thinking about site optimization while they are developing. _Siteglass_ provides a bare-bones web site template, mainly for illustrative purposes, and a grunt build that creates an aggressively optimized copy of your source. You organize your CSS with @import, your JavaScript with requirejs and use whatever kind of templates you like and _Siteglass_ gives you...

* Combined and minified JavaScript (r.js + almond)
* Combined and minified CSS
* Fonts & images inlined in CSS
* Cache busting file names for minified CSS and JS files

## How to use it

First, you need [grunt](http://gruntjs.com/). Then...

```sh
git clone https://github.com/cooper-software/_Siteglass_.git myproject
cd myproject
npm install
# write some code
grunt dist
```

This will create a dist folder which you are encouraged to explore.

## Why?

There are some great tools around for site optimization but, at the time this was written, no package that ties everything together and that fits with the workflow and structure of many different types of projects. We wanted the freedom to organize our code and assets in whatever way made sense for development and then do something simple, like issue a single command, and get a well-optimized front end. We wanted this ease of use without relying on a particular framework. Here's what we chose to do (or not) and why:

* **Use requirejs** -- manually managing module dependencies is insane in a large project. Requirejs works well and has widespread support.
* **Use plain old CSS** -- preprocessors have some nice syntax but we find them to hinder development more than help it for a variety of reasons. Mostly it comes down to the fact that plain old CSS is much easier to debug and explore using existing tools. It's easy enough to structure CSS using `@import`. The only downside to this approach is multiple HTTP requests. _Siteglass_ takes care of that by pulling all the CSS into one file and minifying it.
* **Inline assets** -- sprites are a great invention, but they can be time consuming to create. Inlining images not only obsoletes sprites but it also uses fewer HTTP requests (1 for CSS instead of 1 for CSS + 1 per sprite). And we might as well do it with fonts, too. The build is configurable so it's possible to create optimized page-specific CSS files so clients don't need to download inlined page-specific assets for pages they aren't viewing. The CSS files developers work on aren't cluttered with data URIs and image files can be organized in any way without affecting performance.
* **Use cache-busting file names** -- we all know by now (or should) that setting a far future expires header on static files reduces traffic and speeds up subsequent page loads. But this presents a problem when our files change. Usually, this is handled by appending a version number to the file name or in a query string where the file is referenced. _Siteglass_ takes a different approach. It generates file names suffixed with a hash of the file's contents. This way, if your CSS or JS changes, clients will never read a file from a stale cache and there is no need to manually manage per-file version numbers.
* **Replace references to generated files in everything** -- This sort of ties it all together. It's all well and good to have minified files with fancy names but we need to actually point at them with our templates. _Siteglass_ uses simple search and replace to make specified files reference the generated files. There is no DOM involved so the files don't need to be HTML. They can be ejs, PHP, mako, C or FORTRAN if you're in to that sort of thing.

In a nutshell, we want flexibility, ease of development and the best possible performance without compromise.

## Configuration

_Siteglass_ relies on some existing grunt tasks like [grunt-requirejs](http://asciidisco.github.com/grunt-requirejs/) and [grunt-css](https://github.com/jzaefferer/grunt-css). See the task-specific pages for details on how to configure them if you need or want to modify the defaults. There are three other tasks included in this project. You can find them in `<siteglass>/tasks/`. The default grunt.js will work for a lot of cases but if you need or want to customize, here is some information on configuring the these tasks. As a side not, all of these are multitasks.

### regex

This task is very simple. It performs regular expression search and replace on text files. _Siteglass_ uses it to replace requirejs script tags with normal ones pointing at the minified, almondified files. If you are referencing JS in files that have an extension other than ".html" you'll want to modify this task to include those files.

```js
regex:
{
    dist:
    // Provide this task with an array of search and replace configurations.
    [
        {
            // Specify the files which should be scanned
            files: ['dist/**/*.html'],
            
            // Define the search pattern...
            find: '<script data-main="([^"]+)" src="[^"]+"></script>',
            
            // ...and the replacement
            replace: '<script src="$1"></script>'
        }
    ]
}
```

### inlineassets

Get rid of pesky HTTP requests with data URIs. This task will inline WOFF fonts, svg, png and jpeg images. This saves lots of HTTP requests and you don't have to create sprites anymore.

```js
inlineassets:
{
    dist:
    // Provide a list of configurations.
    [
        {
            // This is the base directory against which paths found in the 
            // files will be resolved.
            baseDir: 'dist/css',
            
            // These are the files in which to look for inlineable assets.
            files: 'dist/css/main.css',
            
            // Set each type of file you want inlined to `true`.
            // The options are 'woff', 'svg', 'png' and 'jpg'.
            woff: true,
            svg: true
        }
    ]
}
```

### cachebust

Copy files, giving the new file names a suffix that is a hash of the file contents. This way web servers can set a far-future expires header but when your CSS or JS changes, clients will not read from a stale cache.

```js
cachebust:
{
    dist: 
    {
        // The list of files that should get new names.
        bustFiles: [
            'dist/css/main.css',
            'dist/js/main.js'
        ],
        
        // The list of files that may contain references to the busted files.
        replaceInFiles: ['dist/**/*.html'],
        
        // The prefix of the busted file paths to remove when replacing the paths.
        // In this example, cachebust will search for 'css/main.css' and replace it with
        // something like 'css/main-9071bd176416fba3721d45e5e6df9095.css'. Without this
        // argument, cachebust would be looking for references to 'dist/css/main.css'.
        removePathPrefix: 'dist/',
    }
}
```

## Status

This is a young project. We think it's pretty good but we want it to be great. In the future, we plan to add more optimizations like PNG and JPEG shrinking prior to inlining and whitespace removal from template files. If you have ideas, bugs, comments, please share.