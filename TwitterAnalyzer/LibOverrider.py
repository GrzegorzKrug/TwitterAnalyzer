# LibOverrider.py
# Grzegorz Krug

import twitter

def overrider(display=True):
    def show_user_items(self):
        return self.__dict__.items()

    twitter.User.items = show_user_items
    if display:
        print("New Method twitter.User.items")
    
