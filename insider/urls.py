from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

import insider.webapp.views.home as home_views
import insider.webapp.views.user_search as user_search_views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home_views.HomeView.as_view(), name='insider-webapp-views-home'),
    url(r'^linkedin-callback/$', home_views.LinkedInLoginCallbackView.as_view(), name='insider-webapp-views-linkedinlogincallback'),
    url(r'^linkedin-user-data/$', home_views.LinkedInUserDataView.as_view(), name='insider-webapp-views-linkedinuserdata'),

    # Test URLs.
    url(r'^test/$', home_views.TestView.as_view(), name='insider-webapp-views-test'),

    # Event URLs.
    url(r'^swkirkland/$', home_views.SWKirklandView.as_view(), name='insider-webapp-views-swkirkland'),
       
    # Result URLs.
    url(r'^results/$', home_views.ResultsView.as_view(), name='insider-webapp-views-results'),

    url(r'^user-search-test/$', user_search_views.UserSearchTest.as_view(), name='insider-webapp-views-usersearchtest'),

    # Groups URLs.
    url(r'^swkirklandgroup/$', home_views.SWKirklandGroupView.as_view(), name='insider-webapp-views-swkirklandgroup'),
                       
    # Admin URLs.
    url(r'^admin/', include(admin.site.urls)),

    # Other auth URLs.
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', kwargs={'next_page': '/swkirkland/'}, name="insider-webapp-views-logout"),
)
