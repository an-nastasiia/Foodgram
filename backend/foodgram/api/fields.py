from django.shortcuts import get_object_or_404

from users.models import User


class CurrentAuthor:
    requires_context = True

    def __call__(self, serializer_field):
        author_id = serializer_field.context['request'].parser_context.get(
            'kwargs').get('author_id')
        return get_object_or_404(User, pk=author_id)

    def __repr__(self):
        return '%s()' % self.__class__.__name__
