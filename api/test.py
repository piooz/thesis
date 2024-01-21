import logging

import algorithm as a

arparams = [1, 0, 0, 1, -1]
maparams = [-0.6, 0, 0, -0.6, 0.36]


def io_effect_test():

    calc = a.io_effect(11, 0, arparams, maparams, 1)
    logging.debug(calc)
    expected = [
        1.00,
        0.40,
        0.40,
        0.40,
        0.80,
        0.56,
        0.56,
        0.56,
        0.96,
        0.72,
        0.72,
    ]
    assert len(calc) == len(
        expected
    ), f'not expected lenght {len(calc)} != {len(expected)}'
    for e, c in zip(expected, calc):
        assert round(e) == round(
            c
        ), f'io effect is not correct {calc == expected} output: {calc}, expected {expected} e:{e} c:{c}'


if __name__ == '__main__':

    io_effect_test()
