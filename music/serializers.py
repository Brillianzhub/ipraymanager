from rest_framework import serializers
from .models import Artist, Music


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = [
            "id",
            "name",
            "photo"
        ]


class RelatedArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = [
            "id",
            "name",
            "photo",
            "bio", 
            "facebook",
            "instagram", 
            "youtube_channel", 
            "website" 
        ]

class MusicSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)  
    youtube_id = serializers.ReadOnlyField()
    thumbnail = serializers.ReadOnlyField()

    class Meta:
        model = Music
        fields = [
            "id",
            "title",
            "artist",
            "url",
            "category",
            "views",
            "youtube_id",
            "thumbnail",
            "featured",
            "recommended",
            "date_published",
            "date_added",
        ]


class DetailMusicSerializer(serializers.ModelSerializer):
    artist = RelatedArtistSerializer(read_only=True)  
    youtube_id = serializers.ReadOnlyField()
    thumbnail = serializers.ReadOnlyField()

    class Meta:
        model = Music
        fields = [
            "id",
            "title",
            "artist",
            "url",
            "category",
            "views",
            "youtube_id",
            "thumbnail",
            "featured",
            "recommended",
            "date_published",
            "date_added",
        ]
