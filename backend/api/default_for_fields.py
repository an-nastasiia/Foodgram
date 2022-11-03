from django.shortcuts import get_object_or_404


class CurrentID:
    '''Получение id для присвоения дефолтного значения в поле сериализатора.'''

    requires_context = True

    def __init__(self, model):
        self.model = model

    def __call__(self, serializer_field):
        id = serializer_field.context['request'].parser_context.get(
            'kwargs').get('id')
        return get_object_or_404(self.model, pk=id)

    def __repr__(self):
        return f'{self.__class__.__name__}'
