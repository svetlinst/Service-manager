from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def numbers_only_validator(value):
    if not all([x.isdigit() for x in str(value)]):
        raise ValidationError(_('Please, enter digits only.'), code='invalid')


def phone_number_validator(value):
    allowed_chars = ['+', ' ']
    for c in str(value):
        if not c.isdigit() and c not in allowed_chars:
            raise ValidationError(_('The allowed characters are: +, space and digits.'), code='invalid')
