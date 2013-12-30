Brunch + Flask
==============

Features
--------

- [Brunch][brunch] (JS/Coffeescript/CSS/Sass)
- [Flask][flask] ([SQLAlchemy][sqlalchemy]/[Flask-cache][flask-cache])
- [Karma][karma]
- [Nose][nose]

### Frontend

[Brunch][brunch] compiles all your frontend assets for you. Just start
adding things to the `app/` folder.

### Server

The server uses [Flask][flask] + [SQLAlchemy][sqlalchemy] + [Flask-cache][flask-cache].
Review `server/config.py` and `server/main.py` to see if there are any
changes you need to make, then start adding things in
`server/blueprints/`, `server/views/` or `server/models/`.

Getting Started
---------------

```bash
gem install foreman
npm install -g bower brunch
brunch new https://github.com/mikew/brunch-flask myapp
cd myapp
virtualenv venv
source venv/bin/activate
pip install -r server/requirements/development.txt
# or pip install -r server/requirements/test.txt
foreman start -f Procfile.dev
```

That's it. Visit `http://localhost:5000`, as you save files in `app/` that
page will update.

Testing
-------

### Frontend

I would suggest using one of Karma, Test'em or the browser, as those
will update as files in `app/` are modified.

**Using [Karma][karma]:**

```bash
node_modules/.bin/karma start
```

**Using [Test'em][testem]:**

```bash
node_modules/.bin/testem
```

**Using the browser:**

```bash
foreman start -f Procfile.dev
```

Open `http://localhost:5000/static/test/index.html` in your browser.

**Using [mocha-phantomjs][mocha-phantomjs]:**

```bash
node_modules/.bin/mocha-phantomjs public/test/index.html
```

### Server

```bash
server/tests/runner.py server/tests/ # Run all tests
server/tests/runner.py server/tests/test_foo.py # Run specific test
```

There is a Guardfile included that will run any tests whenever a file is
saved.

[brunch]: http://brunch.io
[flask]: http://flask.pocoo.org
[sqlalchemy]: http://www.sqlalchemy.org
[flask-cache]: http://pythonhosted.org/Flask-Cache/
[karma]: http://karma-runner.github.io/
[nose]: https://nose.readthedocs.org/en/latest/
[testem]: https://github.com/airportyh/testem
[mocha-phantomjs]: http://metaskills.net/mocha-phantomjs/
