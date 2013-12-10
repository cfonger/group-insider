from django.contrib.auth.models import User
from django.db import models


class TestModel(models.Model):
    somefield = models.BooleanField()


class LinkedInUserData(models.Model):
    # The user that this LinkedIn data is for.
    user = models.ForeignKey(User, null=True, blank=True)

    # OAuth info.
    access_token = models.CharField(max_length=300, blank=True, null=True)
    expires_in = models.IntegerField(blank=True, null=True)

    # LinkedIn parsed data.
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    headline = models.CharField(max_length=200, blank=True, null=True)
    picture_url = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    position_title = models.CharField(max_length=200, blank=True, null=True)
    position_company = models.CharField(max_length=200, blank=True, null=True)
    position_industry = models.CharField(max_length=200, blank=True, null=True)
    public_profile_url = models.CharField(max_length=300, blank=True, null=True)

    # Raw JSON data.
    profile_json = models.TextField(blank=True, null=True)
    connections_json = models.TextField(blank=True, null=True)

    def __unicode__(self):
        if self.user:
            return '%s %s' % (self.user.first_name, self.user.last_name)
        return 'LinkedInUserData object'


class LinkedInConnection(models.Model):
    # The user for which this connection is a 1st level connection.
    connected_with = models.ForeignKey(LinkedInUserData, null=True, blank=True)
    
    # LinkedIn parsed data.
    user_id = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    headline = models.CharField(max_length=200, blank=True, null=True)
    picture_url = models.CharField(max_length=300, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    position_title = models.CharField(max_length=200, blank=True, null=True)
    position_company = models.CharField(max_length=200, blank=True, null=True)
    position_industry = models.CharField(max_length=200, blank=True, null=True)
    public_profile_url = models.CharField(max_length=300, blank=True, null=True)

    # Raw JSON data.
    full_connection_json = models.TextField(blank=True, null=True)

    def __unicode__(self):
        if self.first_name:
            return '%s %s' % (self.first_name, self.last_name)
        return 'LinkedInConnection object'
