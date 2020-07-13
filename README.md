# Overview

This project is a Python implementation of the well-known card game [Dominion](https://en.wikipedia.org/wiki/Dominion_%28card_game%29)
# Installation

## Pre-requisites

- Install [pyenv](https://github.com/pyenv/pyenv) or [pyenv-win](https://github.com/pyenv-win/pyenv-win)
- Install [poetry](https://python-poetry.org/docs/#installation)

Create a Python 3.8.2 environment

```
$ pyenv install 3.8.2

$ pyenv local

$ poetry env use 3.8.2

$ poetry install
```


# Running the game (self-test)

```
$ poetry run python self-test/main.py
```

# Testing

```
$ poetry run python -m unittest discover -s . -p '*_test.py' -v
```

# Concepts

## Zones

Zones are areas that contain cards. A card is always in exactly one zone.

### Supply piles

The kingdom cards, the treasures, the victory cards and the curses are all considered supply piles.
Each such pile contain cards of the same type and can be implemented as a simple counter (how many cards
of this type remain in the pile) 

### Player hand

The player hand is an unordered collection of cards. The human player may organize and order them for, but that is
for human display only. It doesn't affect the game state or the other players in any way. The only relevant
information is what cards are in the player's hand.

### Play area

When a player plays an action card the card moves out of their hand to the play area until the end of turn.

### Draw deck

The draw deck is a stack of cards that the player draws their hands from at the beginning of their turn and sometimes more
cards during their turn or other players' turns. Cards are sometimes put back on top of the draw deck or pushed to the
bottom of the deck.

### Player Discard pile

The discard pile is another stack of cards. When the draw deck is exhausted the discard pile is shuffled and all of its
cards are added to the draw deck. 

### Trash

The trash is where cards that are removed from the game go. If the rules allow recovering trashed cards then the trash
needs to keep the cards as a collection or stack.

### Unused

Dominion has many cards and only some of them are used in each game.
All cards that are not used in the current game are considered to be
in the unused zone

## Game Manager

The game manager is an entity that manages the game state, enforces the game rules and
controls the workflow of the game. In particular it allows actors to take valid actions
based on initiative.

## Actors

Actors are entities that cn take actions. In dominion the only actors are players.
There are human and computer players, but conceptually both are actors. Specifically,
the game engine doesn't distinguish between them and treats all actors exactly the same.

## Initiative

The initiative is the ability to take action at a given moment, Dominion is a turn-based game.
Players get the initiative on after the other. In some situations, other players can react to
the active player's action.

# Architecture

## Game engine

The game engine is responsible for all the generic aspects of teh game that can be applied to many similar games:

- managing the players
- transitioning from player to player when turns end
- check for end of game 

## Game

The game object is where all the domain-specific knowledge exists.

## Player State

The game state is the data that the game object operates on.

### Personal Player State

The personal game state is the state that each player is allowed to see.
The game frequently syncs the personal game state to reflect the real game state


## Players

There are two types of players: human players and computer players (a.k.a AI).
From the game's point of view they are identical and the interaction is
through the Player interface

```
class Player(metaclass=ABCMeta):
    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def respond(self, action, *args):
        """The player should return a proper response to the specific request

        this method may be called during the play of the active player
        while they play an action card on the active player and/or other
        players.

        Example:
            - in response to militia card all other players must discard to 3 cards
            - in response to an attack card, each player with  moat may block the attack
            - in response to a thief, the active player must select if/who to steal from
        """
        pass

    @abstractmethod
    def on_event(self, event):
        pass
```

### Human players

Human players will use a user interface client program that understands the Dominion protocol,
display relevant information to the human player and interact with the game on behalf of the
human via the Player interface.

### Computer players

Computer players implement the Player interface as well and implement some algorithm.
There are several computer players that come with the game. check out the `computer_players`
directory.

## Cards

Cards in dominion have attributes like name, type, description, cost and victory points. Some cards are also reaction
cards, which means they can counteract an attack by another player.

### Card collections

Card collections are just unordered collections of cards. 

### Card stacks

Card stacks behave like stacks and allow operations like:
- pop
- peek
- add on top
- push to bottom

# Reference

Game rules can be found here:
https://entertainment.howstuffworks.com/leisure/brain-games/dominion3.htm

Cards description here:
http://wiki.dominionstrategy.com/index.php/List_of_cards

Multiplayer game library:
https://github.com/chr15m/PodSixNet/

