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


class UserSearchTest(generic.base.TemplateView):
    template_name = 'webapp/user_search_test.html'

    def get(self, request, *args, **kwargs):
        return super(UserSearchTest, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserSearchTest, self).get_context_data(**kwargs)

        query = self.request.GET.get('query', '').strip().lower()
        if query:
            results = models.LinkedInConnection.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(position_title__icontains=query) |
                Q(position_company__icontains=query) |
                Q(position_industry__icontains=query)
            )
            context['results'] = results
        return context
