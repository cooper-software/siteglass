/**
 * Siteglass optimization build
 * Copyright (c) 2012 Cooper
 * @author Elisha Cook <elisha@cooper.com>
 * License: MIT
 */
module.exports = function(grunt)
{
    grunt.initConfig(
    {
        // Start with a pristine dist folder
        clean: {
            dist: 'dist'
        },
        
        // Copies the src directory and creates minified JS files,
        // with almond.js inlined.
        requirejs:
        {
            dist:
            {
                appDir: "src",
                baseUrl: "js",
                dir: "dist",
                modules: [
                    {
                        name: "main"
                    }
                ],
                paths: [],
                preserveLicenseComments: false,
                
                almond: true,
                wrap: true
            }
        },
        
        // Minfies the CSS that requirejs concatenated.
        cssmin:
        {
            dist:
            {
                src: 'dist/css/main.css',
                dest: 'dist/css/main.css'
            }
        },
        
        // Replaces requirejs-structured script tags with ones pointing
        // directly at the almond-based, minified files.
        regex:
        {
            dist:
            [
                {
                    files: ['dist/**/*.php', 'dist/**/*.html'],
                    find: '<script data-main="([^"]+)" src="[^"]+"></script>',
                    replace: '<script src="$1"></script>'
                }
            ]
        },
        
        // Inlines fonts and images in the CSS
        inlineassets:
        {
            dist:
            [
                {
                    baseDir: 'dist/css',
                    files: 'dist/css/main.css',
                    woff: true,
                    svg: true
                }
            ]
        },
        
        // Creates copies of the minified CSS and JS files appending a hash
        // of the file contents to the end of the file name. Also replaces
        // references to the renamed files in html/template files.
        cachebust:
        {
            dist: 
            {
                bustFiles: [
                    'dist/css/main.css',
                    'dist/js/main.js'
                ],
                replaceInFiles: ['dist/**/*.php', 'dist/**/*.html'],
                removePathPrefix: 'dist/',
            }
        }
    })
    
    grunt.loadNpmTasks('grunt-contrib-clean')
    grunt.loadNpmTasks('grunt-requirejs')
    grunt.loadNpmTasks('grunt-css')
    grunt.loadTasks('tasks')
    
    grunt.registerTask('dist', 'clean:dist requirejs:dist cssmin:dist regex:dist inlineassets:dist cachebust:dist')
};
