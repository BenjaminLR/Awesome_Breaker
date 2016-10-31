from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Ball(Widget):
    def __init__(self, center, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.velocity = Vector(1, 1)
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


class WallBreakerApp(App):
    def build(self):
        game = Game(size=Window.size)
        return game

if __name__ == '__main__':
    WallBreakerApp().run()
