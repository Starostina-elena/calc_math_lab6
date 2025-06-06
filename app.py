from math import log, exp

from flask import Flask, render_template, request
from forms.InputForm import InputForm

from utils.adams import adams, adams_find_h_for_eps
from utils.eiler import eiler, eiler_find_h_for_eps
from utils.runge_cutt import runge_cutt, runge_cutt_find_h_for_eps

app = Flask(__name__)
app.secret_key = 'ajkdb^&yhjzxbd'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm()

    if form.validate_on_submit():
        try:
            if form.equation_choice.data == 'eq1':
                f = lambda x, y: 2 * x * y / (x ** 2 + 1)
                math_answer = lambda x, x0, y0: (x ** 2 + 1) * y0 / (x0 ** 2 + 1)
                desmos_equation = 'y=C * (x^2 + 1)'
                desmos_C = lambda x0, y0: y0 / (x0 ** 2 + 1)
            elif form.equation_choice.data == 'eq2':
                f = lambda x, y: y + (1 + x) * y ** 2
                math_answer = lambda x, x0, y0: -exp(x) / (x * exp(x) - (x0 * y0 * exp(x0) + exp(x0)) / y0)
                desmos_equation = 'y= -e^x / (x * e ^ x + C)'
                desmos_C = lambda x0, y0: - (x0 * y0 * exp(x0) + exp(x0)) / y0
            elif form.equation_choice.data == 'eq3':
                f = lambda x, y: x + y
                math_answer = lambda x, x0, y0: exp(x - x0) * (y0 + x0 + 1) - x - 1
                desmos_equation = 'y=C * e^x - x - 1'
                desmos_C = lambda x0, y0: (y0 + x0 + 1) / exp(x0)
            if form.xn.data <= form.x0.data:
                raise ValueError('Некорректный интервал X')
            adams_points = adams(f, form.y0.data, form.x0.data, form.xn.data, form.h.data)
            adam_r = max(abs(math_answer(x, form.x0.data, form.y0.data) - y) for x, y in adams_points)
            try:
                adam_h = adams_find_h_for_eps(f, form.y0.data, form.x0.data, form.xn.data, form.h.data, form.eps.data, math_answer)
                adam_h_success = True
            except ValueError as e:
                adam_h_success = False
                adam_h = None
            eiler_points = eiler(f, form.y0.data, form.x0.data, form.xn.data, form.h.data)
            eiler_r = eiler_points[1][1] - eiler(f, form.y0.data, form.x0.data, form.xn.data, form.h.data / 2)[1][1]
            eiler_h = eiler_find_h_for_eps(f, form.y0.data, form.x0.data, form.xn.data, form.h.data, form.eps.data)
            runge_points = runge_cutt(f, form.y0.data, form.x0.data, form.xn.data, form.h.data)
            runge_r = (runge_points[1][1] - runge_cutt(f, form.y0.data, form.x0.data, form.xn.data, form.h.data / 2)[1][1]) / 15
            runge_h = runge_cutt_find_h_for_eps(f, form.y0.data, form.x0.data, form.xn.data, form.h.data, form.eps.data)
            return render_template('result.html', adams_points=adams_points,
                                   eiler_points=eiler_points, runge_points=runge_points,
                                   eiler_r=eiler_r, runge_r=runge_r, adam_r=adam_r,
                                   adams_x = [point[0] for point in adams_points],
                                   adams_y = [point[1] for point in adams_points],
                                   eiler_x = [point[0] for point in eiler_points],
                                   eiler_y = [point[1] for point in eiler_points],
                                   runge_x = [point[0] for point in runge_points],
                                   runge_y = [point[1] for point in runge_points],
                                   desmos_equation=desmos_equation, desmos_C=desmos_C(form.x0.data, form.y0.data),
                                   desmos_C_min = -50 * abs(desmos_C(form.x0.data, form.y0.data)),
                                   desmos_C_max = 50 * abs(desmos_C(form.x0.data, form.y0.data)),
                                   runge_h=runge_h, eiler_h=eiler_h, eps=form.eps.data,
                                   equation=form.equation_choice.data,
                                   adam_h_success=adam_h_success, adam_h=adam_h, step= form.h.data,)
        except Exception as e:
            return render_template('main.html', form=form, message=f'Ошибка: {e}')
    elif request.method == 'POST':
        print(form.errors)
        return render_template('main.html', form=form, message='Некорректные данные')

    return render_template('main.html', form=form)


if __name__ == '__main__':
    app.run()