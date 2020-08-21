from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
import random


class StartScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create box layout
        self.layout = BoxLayout(orientation='vertical')

        # create the label and button widgets
        self.instruction_label = Label(
            text="Welcome to NuMery!\n\nKey in the numbers displayed to proceed to the next stage!",
            font_size=22, halign='center')
        self.start_button = Button(text='Start', font_size=30, on_press=self.change_to_game)

        # add widgets to screen layout and add layout to screen
        self.layout.add_widget(self.instruction_label)
        self.layout.add_widget(self.start_button)
        self.add_widget(self.layout)

    def change_to_game(self, value):

        self.manager.transition.direction = 'left'
        self.manager.current = 'game'


# Generate a number of length that is equals to stage number
def number_generator(stage):
    range_start = 10 ** (stage - 1)
    range_end = (10 ** stage) - 1
    number_generated = random.randint(range_start, range_end)
    return number_generated


class GameScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # initialize game!
        self.stage = 1
        self.numbers = number_generator(self.stage)

        # create box layout
        self.layout = BoxLayout(orientation='vertical')

        # create the labels, text input and button
        self.stage_label = Label(text="Stage {:d}".format(self.stage), font_size=20)
        self.number_list_label = Label(text="{:d}".format(self.numbers), font_size=20)
        self.player_inp = TextInput(multiline=False, halign='center', padding_y=[50, 0], font_size=20)
        self.inp_button = Button(text='OK', font_size=20, on_press=self.gameStart)

        # adding widgets to screen
        self.layout.add_widget(self.stage_label)
        self.layout.add_widget(self.number_list_label)
        self.layout.add_widget(self.player_inp)
        self.layout.add_widget(self.inp_button)
        self.add_widget(self.layout)

    def gameStart(self, value):

        if self.player_inp.text == str(self.numbers):

            # increase stage and regenerate number
            self.stage += 1
            self.numbers = number_generator(self.stage)

            # reset widgets text
            self.stage_label.text = 'Stage ' + str(self.stage)
            self.number_list_label.text = str(self.numbers)
            self.player_inp.text = ''

            # animate numbers to appear/disappear
            anim = Animation(opacity=1, duration=0) + Animation(opacity=0, duration=3)
            anim.start(self.number_list_label)

        else:

            # reset stage to 1 and regenerate number
            self.stage = 1
            self.numbers = number_generator(self.stage)

            # reset widgets text
            self.stage_label.text = 'Stage ' + str(self.stage)
            self.number_list_label.text = str(self.numbers)
            self.player_inp.text = ''

            # animate number to appear
            Animation(opacity=1, duration=2).start(self.number_list_label)

            # move to lose screen
            self.manager.transition.direction = 'left'
            self.manager.current = 'lose'


class LoseScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')
        self.lose_label = Label(text='You keyed the wrong number!\n\nYou lose!', font_size=20, halign='center')
        self.restart_button = Button(text='Restart', font_size=20, on_press=self.change_to_game)
        self.layout.add_widget(self.lose_label)
        self.layout.add_widget(self.restart_button)
        self.add_widget(self.layout)

    def change_to_game(self, value):
        self.manager.transition.direction = 'left'
        self.manager.current = 'game'


class SwitchScreenApp(App):

    def build(self):

        sm = ScreenManager()

        # set the names of each screen to call them when switching screens
        ss = StartScreen(name='start')
        gs = GameScreen(name='game')
        ls = LoseScreen(name='lose')

        # add the start and game screens as widgets to screen manager
        sm.add_widget(ss)
        sm.add_widget(gs)
        sm.add_widget(ls)

        # the first screen is the 'start' screen, corresponding to StartScreen
        sm.current = 'start'
        return sm


SwitchScreenApp().run()
