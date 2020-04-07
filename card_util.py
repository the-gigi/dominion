import cards
import inspect

def get_card_types():
    return [cls for _, cls in inspect.getmembers(cards) if inspect.isclass(cls) and cls != cards.BaseCard]
