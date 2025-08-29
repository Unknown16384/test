from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import UserProfile, Skills, SkillList, Desks

User = get_user_model()

class DeskAdjunct(serializers.ModelSerializer):

    class Meta:
        model = Desks
        fields = ('number',)

class SkillsAdjunct(serializers.ModelSerializer):
    skill = serializers.SlugRelatedField(slug_field='skill', queryset=SkillList.objects.all())

    class Meta:
        model = Skills
        fields = ('skill', 'level')

class UserAdjunct(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileAdjunct(serializers.ModelSerializer):
    skills = SkillsAdjunct(many=True, read_only=True)
    desk = serializers.IntegerField(source='desk.number', read_only=True)

    class Meta:
        model = UserProfile
        exclude = ('user',)

class UserListSerializer(serializers.ModelSerializer):
    skills = SkillsAdjunct(many=True)
    desk = serializers.SlugRelatedField(slug_field='number', queryset=Desks.objects.all())

    class Meta:
        model = UserProfile
        fields = ('id', 'family', 'name', 'skills', 'diff_date', 'desk')

class UserDetailSerializer(serializers.ModelSerializer):
    skills = SkillsAdjunct(many=True)
    desk = serializers.SlugRelatedField(slug_field='number', queryset=Desks.objects.all())

    class Meta:
        model = UserProfile
        fields = ('family', 'name', 'surname', 'gender', 'tester', 'skills', 'diff_date', 'desk', 'gallery', 'description')

class UserDeskSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Desks
        fields = ('user', 'number')

    def get_user(self, obj):
        return f'{obj.user}'

class AdminListSerializer(serializers.ModelSerializer):
    profile = UserProfileAdjunct()

    class Meta:
        model = User
        fields = ('username', 'password', 'profile')

    def create(self, validated_data):
        user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
            )
        UserProfile.objects.create(user_id=user.id, **validated_data['profile'])
        return user

class AdminDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserAdjunct(required=False)
    desk = DeskAdjunct(required=False)
    skills = SkillsAdjunct(many=True, required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        desk_data = validated_data.pop('desk', None)
        skills_data = validated_data.pop('skills', [])
        user = super().update(instance, validated_data)
        if user_data:
            user_instance = User.objects.get(profile=user)
            user_serializer = UserAdjunct(user_instance, data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)
        if desk_data:
            desk_instance = Desks.objects.get(user=user)
            desk_serializer = DeskAdjunct(desk_instance, data=desk_data)
            if desk_serializer.is_valid():
                desk_serializer.save()
            else:
                raise serializers.ValidationError(desk_serializer.errors)
        for skill in skills_data:
            skills_instance, created = Skills.objects.get_or_create(user=user, skill=skill['skill'], defaults={'level': 1})
            skills_serializer = SkillsAdjunct(skills_instance, data=skill)
            if skills_serializer.is_valid():
                skills_serializer.save()
            else:
                raise serializers.ValidationError(skills_serializer.errors)
        return instance
