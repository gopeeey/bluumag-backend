from rest_framework import serializers
from .models import MyUser


class MyUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True
    )
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = MyUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'is_writer',
            'is_store_keeper',
            'phone',
            'address',
            'birthdate')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'is_writer',
            'is_store_keeper',
            'phone',
            'address',
            'birthdate'
        ]
