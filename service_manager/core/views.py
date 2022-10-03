from django.views import View


class BootstrapViewMixin:
    def get_from(self, **kwargs):
        form = super().get_form(**kwargs)

    @staticmethod
    def __apply_bootstrap_classes(form):
        for (_, field) in form.fields.items():
            if 'attrs' not in field.widget:
                field.widget.attrs = {}
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''

            field.widget.attrs['class'] += ' form-control'
