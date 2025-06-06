def runge_cutt(f, y0, x0, xn, h):
    res = [(x0, y0)]
    xi = x0
    yi = y0

    while xi <= xn:
        k1 = h * f(xi, yi)
        k2 = h * f(xi + h / 2, yi + k1 / 2)
        k3 = h * f(xi + h / 2, yi + k2 / 2)
        k4 = h * f(xi + h, yi + k3)

        yi += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        xi += h
        res.append((xi, yi))


    return res
