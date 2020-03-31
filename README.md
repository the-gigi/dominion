# Overview

# Concepts

## Zones

Zones are areas that contain cards. A card is always in exactly one zone.

### Draw piles

### Player hand

### Player deck

### Player discard pile

### Trash

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

## Players

There are two types of players


### Human players

### Computer players

## Cards

## Card collection


# Reference

Game rules can be found here:
https://entertainment.howstuffworks.com/leisure/brain-games/dominion3.htm

Cards description here:
http://wiki.dominionstrategy.com/index.php/List_of_cards