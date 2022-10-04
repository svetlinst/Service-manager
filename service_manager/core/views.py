class BootstrapFormViewMixin:
    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        self.__apply_bootstrap_classes(form)
        return form

    @staticmethod
    def __apply_bootstrap_classes(form):
        for (_, field) in form.fields.items():
            if not hasattr(field.widget, 'attrs'):
                field.widget.attrs = {}
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''

            field.widget.attrs['class'] += ' form-control'
