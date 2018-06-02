from rest_framework import serializers
from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from oauth2_provider.settings import oauth2_settings
from django.http import JsonResponse
from django.contrib.gis.geos import fromstr
from sportsapp.models import Profile
from oauth2_provider.models import AccessToken, Application, RefreshToken
from django.utils.timezone import now, timedelta
from oauthlib.common import generate_token
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis import serializers as geo_serializers
from rest_framework_gis.fields import GeometrySerializerMethodField
from django.http import JsonResponse


class UserSerializer(GeoFeatureModelSerializer):
    #email = serializers.EmailField(source='user.email',required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    #username = serializers.CharField(source='user.username',required=True,validators=[UniqueValidator(queryset=User.objects.all())])

    gender_choices = (('M','Male'),
                        ('F','Female'),
                        ('O','Others')
                        )
    user_gender = serializers.ChoiceField(source='profile.user_gender',choices=gender_choices)
    #dob = serializers.DateField(source='profile.dob')  # date in the format 1995-12-17:yyyy-mm-dd
    #posts = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='post-detail')
    last_location = geo_serializers.GeometryField(source='profile.last_location')
    prefered_radius = serializers.IntegerField(source='profile.prefered_radius',default=5)

    class Meta:
        model = User
        geo_field="last_location"
        id_field = False
        fields = ('id', 'first_name', 'email', 'password','user_gender','prefered_radius')



#By overriding create and update any put or post delete will be in sync with the profile table
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        #self.password = make_password(self.password,salt=None,hasher='default')
        validated_data['password'] = make_password(validated_data['password'],salt=None,hasher='default')
        user = super(UserSerializer, self).create(validated_data)
        #user.password = make_password(user.password,salt=None,hasher='default')
        self.update_or_create_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        self.update_or_create_profile(instance, profile_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def get_last_location(self, instance):
        print(instance)
        return Point(instance.last_location.lat, instance.last_location.lon)

    def update_or_create_profile(self, user, profile_data):
        # This always creates a Profile if the User is missing one;
        # change the logic here if that's not right for your app
        Profile.objects.update_or_create(user=user, defaults=profile_data)

class LoginSerializer(serializers.ModelSerializer):
    def get_token_json(access_token):
        """
        Takes an AccessToken instance as an argument
        and returns a JsonResponse instance from that
        AccessToken
        """
        token = {
            'access_token': access_token.token,
            'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            'token_type': 'Bearer',
            'refresh_token': access_token.refresh_token.token,
            'scope': access_token.scope
        }
        return token

    def get_access_token(user):

        """
        Takes a user instance and return an access_token as a JsonResponse
        instance.
        """

        # our oauth2 app
        app = Application.objects.get(name=user)

        # We delete the old access_token and refresh_token
        try:
            old_access_token = AccessToken.objects.get(
                user=user, application=app)
            old_refresh_token = RefreshToken.objects.get(
                user=user, access_token=old_access_token
            )
        except:
            pass
        else:
            old_access_token.delete()
            old_refresh_token.delete()

        # we generate an access token
        token = generate_token()
        # we generate a refresh token
        refresh_token = generate_token()

        expires = now() + timedelta(seconds=oauth2_settings.
                                    ACCESS_TOKEN_EXPIRE_SECONDS)
        scope = "read write"

        # we create the access token
        access_token = AccessToken.objects.\
            create(user=user,
                   application=app,
                   expires=expires,
                   token=token,
                   scope=scope)

        # we create the refresh token
        RefreshToken.objects.\
            create(user=user,
                   application=app,
                   token=refresh_token,
                   access_token=access_token)

        # we call get_token_json and returns the access token as json
        return LoginSerializer.get_token_json(access_token)

class PasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField()

    def reset_password(request, email, subject_template_name='sportsapp/password_reset_subject.txt',
                   rich_template_name='sportsapp/password_reset_email_rich.html',
                   template_name='sportsapp/password_reset_email.html'):
        """
        Inspired by Django's `PasswordResetForm.save()`. Extracted for reuse.
        Allows password reset emails to be sent to users with unusable passwords
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        user = User.objects.get(email=email)
        print(user)
        if user:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain

            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                #'token': default_token_generator.make_token(user),
                'protocol': 'http',  # Your site can handle its own redirects
            }
            print(c)
            subject = loader.render_to_string(subject_template_name, c)

            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(template_name, c)
            html_email = loader.render_to_string(rich_template_name, c)
            send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_email)
