from time import sleep
from random import randint


def have_a_rest(mode: int) -> None:
    """
    mode:
    1 -> (1;5)
    2 -> (5;10)
    3 -> (10;20)
    4 -> (20;30)
    5 -> (30;40)
    :param mode:
    :return:
    """
    match mode:
        case 1:
            sleep(randint(1, 5))
        case 2:
            sleep(randint(5, 10))
        case 3:
            sleep(randint(10, 20))
        case 4:
            sleep(randint(20, 30))
        case 5:
            sleep(randint(30, 40))
        case _:
            print("Не допустимый входной параметр")
