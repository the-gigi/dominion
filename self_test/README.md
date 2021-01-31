# SELF_TEST

The self_test package runs a game of dominion that pits AI computer players
against themselves.

It runs in a single process and doesn't need any network connection.

All the output is printed to the console.

Run it from dominion's root directory as follows:

```
PYTHONPATH=$(pwd); poetry run python self_test/main.py
```