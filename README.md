## Quick Start

### Run

1. Run follwing command in one terminal

```
python -m src.server
```

2. Run following command in one or more terminals as clients terminals

```
python -m src.client
```

3. Input command in clients terminals.

### Run Unit Test

> start server for tests.test_server (in TAB 1)

```
python -m src.server
```

> run unit tests (in TAB 2)

```

python -m unittest tests.test_server tests.test_command
```

## Assumption

1. Initial data is empty.
2. One message length is less than 1024 bytes.
3. Login username shouldn't be empty or only contains empty spaces.
4. Added Debug command to ease unit test.
5. Send/forward a message to current login user is not allowed.
6. Broadcast can send message to a logged out user.

## Unit Test Coverage

```
Name                    Stmts   Miss  Cover
-------------------------------------------
src/__init__.py             0      0   100%
src/command.py            146     19    87%
src/constants.py           31      0   100%
src/data.py                 2      0   100%
src/models.py              17      4    76%
src/utils.py               46     14    70%
tests/__init__.py           0      0   100%
tests/test_command.py     193      5    97%
tests/test_server.py      163      1    99%
-------------------------------------------
TOTAL                     598     43    93%
```
