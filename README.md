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

Testing
-------

### Frontend

**Using [Karma][karma]:**

```bash
node_modules/.bin/karma start
```

**Using [Test'em][testem]:**

```bash
node_modules/.bin/testem
```

**Using [mocha-phantomjs][mocha-phantomjs]:**

```bash
node_modules/.bin/mocha-phantomjs public/test/index.html
```

**Using the browser:**

```bash
./manage.py runserver
```

Open `http://localhost:5000/test/` in your browser.

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
