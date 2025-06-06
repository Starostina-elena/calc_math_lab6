from .runge_cutt import runge_cutt

def adams(f, y0, x0, xn, h):
    res = runge_cutt(f, y0, x0, x0 + 3 * h, h)
    f_res = [f(x, y) for x, y in res]

    xi = x0 + 4 * h

    while xi <= xn:

        delta_fi = f_res[-1] - f_res[-2]
        delta_fi_2 = f_res[-1] - 2 * f_res[-2] - f_res[-3]
        delta_fi_3 = f_res[-1] - 3 * f_res[-2] + 3 * f_res[-3] - f_res[-4]

        yi = res[-1][1] + h * f_res[-1] + h ** 2 / 2 * delta_fi + h ** 3 * 5 / 12 * delta_fi_2 + h ** 4 * 3 / 8 * delta_fi_3

        res.append((xi, yi))
        f_res.append(f(xi, yi))
        xi += h

    return res
