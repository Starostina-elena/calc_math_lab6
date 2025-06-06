from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, NumberRange


class InputForm(FlaskForm):
    equation_choice = RadioField(
        'Выберите ОДУ',
        choices=[('eq1', "y'=2xy/(x^2+1)"), ('eq2', "y'=y+(1+x)y^2"), ('eq3', "y'=x+y")],
        validators=[DataRequired()]
    )
    y0 = FloatField('Начальное значение Y0', validators=[DataRequired()])
    x0 = FloatField('X от', validators=[DataRequired()])
    xn = FloatField('X до', validators=[DataRequired()])
    h = FloatField('Шаг', validators=[DataRequired(), NumberRange(min=0.001, message='Шаг должен быть больше 0')])
    eps = FloatField('Точность', default=0.01, validators=[DataRequired(), NumberRange(min=0.01, message='Точность должна быть больше 0')])

    submit = SubmitField('Вычислить', render_kw={'class': 'btn'})
