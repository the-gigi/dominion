# Overview


# Running the game

```
python3 dominion.py
```

# Testing

```
python3 -m unittest discover -s . -p '*_test.py' -v
```

# Concepts

## Zones

Zones are areas that contain cards. A card is always in exactly one zone.

### Supply piles

The kingdom cards, the treasures, the victory cards and the curses are all considered supply piles.
Each such pile contain cards of the same type and can be implemented as a simple counter  (how many cards 
of this type remain in the pile) 

### Player hand

The player hand is an unordered collection of cards. The human player may organize and order them for, but that is
for human display only. It doesn't effect the game state or the other players in any way. The only relevant 
information is what cards are in the player's hand.

### Play area

When a player plays an action card the card moves out of their hand to the play area until the end of turn.

### Draw deck

The draw deck is a stack of cards that the player draws their hands at the beginning of their turn and sometimes more 
cards during the turn or other players turn. Cards are sometimes put back on top of the draw deck or pushed to the 
bottom of the deck.

### Player Discard pile

The discard pile is another stack of cards. When the draw deck is exhausted the discard pile is shuffled and all its 
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


## Players

There are two types of players: human players and computer players (a.k.a AI).

### Human players

Human players

### Computer players

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