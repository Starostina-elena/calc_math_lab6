def eiler(f, y0, x0, xn, h):
    res = [(x0, y0)]
    xi = x0 + h
    yi = y0 + h * f(x0, y0)

    while xi - xn <= 0.001:
        res.append((xi, yi))
        yi = yi + h * f(xi, yi)
        xi += h

    return res


def eiler_find_h_for_eps(f, y0, x0, xn, h, eps):
    res = eiler(f, y0, x0, xn, h)

    while True:
        new_res = eiler(f, y0, x0, xn, h / 2)
        if abs(new_res[1][1] - res[1][1]) < eps:
            return h
        res = new_res
        h /= 2