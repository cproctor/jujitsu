from jujitsu_library import jujitsu_server, cards
from hestiaflame_jujitsu_v2_fixed import chris_version_of_myplayer

def next_highest_card(hand, card_to_beat):
    """Given a hand and a target, returns the lowest card that is
    higher than the target card. If no such card exists, returns
    None."""
    cards_at_or_above_target = filter(lambda card: card > card_to_beat, hand)
    if any(cards_at_or_above_target):
        return min(cards_at_or_above_target)

def surrender(hand):
    """Returns the worst card in a hand. This is the lowest card that's not 1,
    if there is one. Otherwise returns 1."""
    non_one_cards = filter(lambda card: card != 1, hand)
    if any(non_one_cards):
        return min(non_one_cards)
    elif any(hand):
        return 1

def get_opponent_name(state, my_name):
    if any(state['history']):
        names = state['history'][0].keys()
        names.remove('treasure')
        names.remove(my_name)
        return names[0]

def make_sneaky_player(opponent):
    "Makes a sneaky jujitsu player, designed to beat a particular opponent"
    def sneaky_player(state, player_name):
        hand = cards(player_name, state['history'])
        opponent_name = get_opponent_name(state, player_name) or "ANONYMOUS"
        opponent_choice = opponent(state, opponent_name)
        return next_highest_card(hand, opponent_choice) or surrender(hand)
    return sneaky_player

sneak = make_sneaky_player(chris_version_of_myplayer)
server = jujitsu_server(sneak)
server.run(host="0.0.0.0", port="6789")
