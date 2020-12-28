from typing import List

from dominion_game_engine.card_util import get_card_class
from dominion_game_engine.hand import has_card_type, select_by_name, remove_by_name, has_card_names
from dominion_game_engine.cards import *


# def play_adventurer(game):
#     treasures = 0
#     deck = game.player_state.draw_deck
#     while treasures < 2:
#         game.player_state.reload_deck(1)
#         top_card = deck.pop(1)[0]
#         if top_card.Type == 'Treasure':
#             game.player_state.hand.append(top_card)
#             treasures += 1
#         else:
#             game.player_state.discard_pile.add_to_top([top_card])


def play_bandit(game):
    """
    Gain a gold.

    Each other player reveals the top 2 cards of their deck,
    trashes a revealed Treasure other than Copper, and discards the rest.
    """

    def choose_treasure(response, trash_candidates):
        # Two candidates. See if response matches and return it
        if response in trash_candidates:
            return response

        # If not pick first
        return next(iter(trash_candidates))

    if not game._is_pile_empty('Gold'):
        game.piles['Gold'] -= 1
        game.player_state.discard_pile.add_to_top([Gold()])
    for player, player_state in game.other_players:
        top_two = [c for c in player_state.draw_deck.peek(2)]
        trash_candidates = set(x for x in top_two if x.Name() in ('Silver', 'Gold'))
        # No non-copper treasures. nothing to choose from
        if not trash_candidates:
            continue

        # One non-copper treasure. No choice
        elif len(trash_candidates) == 1:
            treasure = next(iter(trash_candidates))
        else:
            response = game._respond(player, 'Bandit', trash_candidates)
            treasure = choose_treasure(response, trash_candidates)

        player_state.draw_deck.pop(treasure)
        other = player_state.draw_deck.pop
        player_state.discard_pile.add_to_top(other)


def play_bureaucrat(game):
    """
        Gain a silver card; put it on top of your deck.
        Each other player reveals a Victory card from
        his hand and puts it on top of his deck (or reveals
        a hand with no Victory cards).
    """

    def choose_victory(response):
        if response is None or response.Type != 'Victory':
            for c in player_state.hand:
                if c.Type == 'Victory':
                    return c
            return None

        for c in player_state.hand:
            if isinstance(c, response):
                return c
        return None

    if not game._is_pile_empty('Silver'):
        game.piles['Silver'] -= 1
        game.player_state.draw_deck.add_to_top([Silver()])
    for player, player_state in game.other_players:
        response = game._respond(player, 'Bureaucrat')
        victory = choose_victory(response)
        if victory is not None:
            player_state.draw_deck.add_to_top([victory])
            player_state.hand.remove(victory)


# def play_chancellor(game):
#     """
#     +$2
#
#     You may immediately put your deck into your discard pile.
#     """
#     # TO DO - Ask player if they want to put their deck into their discard pile


def play_chapel(game):
    """
    Trash up to 4 cards from your hand.
    """
    cards_to_trash = game._respond(game.player, 'Chapel')
    if not isinstance(cards_to_trash, List) or len(cards_to_trash) == 0 or len(cards_to_trash) > 4:
        return

    if not has_card_names(game.player_state.hand, cards_to_trash):
        return

    # trash the selected cards
    remove_by_name(game.player_state.hand, cards_to_trash)


def play_cellar(game):
    """
    +1 Action

    Discard any number of cards, then draw that many.
    """
    game.player_state.actions += 1

    cards_to_discard = game._respond(game.player, 'Cellar')
    if not isinstance(cards_to_discard, List) or len(cards_to_discard) == 0:
        return

    if not has_card_names(game.player_state.hand, cards_to_discard):
        return

    # discard the selected cards
    discarded = remove_by_name(game.player_state.hand, cards_to_discard)
    game.player_state.discard_pile.add_to_top(discarded)

    # draw new cards
    game.player_state.draw_cards(len(cards_to_discard))


def play_council_room(game):
    """
    +4 Cards
    +1 Buy

    Each other player draws a card.
    """
    game.player_state.draw_cards(3)
    game.player_state.buys += 1
    for player_state in game.player_states:
        player_state.draw_cards(1)


def play_festival(game):
    """
    +2 Actions
    +1 Buy
    +$2
    """
    game.player_state.actions += 2
    game.player_state.buys += 1


def play_harbinger(game):
    """
    +1 Card
    +1 Action

    Look through your discard pile. You may put a card from it onto your deck.
    """
    game.player_state.draw_cards(1)
    game.player_state.actions += 1

    if len(game.player_state.discard_pile) == 0:
        return

    card_to_put_on_deck = game._respond(game.player, 'Harbinger')
    if not card_to_put_on_deck:
        return

    card = None
    for c in game.player_state.discard_pile.cards:
        if c.Name() == card_to_put_on_deck:
            card = c
            game.player_state.draw_deck.add_to_top([card])
            break

    if card is not None:
        game.player_state.discard_pile.cards.remove(card)


def play_market(game):
    """
    +1 Card
    +1 Action
    +1 Buy
    +$1
    """
    game.player_state.draw_cards(1)
    game.player_state.actions += 1
    game.player_state.buys += 1


