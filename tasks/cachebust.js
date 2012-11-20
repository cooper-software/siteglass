/**
 * Copy files and rename them by appending a hash of their contents.
 * Copyright (c) 2012 Cooper
 * @author Elisha Cook <elisha@cooper.com>
 * License: MIT
 */
var md5 = require('MD5'),
    path = require('path')

module.exports = function (grunt)
{
    grunt.registerMultiTask(
        'cachebust', 
        'Generate cache-busting filenames and replace references in other files.', 
        function ()
        {
            var bustFiles = grunt.file.expand(this.data.bustFiles),
                replaceInFiles = grunt.file.expand(this.data.replaceInFiles),
                prefix = this.data.removePathPrefix,
                replacements = []
            
            grunt.log.writeln('')
            grunt.log.writeln('Creating cache-busted files...')
            
            bustFiles.forEach(function (original)
            {
                var contents = grunt.file.read(original, 'utf-8'),
                    hash = md5(contents),
                    ext = path.extname(original),
                    busted = path.join(path.dirname(original), path.basename(original, ext) + '-' + hash + ext)
                    find = prefix ? original.substr(prefix.length) : original
                    replace = prefix ? busted.substr(prefix.length) : busted
                
                grunt.file.copy(original, busted)
                
                replacements.push([
                    new RegExp(find.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&"), 'g'), 
                    replace
                ])
                
                grunt.log.writeln(original + ' -> ' + busted)
            })
            
            grunt.log.writeln('')
            grunt.log.writeln('Replacing old names with cache-busted names...')
            
            replaceInFiles.forEach(function (f)
            {
                var contents = grunt.file.read(f, 'utf-8') + ''
                
                if (contents == '')
                {
                    grunt.log.writeln(f)
                    return
                }
                
                replacements.forEach(function (r)
                {
                    contents = contents.replace(r[0], r[1])
                })
                
                grunt.file.write(f, contents)
                grunt.log.writeln(f)
            })
        }
    )
}