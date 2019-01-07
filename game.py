from microbit import *
import random

SHOT_INTERVAL = 150
ENEMY_SPAWN_INTERVAL = 800
ENEMY_MOVE_INTERVAL = 1000

SCORE = 0


class Aircraft:
    def __init__(self, x_p, y_p):
        self.__b = False
        self.__b_x = -1
        self.__b_y = 4
        self.__b_br = 8
        self.__b_fw = False
        self.__b_fe = False

        self.__a_x = x_p
        self.__a_y = y_p

        display.set_pixel(self.__a_x, self.__a_y, 9)

    def __make_bullet(self):
        self.__b = False
        self.__b_x = -1
        self.__b_y = 4
        self.__b_br = 8
        self.__b_fw = False
        self.__b_fe = False

    def move_right(self):
        if self.__a_x < 4:
            display.set_pixel(self.__a_x, self.__a_y, 0)
            self.__a_x += 1
            display.set_pixel(self.__a_x, self.__a_y, 9)

    def move_left(self):
        if self.__a_x > 0:
            display.set_pixel(self.__a_x, self.__a_y, 0)
            self.__a_x -= 1
            display.set_pixel(self.__a_x, self.__a_y, 9)

    # def killed_enemy(self):
    #     self.__b_fe = True

    def waste_bullet(self):
        self.__b = False

    def has_bullet(self):
        return self.__b

    def b_x(self):
        return self.__b_x

    def b_y(self):
        return self.__b_y

    def strike(self):
        if self.__b is False:
            self.__make_bullet()

            self.__b = True
            self.__b_x = self.__a_x

        if self.__b_fw:
            display.set_pixel(self.__b_x, self.__b_y, 0)
            self.__b = False
        else:
            if self.__b_y is not 4:
                display.set_pixel(self.__b_x, self.__b_y, 0)

            self.__b_y = self.__b_y - 1
            self.__b_br -= 1

            if self.__b_y is 0:
                self.__b_fw = True

            display.set_pixel(self.__b_x, self.__b_y, self.__b_br)


class Enemy:
    def __init__(self, x):
        self.__x = x
        self.__y = -1

    def x_pos(self):
        return self.__x

    def y_pos(self):
        return self.__y

    def increment_y(self):
        self.__y = self.__y + 1


class EnemyManager:
    def __init__(self):
        self.__l_e = None
        self.__en = []

    def spawn(self):
        enemy = None

        if self.__l_e is not None:
            last_enemy_x = self.__l_e.x_pos()

            if last_enemy_x is 0:
                enemy = Enemy(random.choice([1, 2, 3, 4]))
            elif last_enemy_x is 1:
                enemy = Enemy(random.choice([0, 2, 3, 4]))
            elif last_enemy_x is 2:
                enemy = Enemy(random.choice([0, 1, 3, 4]))
            elif last_enemy_x is 3:
                enemy = Enemy(random.choice([0, 1, 2, 4]))
            elif last_enemy_x is 4:
                enemy = Enemy(random.choice([0, 1, 2, 3]))
        else:
            enemy = Enemy(random.choice([0, 1, 2, 3, 4]))

        self.__l_e = enemy
        self.__en.append(enemy)

    def __show(self, enemy):
        display.set_pixel(enemy.x_pos(), enemy.y_pos(), 9)

    def __hide(self, enemy):
        display.set_pixel(enemy.x_pos(), enemy.y_pos(), 0)

    def kill(self, bullet_x, bullet_y):
        for i, enemy in enumerate(self.__en):
            if enemy.x_pos() is bullet_x and \
                    enemy.y_pos() is bullet_y:
                self.__hide(enemy)
                self.__en.remove(enemy)
                return True
        return False

    def move_forward(self):
        for enemy in self.__en:
            if enemy.y_pos() < 4:
                if enemy.y_pos() is not -1:
                    self.__hide(enemy)

                enemy.increment_y()
                self.__show(enemy)
            else:
                return False

        return True


enemy_manager = EnemyManager()
aircraft = Aircraft(2, 4)

time_list = [running_time(), running_time(), running_time()]

while True:
    if button_a.was_pressed():
        aircraft.move_left()
    elif button_b.was_pressed():
        aircraft.move_right()

    if running_time() - time_list[0] > SHOT_INTERVAL:
        aircraft.strike()
        time_list[0] = running_time()

    if running_time() - time_list[1] > ENEMY_SPAWN_INTERVAL:
        enemy_manager.spawn()
        time_list[1] = running_time()

    if running_time() - time_list[2] > ENEMY_MOVE_INTERVAL:
        if enemy_manager.move_forward() is False:
            display.scroll(SCORE)
            display.show(Image.HEART)
            break

        time_list[2] = running_time()

    if enemy_manager.kill(aircraft.b_x(), aircraft.b_y()):
        aircraft.waste_bullet()

        ENEMY_MOVE_INTERVAL -= 5
        ENEMY_SPAWN_INTERVAL -= 5

        SCORE += 1
