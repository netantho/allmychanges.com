# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework_extensions.fields import ResourceUriField

from allmychanges.models import Repo, RepoVersion, RepoVersionItem, RepoVersionItemChange


class RepoVersionItemChangeSerializer(serializers.ModelSerializer):
    text_clean = serializers.CharField()

    class Meta:
        model = RepoVersionItemChange
        fields = (
            'type',
            'text',
            'text_clean',
        )


class RepoVersionItemSerializer(serializers.ModelSerializer):
    changes = RepoVersionItemChangeSerializer(many=True)
    clean_text = serializers.CharField()

    class Meta:
        model = RepoVersionItem
        fields = (
            'text',
            'clean_text',
            'changes',
        )


class RepoVersionSerializer(serializers.ModelSerializer):
    items = RepoVersionItemSerializer(many=True)

    class Meta:
        model = RepoVersion
        fields = (
            'date',
            'name',
            'items',
        )


class RepoSerializer(serializers.ModelSerializer):
    resource_uri = ResourceUriField(view_name='repo-detail')
    versions = RepoVersionSerializer(many=True)

    class Meta:
        model = Repo
        fields = (
            'id',
            'resource_uri',
            'url',
            'title'
        )


class RepoDetailSerializer(RepoSerializer):
    class Meta(RepoSerializer.Meta):
        fields = RepoSerializer.Meta.fields + (
            'versions',
            'processing_state',
            'processing_status_message',
            'processing_progress',
            'processing_date_started',
            'processing_date_finished',
            'changelog_markup',
        )


class CreateChangelogSerializer(serializers.Serializer):
    url = serializers.URLField()