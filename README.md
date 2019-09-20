# My Time Tracker
A simple time tracker for the MHK crew.

## Getting started

### Requirements
 * python 3.6.7 or higher (package _python3_);

### Install
Install all the required tools in a virtualenv:
```
$ make install
```

### Serve

#### Development environment
To run the application locally in a development environment:
```
$ make serve
```

#### Production environment
Create a new file named `production.py` in `myworkshop/settings` and write your production settings in it.

Edit `myworkshop/settings/__init__.py`:
```
from .production import *
```

## Tech/framework used
 * [Django](https://www.djangoproject.com/)

## Versioning
We use [SemVer](http://semver.org/) for versioning. See the [CHANGELOG.md](CHANGELOG.md) file for details.

## Contributing
If you'd like to contribute, please raise an issue or fork the repository and use a feature branch. Pull requests are warmly welcome.

## Licensing
The code in this project is licensed under MIT license. See the [LICENSE](LICENSE) file for details.

## Contributors
 * **Julien Lebunetel** - [jlebunetel](https://github.com/jlebunetel)
