from django.conf.urls import url

from proposals import views

urlpatterns = [
    url(r'^markdown/$', views.markdown_preview, name='markdown'),
    url(r'^$', views.home, name='home'),
    url(r'^conference/$', views.conference, name='conference'),
    url(r'^talk/$', views.talk_list, name='list-talks'),
    url(r'^talk/add/$', views.talk_edit, name='add-talk'),
    url(r'^talk/edit/(?P<talk>[-\w]+)$', views.talk_edit, name='edit-talk'),
    url(r'^talk/vote/(?P<talk>[-\w]+)/(?P<score>[-0-2]+)$', views.vote, name='vote'),
    url(r'^talk/details/(?P<slug>[-\w]+)$', views.TalkDetail.as_view(), name='show-talk'),
    url(r'^talk/by-topic/(?P<topic>[-\w]+)$', views.talk_list_by_topic, name='list-talks-by-topic'),
    url(r'^topic/$', views.TopicList.as_view(), name='list-topics'),
    url(r'^topic/add/$', views.TopicCreate.as_view(), name='add-topic'),
    url(r'^topic/(?P<slug>[-\w]+)/edit/$', views.TopicUpdate.as_view(), name='edit-topic'),
    url(r'^speakers/$', views.SpeakerList.as_view(), name='list-speakers'),
    url(r'^speaker/(?P<username>[\w.@+-]+)$', views.user_details, name='show-speaker'),
]
