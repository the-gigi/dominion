class Player():
    def __init__(self):
        """ """
        self._name = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

