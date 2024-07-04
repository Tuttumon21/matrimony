from django import forms

class RangeSliderWidget(forms.Widget):
    template_name = 'widgets/range_slider.html'

    def __init__(self, attrs=None):
        default_attrs = {'min': '0', 'max': '100'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def get_context(self, name, value, attrs):
        if value is None:
            value = ''
        if isinstance(value, str):
            value = value.split(',')
        context = super().get_context(name, value, attrs)
        context['widget']['value_min'] = value[0] if len(value) > 0 else attrs.get('min', '0')
        context['widget']['value_max'] = value[1] if len(value) > 1 else attrs.get('max', '100')
        return context

    def value_from_datadict(self, data, files, name):
        return f"{data.get(f'{name}_min')},{data.get(f'{name}_max')}"
