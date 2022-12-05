from random import randint

from sea_exceptions import BoardOutException, BoardAlreadyHitException, BoardWrongShipException, BoardException


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, bow, length, place):
        self.bow = bow
        self.length = length
        self.o = place
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["o"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def __str__(self):
        res = ''
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + ' |'

        if self.hid:
            res = res.replace("■", 'o')
        return res

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def shot(self, s):
        if self.out(s):
            raise BoardOutException()

        if s in self.busy:
            raise BoardAlreadyHitException()

        self.busy.append(s)

        for ship in self.ships:
            if s in ship.dots:
                ship.lives -= 1
                self.field[s.x][s.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Корабль был уничтожен')
                    return False
                else:
                    print('Корабль подбит')
                    return True

        self.field[s.x][s.y] = '.'
        print('Промах')
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        return NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        shot = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход противника: {shot.x + 1} {shot.y + 1}')
        return shot


class User(Player):
    def ask(self):
        while True:
            cords = input('Введите координаты: ').split()

            if len(cords) != 2:
                print('Введите две координаты')
                continue

            x, y = cords

            if not (x.isdigit() or not (y.isdigit())):
                print('Введите число: ')
                continue

            x, y = int(x) - 1, int(y) - 1

            return Dot(x, y)


class Game:
    def __init__(self, size=6):
        self.size = size
        user = self.random_board()
        bot = self.random_board()
        bot.hid = True

        self.user = User(user, bot)
        self.bot = AI(bot, user)

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def try_board(self):
        len_boats = [3, 2, 2, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for len_boat in len_boats:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), len_boat, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    @staticmethod
    def greet():
        print('Это игра морской бой')
        print('Вам нужно ввести координату x или y,')
        print('чтобы подбить чужой корабль.')
        print('Да победит сильнейший!')
        print('\n')

    def loop(self):
        num = 0
        while True:
            print("Доска пользователя:")
            print(self.user.board)
            print('\n')
            print("Доска компьютера:")
            print(self.bot.board)
            print('\n')
            if num % 2 == 0:
                print("Ходит пользователь")
                repeat = self.user.move()
            else:
                print("Ходит компьютер")
                repeat = self.bot.move()
            if repeat:
                num -= 1

            if self.bot.board.count == 7:
                print("Пользователь выиграл")
                break

            if self.bot.board.count == 7:
                print("Компьютер выиграл\n")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


if __name__ == '__main__':
    g = Game()
    g.start()
