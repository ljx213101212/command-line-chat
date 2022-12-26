## Utils

```
lsof -nti:7976 | xargs kill -9
```

## Hot Reload

> https://github.com/breuleux/jurigged#develoop

### Debug with Hot Reload

```
jurigged -v src/server.py
jurigged -v src/client.py
```

## Test Coverage

> pip install coverage

```
coverage run -m unittest tests.test_server tests.test_command
coverage report
```
