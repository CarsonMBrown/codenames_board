from random import randint
from kivy import Config

Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('kivy', 'desktop', 1)
Config.set('graphics', 'fullscreen', "auto")

from kivy.app import App
from kivy.graphics.svg import Window
from kivy.properties import Property
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen


class Card(Button):
    def __init__(self, word, identifier, **kwargs):
        super().__init__(**kwargs)
        self.text = word
        self.id = identifier
        self.card_type = 0
        self.font_name = 'theme/font'
        self.font_size = 30
        self.halign = 'center'
        self.valign = 'middle'
        self.background_normal = 'theme/message.png'
        self.color = [0, 0, 0, 1]

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            print(self.text_size, self.size, self.texture_size)
            # print(touch.button)
            if touch.button == "left":
                if 'blue' in self.background_normal:
                    self.background_normal = 'theme/message.png'
                    self.color = [0, 0, 0, 1]
                else:
                    self.background_normal = 'theme/blue_' + str(randint(1,2)) + '.png'
                    self.color = [1, 1, 1, 1]
            elif touch.button == "right":
                if 'red' in self.background_normal:
                    self.background_normal = 'theme/message.png'
                    self.color = [0, 0, 0, 1]
                else:
                    self.background_normal = 'theme/red_' + str(randint(1,2)) + '.png'
                    self.color = [1, 1, 1, 1]
            elif touch.button == "middle":
                if 'grey' not in self.background_normal and 'black' not in self.background_normal:
                    self.background_normal = 'theme/grey_' + str(randint(1,2)) + '.png'
                    self.color = [1, 1, 1, 1]
                elif 'grey' in self.background_normal:
                    self.background_normal = 'theme/black_1.png'
                    self.color = [1, 1, 1, 1]
                elif 'black' in self.background_normal:
                    self.background_normal = 'theme/message.png'
                    self.color = [0, 0, 0, 1]


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        f = open("words.txt")
        self.all_words = f.read().split(",")
        self.layout = GridLayout()
        self.layout.cols = 5
        self.layout.id = "board"
        self.layout.spacing = [10, 10]
        self.add_widget(self.layout)

        self.create_cards()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print(keycode, text, modifiers)
        if keycode[1] == 'spacebar':
            self.create_cards()
            return True
        else:
            return False

    def create_cards(self):
        self.layout.clear_widgets()
        for i in range(25):
            self.layout.add_widget(Card(self.random_word(), str(i)))

    def random_word(self):
        r = randint(0, len(self.all_words) - 1)
        word = self.all_words[r]
        self.all_words.remove(word)
        return word.strip()


class MainApp(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MainApp().run()
