exports.config =
  # See https://github.com/brunch/brunch/blob/master/docs/config.md for docs.
  files:
    javascripts:
      joinTo:
        'javascripts/app.js': /^app/
        'javascripts/vendor.js': /^(vendor|bower_components)/
        'test/javascripts/test.js': /^test\/(?!vendor)/
        'test/javascripts/test-vendor.js': /^test\/(?=vendor)/

    stylesheets:
      joinTo:
        'stylesheets/app.css': /^(app|vendor|bower_components)/
        'test/stylesheets/test.css': /^test/

    templates:
      joinTo: 'app.js'
