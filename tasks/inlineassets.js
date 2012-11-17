/**
 * Inlines font and image files in CSS
 * Copyright (c) 2012 Cooper
 * @author Elisha Cook <elisha@cooper.com>
 * License: MIT
 */
module.exports = function (grunt)
{
    var types = 
    {
        woff:
        {
            pattern: new RegExp('url\\([\'"]?([^\'"\\)]+)[\'"]?\\)\\s+format\\([\'"]?woff[\'"]?\\)', 'g'),
            mime: 'application/x-font-woff',
        },
        
        svg:
        {
            pattern: new RegExp('url\\([\'"]?([^\'"\)]+?\.svg)[\'"]?\\)', 'g'),
            mime: 'image/svg+xml'
        },
        
        png:
        {
            pattern: new RegExp('url\\([\'"]?([^\'"\)]+?\.png)[\'"]?\\)', 'g'),
            mime: 'image/png'
        },
        
        jpg:
        {
            pattern: new RegExp('url\\([\'"]?([^\'"\)]+?\.jpg)[\'"]?\\)', 'g'),
            mime: 'image/jpeg'
        }
    }
    
    grunt.registerMultiTask(
        'inlineassets',
        'Inlines fonts & images into CSS using the data URI scheme.',
        function ()
        {
            this.data.forEach(function (spec)
            {
                var files = grunt.file.expand(spec.files)
                
                files.forEach(function (f)
                {
                    var contents = grunt.file.read(f).toString(),
                        replacements = []
                    
                    for (var n in types)
                    {
                        if (spec[n])
                        {
                            var match
                            
                            while (match = types[n].pattern.exec(contents))
                            {
                                var asset_contents = grunt.file.read(spec.baseDir + '/' + match[1],true),
                                    encoded_asset_contents = asset_contents.toString('base64'),
                                    replacement = 'url(data:'+types[n].mime+';base64,'+encoded_asset_contents+')'
                                    
                                replacements.push([
                                    new RegExp(match[0].replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&"), 'g'), 
                                    replacement
                                ])
                            }
                        }
                    }
                    
                    replacements.forEach(function (r)
                    {
                        contents = contents.replace(r[0], r[1])
                    })
                    
                    grunt.file.write(f, contents)
                })
            })
        }
    )
}