def play_militia(game):
    """
    +$2

    Each player discards down to 3 cards in his hand.
    """

    def choose_hand(response, player_state):
        """The expected response is a set of 3 cards from the player's hand

        If the response is different return None
        """
        h = player_state.hand
        if response == 'Moat':
            if has_card_type(h, 'Moat'):
                return None

        if not isinstance(response, List) or len(response) > min(len(h), 3):
            return player_state.hand[:3]

        if not has_card_names(h, response):
            return player_state.hand[:3]

        new_hand = select_by_name(h, response)
        return new_hand

    for player, player_state in game.other_players:
        if Moat in set(c.Name() for c in player_state.hand):
            continue

        if len(player_state.hand) <= 3:
            continue

        response = game._respond(player, 'Militia')
        hand = choose_hand(response, player_state)
        if hand is None:
            continue
        discarded = [c for c in player_state.hand if c not in hand]

        player_state.hand = hand
        player_state.discard_pile.add_to_top(discarded)
        game.send_personal_state()


def play_moneylender(game):
    """
    You may trash a Copper from your hand for +$3.
    """
    if not has_card_names(game.player_state.hand, 'Copper'):
        return

    # Trash the money lender card
    remove_by_name(game.player_state.hand, 'Copper')
    # Add 3 money
    game.player_state.used_money -= 3


def play_moat(game):
    """
    The active player draws 2 cards and adds them to their hand.

    Counter - When another player plays an Attack card, you may first
    reveal this from your hand, to be unaffected by it.
    """
    game.player_state.draw_cards(2)


def play_smithy(game):
    """
    +3 Cards
    """
    game.player_state.draw_cards(3)


# def play_spy(game):
#     """+1 Card
#     +1 Action
#
#     Each player (including you) reveals the top card of his deck
#     and either discards it or puts it back, your choice.
#     """
#     game.player_state.draw_cards(1)
#     game.player_state.actions += 1
#
#     top_cards = {}
#     for player_state in game.player_states:
#         player_state.reload_deck(1)
#         top_card = player_state.draw_deck.cards[0]
#         top_cards[player_state.name] = top_card
#     top_card_names = [card.Name() for card in top_cards.values()]
#     response = game.player.respond('Spy', *top_card_names)
#     if response is None:
#         return
#     for player_state in game.player_states:
#         if player_state.name in response and response[player_state.name] == 'discard':
#             card = player_state.draw_deck.pop(1)
#             player_state.discard_pile.cards += card
#
# def play_thief(game):
#     """ Each other player reveals the top 2 cards of his deck.
#     If they revealed any Treasure cards, they trash one of them that you choose.
#     You may gain any or all of these trashed cards.
#     They discard the other revealed cards.
#     """
#     treasure_dict = {}
#     for name, player_state in game.other_players:
#         if player_state.draw_deck.count < 2:
#             n = 2 - player_state.draw_deck.count
#             player_state.discard_pile.shuffle()
#             top_n = player_state.discard_pile.pop(n)
#             player_state.draw_deck.add_to_bottom(top_n)
#
#         top_2 = player_state.draw_deck.peek(2)
#         treasures = [c for c in top_2 if c.Type == 'Treasure']
#         treasure_dict[name] = treasures
#     response = game.player.respond('Thief', [card.Name() for cards in treasure_dict.values() for card in cards])
#     if response is None:
#         return
#
#     for name, player_state in game.other_players:
#         top_2 = player_state.draw_deck.pop(2)
#         discard = player_state.discard_pile.add_to_top
#         gain = game.player_state.discard_pile.add_to_top
#
#         index, action = response[name]
#         if index == 0:
#             discard(top_2[1])
#             if action == 'gain':
#                 gain(top_2[0])
#         elif index == 1:
#             discard(top_2[0])
#             if action == 'gain':
#                 gain(top_2[1])
#         else:
#             discard(top_2[0])
#             discard(top_2[1])


def play_throne_room(game):
    """
    You may play an Action card from your hand twice.
    """
    ps = game.player_state
    card_name = game._respond(game.player, 'ThroneRoom')

    # Play the requested action action card for the first time
    result = game.play_action_card(card_name)
    if result:
        # Return the action card from the play area to the hand and play it again
        card = ps.pop()
        if card.Name() != card_name:
            raise RuntimeError('Something went wrong during throne room!')
        ps.hand.append(card)
        game.play_action_card(card_name)


def play_witch(game):
    """
    +2 Cards

    Each other player gains a Curse.
    """
    game.player_state.draw_cards(2)
    for _, ps in game.other_players:
        if Moat in set(type(c) for c in ps.hand):
            continue

        if game.piles['Curse'] == 0:
            break
        ps.discard_pile.add_to_top([Curse()])
        game.piles['Curse'] -= 1


def play_workshop(game):
    """
    Gain a card costing up to $4
    """
    card_name = game._respond(game.player, 'Workshop')
    card_class = get_card_class(card_name)
    if game.piles.get(card_name, 0) == 0 or card_class.Cost > 4:
        return

    game.piles[card_name] -= 1

    game.player_state.discard_pile.add_to_top([card_class()])
    game.send_game_event(f'{game.player_name} gained {card_name}')


def play_vassal(game):
    """
    +$2

    Discard the top card of your deck.
    If it is an Action card, you may play it.
    """
    game.player_state.reload_deck(1)
    card_name = game.player_state.draw_deck[0]
    play_card = game._respond(game.player, 'Vassal', card_name)
    if play_card:
        game.player_state.draw_cards(1)
        game.player_state.actions += 1
        game.play_action_card(card_name)


def play_village(game):
    """
    +1 Card
    +2 Actions
    """
    game.player_state.draw_cards(1)
    game.player_state.actions += 2
