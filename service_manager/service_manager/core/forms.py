from django.forms import Textarea, Select


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_fields()

    def _init_bootstrap_fields(self):
        for (_, field) in self.fields.items():

            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''

            if isinstance(field.widget, Select):
                field.widget.attrs['class'] += ' form-select'
            else:
                field.widget.attrs['class'] += ' form-control'
