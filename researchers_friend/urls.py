from django.conf.urls import patterns, include, url
from researcher.admin import ADMIN_SITE

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'researchers_friend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(ADMIN_SITE.urls)),
)
