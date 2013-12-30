exports.config =
  # See http://brunch.io/#documentation for docs.
  files:
    javascripts:
      #joinTo: 'app.js'
      joinTo:
        'javascripts/app.js': /^app/
        'javascripts/vendor.js': /^(vendor|bower_components)/
        'test/javascripts/test.js': /^test\/(?!vendor)/
        'test/javascripts/test-vendor.js': /^test\/(?=vendor)/
    stylesheets:
      #joinTo: 'app.css'
      joinTo:
        'stylesheets/app.css': /^(app|vendor|bower_components)/
        'test/stylesheets/test.css': /^test/
    templates:
      joinTo: 'app.js'
