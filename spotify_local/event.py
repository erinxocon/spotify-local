class Event:
    def __init__(self):
        self.handlers: set = set()

    def __iadd__(self, handler):
        print(handler)
        self.handlers.add(handler)

    def __isub__(self, handler):
        try:
            self.handlers.remove(handler)
        except KeyError:
            raise ValueError("Can't unhandle the handle as it's not currently handled.")

    def __call__(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)
