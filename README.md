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

```
python -m unittest tests.test_main
python -m unittest tests.test_server

```

## Assumption

1. Initial data is empty.
2. One message length is less than 1024 bytes.
3. Login username shouldn't be empty or only contains empty spaces.
