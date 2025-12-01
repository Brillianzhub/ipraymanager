# hymns/serializers.py

from rest_framework import serializers
from .models import Hymn, Stanza


class StanzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stanza
        fields = ['stanza_number', 'text']


class HymnSerializer(serializers.ModelSerializer):
    stanzas = StanzaSerializer(many=True, read_only=True)

    class Meta:
        model = Hymn
        fields = ['id', 'title', 'author', 'year',
                  'has_chorus', 'chorus', 'copyright', 'source', 'scripture_references', 'last_updated', 'stanzas']
