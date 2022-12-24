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

### Debug with Hot Reload

```
jurigged -v src/server.py
jurigged -v src/client.py
```

## Assumption

1. Assume one message length is less than 1024 bytes.
