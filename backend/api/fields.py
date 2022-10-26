from django.shortcuts import get_object_or_404
from rest_framework.serializers import Field
import base64

from users.models import User


class CurrentID:
    requires_context = True

    def __init__(self, model):
        self.model = model

    def __call__(self, serializer_field):
        id = serializer_field.context['request'].parser_context.get(
            'kwargs').get('id')
        return get_object_or_404(self.model, pk=id)

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class Base64ImageField(Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, img_data):
        return base64.b64decode(img_data)
