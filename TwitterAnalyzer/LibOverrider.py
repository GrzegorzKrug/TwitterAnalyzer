# LibOverrider.py
# Grzegorz Krug

import twitter

def overrider(display=True):
    def add_items_method(self):
        return self.__dict__.items()

    def __getitem__(cls, x, missing=None):
        return getattr(cls, x, missing)

    @classmethod
    def __getitem_class__(cls, x):
        return getattr(cls, x)

    # def get(self, key, other='n/a'):
    #     getattr(self, )


    twitter.User.items = add_items_method
    if display:
        print("New Method twitter.User.items")

    twitter.User.__getitem__ = __getitem__
    if display:
        print("User is subscriptable twitter.User.__getitem__")

    twitter.Status.items = add_items_method
    if display:
        print("New Method twitter.Status.items")
    
    twitter.Status.__getitem__ = __getitem__
    twitter.Status.get = __getitem__
    if display:
        print("Status is subscriptable twitter.Status.__getitem__")


    print('#' * 20, 'End of overloading.', '#' * 20, '\n')
