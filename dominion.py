import inspect

import cards


def main():
    """ """
    for name, cls in inspect.getmembers(cards):
        if inspect.isclass(cls) and cls != cards.BaseCard:
            print('-' * 10)
            cls().dump()


if __name__ == '__main__':
    main()
