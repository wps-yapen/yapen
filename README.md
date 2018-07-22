# yapen

## Requirements

- Python (3.6)
- Django (2.x)

### Secrets

#### `.sercets/base.json`

```json
{
  "SECRET_KEY": "<Django secret key>"
}
```

## Installation
```
pyenv install
```

## Running

```
# Move project`s directory
- pipenv install
- pipenv shell
- cd app
- export DjANGO_SETTINGS_MODULE=config.settings.local
- `./manage.py runserver`
```