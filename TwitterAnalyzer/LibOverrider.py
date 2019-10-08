# LibOverrider.py
# Grzegorz Krug

import twitter

def overrider(display=True):
    def show_user_items(self):
        return self.__dict__.items()

    def __getitem__(cls, x):
        return getattr(cls, x)

    twitter.User.items = show_user_items
    if display:
        print("New Method twitter.User.items")

    twitter.User.__getitem__ = __getitem__
    if display:
        print("User is subscriptable twitter.User.__getitem__")
    
