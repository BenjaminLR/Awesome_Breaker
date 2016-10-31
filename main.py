from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Ball(Widget):
    def __init__(self, center, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.velocity = Vector(5, 5)
        self.pos = center
        with self.canvas:
            Color(rgba=(1, 0, 1, .8))
            Ellipse(size=(100, 100), pos=self.pos)

    def move(self):
        self.x += self.velocity.x
        self.y += self.velocity.y
        self.canvas.clear()
        with self.canvas:
            Color(rgba=(1, 0, 1, 1))
            Ellipse(size=(100, 100), pos=(self.x, self.y))


class Paddle(Widget):
    def __init__(self, center, **kwargs):
        super(Paddle, self).__init__(**kwargs)
        self.size = 200, 40
        self.pos = center-self.width/2, 20
        with self.canvas:
            Color(rgba=(1, 1, 1, 1))
            Rectangle(size=self.size, pos=self.pos)

    def on_touch_move(self, touch):
        self.center_x = touch.x
        self.update()

    def update(self):
        self.canvas.clear()
        with self.canvas:
            Rectangle(size=self.size, pos=self.pos)


class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.paddle = Paddle(self.center_x)
        self.add_widget(self.paddle)
        self.ball = Ball(self.center)
        self.add_widget(self.ball)

        Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, dt):
        self.ball.move()
        #Bouncing Ball
        if self.ball.y > self.height - self.ball.height:
            self.ball.velocity.y *= -1
        if self.ball.x < 0 or self.ball.x > self.width - self.ball.width:
            self.ball.velocity.x *= -1
        if self.ball.y < 0 - self.ball.height:
            self.remove_widget(self.ball)
            print('game over')


class Menu(Widget):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.start_button = Button(text='Start a Game',
                                   font_size=self.width*0.1)
        self.start_button.size = (self.width*0.6, self.height*0.2)
        self.start_button.center_x = self.center_x
        self.start_button.center_y = self.center_y
        self.start_button.bind(on_press=self.start_btn_cb)
        self.add_widget(self.start_button)

    def start_btn_cb(self, instance):
        print('button clicked')



class WallBreakerApp(App):
    def build(self):
        # game = Game(size=Window.size)
        menu = Menu(size=Window.size)
        return menu

if __name__ == '__main__':
    WallBreakerApp().run()
