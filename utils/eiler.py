def eiler(f, y0, x0, xn, h):
    res = [(x0, y0)]
    xi = x0 + h
    yi = y0 + h * f(x0, y0)

    while xi <= xn:
        res.append((xi, yi))
        yi = yi + h * f(xi, yi)
        xi += h

    return res
