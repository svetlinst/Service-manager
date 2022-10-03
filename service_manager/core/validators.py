from django.core.exceptions import ValidationError


def validate_digits_only(value):
    allowed_non_digit_chars = ['+', ' ', ]
    if type(value) == str:
        for c in value:
            if not c.isdigit() and c not in allowed_non_digit_chars:
                raise ValidationError(f'Please, make sure you enter digits only. Invalid character: {c}')
