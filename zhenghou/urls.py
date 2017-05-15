from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.zhenghou, name='zhenghou'),
    url(r'^rawInput$', views.RawInput.as_view, name="rawinput"),
]
