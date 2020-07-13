# Dominion object model

[
![PyPI](https://img.shields.io/pypi/v/dominion-object-model.svg)
![PyPI](https://img.shields.io/pypi/pyversions/dominion-object-model.svg)
![PyPI](https://img.shields.io/github/license/the-gigi/dominion.svg)
](https://pypi.org/project/dominion-object-model/)


This package contains two abstract base classes for implementing players 
and client libraries for the [dominion](https://github.com/the-gigi/dominion) project.

You can implement a GUI client for humans to play the game or an AI computer
player.

# Usage

A dominion player must implement the Player interface. The dominion game engine
will keep a reference to the player object and call its methods at the right time.

```
class Player(metaclass=ABCMeta):
    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def respond(self, action, *args):
        pass

    @abstractmethod
    def on_game_event(self, event):
        pass

    @abstractmethod
    def on_state_change(self, state):
        pass
```

A client library will implement the GameClient interface and a reference
to it will be passed to concrete player implementations. When the concrete
player who implements the Player interface receives the play() command 
from the game engine it will invoke various GameClient methods until
it finally calls done() and their turn ends.

```
class GameClient(metaclass=ABCMeta):
    @abstractmethod
    def play_action_card(self, card_type: str):
        pass

    @abstractmethod
    def buy(self, card_type: str):
        pass

    @abstractmethod
    def done(self):
        pass
```

# Examples

The dominion project itself contains several [computer players](https://github.com/the-gigi/dominion/tree/master/computer_players).

The [dominion-pygame](https://github.com/Bloblblobl/dominion-pygame) project is an implementation of a GUI client that lets humans play against each other and or bots.


# Build and publish

This section is for the Dominion developers. 
If you just want to implement a player or a client library you can stop reading.


Check out this fantastic [article](https://code.tutsplus.com/tutorials/how-to-write-package-and-distribute-a-library-in-python--cms-28693) ;-)

It provides all the information necessary for writing and uploading packages to PyPI. 


Here is the command to build the package:

```
(🐙)/dominion/dominion/object_model/
$ poetry run python setup.py sdist
``` 

Unfortunately, I couldn't get `poetry build` to work so I resorted to old-fashioned setup.py

The result is tar-gzipped file in the dist subdirectory:

```
(🐙)/dominion/dominion/object_model/
$ ls dist
dominion-object-model-1.0.0.tar.gz
```

Since the object_model package is abstract and designed to be imported by other 
Python libraries there is no need for a binary distribution.


Save the following to ~/.pypirc

```
[distutils]
index-servers=
    pypi
    pypitest

[pypitest]
repository = https://test.pypi.org/legacy/
username = <your user name>

[pypi]
repository = https://pypi.org/legacy/
username = <your user name>
```

Next, we can upload the package using twine to the test PyPI site.


```
(🐙)/dominion/dominion/object_model/
$ poetry run twine upload -r pypitest -p <redacted> dist/*

Uploading distributions to https://test.pypi.org/legacy/
Uploading dominion-object-model-1.0.0.tar.gz
100%|███████████████████████████████████████████████████████████████████████████████████████| 8.91k/8.91k [00:01<00:00, 5.00kB/s]

View at:
https://test.pypi.org/project/dominion-object-model/1.0.0/
```

To upload 

