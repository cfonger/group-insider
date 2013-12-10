import json

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import generic
from linkedin import linkedin
from linkedin.models import AccessToken

from insider.webapp import models


class LinkedInMixin(object):
    def set_up_linkedin(self):
        linkedin_info = settings.LINKEDIN_INFO

        if hasattr(self, 'request'):
            host = self.request.get_host()
        else:
            host = '127.0.0.1:8000'

        return_url = 'http://%s%s' % (
            host,
            reverse('insider-webapp-views-linkedinlogincallback'),
        )

        authentication = linkedin.LinkedInAuthentication(
            linkedin_info['API_KEY'],
            linkedin_info['SECRET_KEY'],
            return_url,
            linkedin.PERMISSIONS.enums.values()
        )

        self.authentication = authentication
        self.application = linkedin.LinkedInApplication(self.authentication)

    def get_shared_profile_fields(self):
        return [
            'id',
            'first-name',
            'last-name',
            'headline',
            'location',
            'distance',
            'num-connections',
            'positions',
            'picture-url',
            'site-standard-profile-request',
            'api-standard-profile-request',
            'public-profile-url',
        ]

    def get_personal_profile_fields(self):
        return (self.get_shared_profile_fields() + [
            'summary',
            'specialties',
            'email-address',
        ])


class HomeView(generic.base.TemplateView, LinkedInMixin):
    template_name = 'webapp/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        if not self.request.user.is_authenticated():
            self.set_up_linkedin()

            context['linkedin_connect_url'] = \
                self.authentication.authorization_url

        return context


class LinkedInLoginCallbackView(generic.base.TemplateView, LinkedInMixin):
    template_name = 'webapp/linkedin_callback.html'

    def pull_and_save_linkedin_data(self):
        userdata = None
        linedin_connections = None

        self.set_up_linkedin()

        self.authentication.authorization_code = self.auth_code
        access_token = self.authentication.get_access_token()

        try:
            linkedin_profile = self.application.get_profile(
                selectors=self.get_personal_profile_fields()
            )
            self.linkedin_profile = linkedin_profile
            
            userdataobjs = models.LinkedInUserData.objects.filter(
                user__username=self.linkedin_profile['id'])
            if not userdataobjs:
                userdata = models.LinkedInUserData()
            else:
                userdata = userdataobjs[0]

            userdata.access_token = access_token.access_token
            userdata.expires_in = access_token.expires_in
            userdata.profile_json = json.dumps(self.linkedin_profile)

            userdata.first_name = self.linkedin_profile.get('firstName', '')
            userdata.last_name = self.linkedin_profile.get('lastName', '')
            userdata.headline = self.linkedin_profile.get('headline', '')
            userdata.picture_url = self.linkedin_profile.get('pictureUrl', '')
            userdata.email = self.linkedin_profile.get('emailAddress', '')
            userdata.location = self.linkedin_profile.get('location', {}).get('name', '')
            
            positions = self.linkedin_profile.get('positions', {}).get('values', [])
            if len(positions) > 0:
                userdata.position_title = positions[0].get('title', '')
                userdata.position_company = positions[0].get('company', {}).get('industry', '')
                userdata.position_industry = positions[0].get('company', {}).get('name', '')

            userdata.public_profile_url = self.linkedin_profile.get('publicProfileUrl', '')

        except Exception as e:
            # Ignore for now, debug later.
            print 'Exception getting the profile'

        if userdata:
            try:
                linedin_connections = self.application.get_connections(
                    selectors=self.get_shared_profile_fields()
                )
                userdata.connections_json = json.dumps(linedin_connections)
            except Exception as e:
                # Ignore for now, debug later.
                print 'Exception getting the connections'

            self.userdata = userdata
            self.userdata.save()

    def login_user(self):
        if self.linkedin_profile:
            email = self.linkedin_profile.get('emailAddress', '')
            linedin_id = self.linkedin_profile['id']

            if hasattr(self, 'userdata'):
                if self.userdata.user:
                    insider_user = self.userdata.user
                else:
                    if User.objects.filter(username=linedin_id).exists():
                        insider_user = User.objects.get(username=linedin_id)
                    else:
                        insider_user = User.objects.create_user(
                            username=linedin_id,
                            email=email,
                            first_name=self.linkedin_profile.get('firstName', ''),
                            last_name=self.linkedin_profile.get('lastName', ''))
                    self.userdata.user = insider_user
                    self.userdata.save()

                insider_user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(self.request, insider_user)

    def get(self, request, *args, **kwargs):
        self.auth_code = self.request.GET.get('code', '')
        if not self.auth_code:
            return redirect(reverse('insider-webapp-views-swkirkland'))

        self.pull_and_save_linkedin_data()

        self.login_user()

        return redirect(reverse('insider-webapp-views-swkirklandgroup'))


class LinkedInUserDataView(generic.base.TemplateView):
    template_name = 'webapp/linkedin_user_data.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        userdataobjs = models.LinkedInUserData.objects.filter(
            user=request.user)
        if not userdataobjs:
            return redirect(reverse('insider-webapp-views-home'))

        self.userdata = userdataobjs[0]
        return super(LinkedInUserDataView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LinkedInUserDataView, self).get_context_data(**kwargs)

        if hasattr(self, 'userdata'):
            context.update({
                'profile': self.userdata.profile_json,
                'connections': self.userdata.connections_json,
            })

        return context


class TestView(generic.base.TemplateView):
    template_name = 'webapp/test.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(TestView, self).get(request, *args, **kwargs)


class SWKirklandView(generic.base.TemplateView, LinkedInMixin):
    template_name = 'webapp/sw.html'
    
    def get_context_data(self, **kwargs):
        context = super(SWKirklandView, self).get_context_data(**kwargs)
        
        if not self.request.user.is_authenticated():
            self.set_up_linkedin()
            
            context['linkedin_connect_url'] = \
                self.authentication.authorization_url
        
        return context


class MemberView(object):
    def __init__(self, member, is_left_column):
        self.member = member
        self.is_left_column = is_left_column


class SWKirklandGroupView(generic.base.TemplateView, LinkedInMixin):
    template_name = 'webapp/swkirklandgroup.html'
    
    def get_context_data(self, **kwargs):
        context = super(SWKirklandGroupView, self).get_context_data(**kwargs)
        
        if not self.request.user.is_authenticated():
            self.set_up_linkedin()
            
            context['linkedin_connect_url'] = \
                self.authentication.authorization_url

        members = models.LinkedInUserData.objects.all()

        member_views = []
        for i, m in enumerate(members):
            v = MemberView(member=m, is_left_column=(i % 2 == 0))
            member_views.append(v)

        context['member_views'] = member_views
        
        return context


class ResultsView(generic.base.TemplateView, LinkedInMixin):
    template_name = 'webapp/results.html'
    
    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        
        if not self.request.user.is_authenticated():
            self.set_up_linkedin()
            
            context['linkedin_connect_url'] = \
                self.authentication.authorization_url

        query = self.request.GET.get('query', '').strip().lower()
        if query:
            member_results = models.LinkedInUserData.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(position_title__icontains=query) |
                Q(position_company__icontains=query) |
                Q(position_industry__icontains=query)
            )
            context['member_results'] = member_results[:50]

            connection_results = models.LinkedInConnection.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(position_title__icontains=query) |
                Q(position_company__icontains=query) |
                Q(position_industry__icontains=query)
            )
            context['connection_results'] = connection_results[:50]
            context['query'] = query
        
        return context

