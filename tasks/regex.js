/**
 * Performs regex search and replace in text files.
 * Copyright (c) 2012 Cooper
 * @author Elisha Cook <elisha@cooper.com>
 * License: MIT
 */
module.exports = function (grunt)
{
    grunt.registerMultiTask('regex', 'Find and replace in files', function ()
    {
        this.data.forEach(function (info)
        {
            var files = grunt.file.expand(info.files),
                find = new RegExp(info.find, 'g')
                
            files.forEach(function (f)
            {
                var contents = grunt.file.read(f, 'utf-8') + ''
                contents = contents.replace(find, info.replace)
                grunt.file.write(f, contents)
            })
        })
    })
}