from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.zhenghou, name='zhenghou'),
    url(r'^rawinfo$', views.RawInfo.as_view(), name="rawinfo"),
    url(r'^wenxian$', views.WenxianCreate.as_view(), name="wenxian"),
    url(r'^wenxian/list$', views.WenxianView.as_view(), name="wx_list"),
]
