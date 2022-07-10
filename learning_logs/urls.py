# 用于自定义url

from django.urls import path, re_path
from . import views

app_name = 'Learning_logs'
urlpatterns = [
    # 主页
    path('',views.index,name='index'),
    # 显示所有的主题
    path('topics/',views.topics,name='Topics'),
    # 特定主题的详细页面
    re_path(r'^topics/(?P<topic_id>\d+)/$',views.topic,name='topic'),
    # 用于添加新的主题
    path('new_topic/',views.new_topic,name='new_topic'),
    # 用于添加新的条目
    re_path(r'^new_entry/(?P<topic_id>\d+)/$',views.new_entry,name="new_entry"),
    # 用于编辑条目
    re_path(r'^edit_entry/(?P<entry_id>\d+)/$',views.edit_entry,name='edit_entry'),
]