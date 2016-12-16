from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Ball(Widget):
    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.velocity = Vector(5, 5)
        self.served_ball = False
        with self.canvas:
            Color(rgba=(0, 1, 1, 1))
            Ellipse(size=(100, 100), pos=self.pos)

    def on_touch_down(self, touch):
        self.served_ball = True

    def update(self):
        if self.served_ball:
            self.x += self.velocity.x
            self.y += self.velocity.y
            self.canvas.clear()
            with self.canvas:
                Color(rgba=(0, 1, 1, 1))
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


class Piece(Widget):
    def __init__(self, **kwargs):
        super(Piece, self).__init__(**kwargs)
        self.size = (150, 50)
        self.inner_size = (148, 48)
        self.inner_pos = (self.x + 1, self.y + 1)
        with self.canvas:
            Color(rgba=(.8, .3, .1, 1))
            Rectangle(size=self.inner_size, pos=self.inner_pos)


class Wall(Widget):
    def __init__(self, **kwargs):
        super(Wall, self).__init__(**kwargs)
        self.count = 0
        for i in range(3):
            self.add_widget(Piece(pos=(150*i, 400)))
            self.count += 1



class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.size = Window.size
        self.paddle = Paddle(self.center_x)
        self.add_widget(self.paddle)
        self.ball = Ball(pos=(self.paddle.x, self.paddle.top+5))
        self.add_widget(self.ball)
        self.wall = Wall()
        self.add_widget(self.wall)

        Clock.schedule_interval(self.update, 1.0/60.0)

    def bounce_ball_paddle(self):
        if self.ball.y >= self.paddle.top:
            self.ball.velocity.y *= -1
        else:
            self.ball.velocity.x *= -1

    def bounce_ball_wall(self, a_wall):
        if self.ball.center_y < a_wall.y or self.ball.center_y > a_wall.top:
            self.ball.velocity.y *= -1
        else:
            self.ball.velocity.x *= -1

    def update(self, dt):
        if self.wall.count == 0:
            print("no more walls")
            Clock.unschedule(self.update) # sleep the loop
            self.end_game("Restart a Game")
        else:
            self.ball.update()
            #Bouncing Paddle
            if self.ball.collide_widget(self.paddle):
                self.bounce_ball_paddle()
            #Boucing Wall
            for wall in self.wall.children:
                if self.ball.collide_widget(wall):
                    self.wall.count -= 1
                    self.bounce_ball_wall(wall)
                    self.wall.remove_widget(wall)
                    del wall
            #Bouncing Ball
            if self.ball.y > self.height - self.ball.height:
                self.ball.velocity.y *= -1
            if self.ball.x < 0 or self.ball.x > self.width - self.ball.width:
                self.ball.velocity.x *= -1
            if self.ball.y < 0 - self.ball.height:
                Clock.unschedule(self.update) # sleep the loop
                self.end_game("Restart a Game")
        ##########################################
        #Dont implement any logic after this line#
        ##########################################

    def end_game(self, a_text):
        self.remove_widget(self.ball)
        self.remove_widget(self.paddle)
        self.remove_widget(self.wall)
        del self.ball
        del self.paddle
        del self.wall
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(Menu(a_text))
        del self



class Menu(Widget):
    def __init__(self, text, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.text = text
        self.size = Window.size
        self.start_button = Button(text=self.text,
                                   font_size=self.width*0.08)
        self.start_button.size = (self.width*0.6, self.height*0.2)
        self.start_button.center_x = self.center_x
        self.start_button.center_y = self.center_y
        self.start_button.bind(on_press=self.start_btn_cb)
        self.add_widget(self.start_button)

    def start_btn_cb(self, instance):
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(Game())



class WallBreakerApp(App):
    def build(self):
        top = Widget(size=Window.size)
        menu = Menu("Start A Game")
        top.add_widget(menu)
        return top

if __name__ == '__main__':
    WallBreakerApp().run()
