from kivy.event import EventDispatcher


class MyClass(EventDispatcher):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_test')  # 1

    def on_test(self, *args, **kwargs):  # 2
        pass

a = MyClass()
a.bind(on_test=lambda __, *args, **kwargs: print('on_test', args, kwargs))

a.dispatch('on_test')
print('-------------------')
a.dispatch('on_test', 12, 34, kivy='awesome', python='awesome')
