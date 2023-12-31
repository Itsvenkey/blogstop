from django.urls import path
from . import views
urlpatterns =[
    path('',views.home,name=''),
    path('login/',views.login,name='login'),
    path('register/',views.register,name = 'register'),
    path('blog_detail/<pk>/',views.blog_detail,name='blog_detail'),
    path('blog_category/<category>/',views.blog_category,name='blog_category'),
    path('blog_index/',views.blog_index,name='blog_index'),
    path('logout/',views.logout,name='logout'),
    path('add-blog/',views.add_blog,name='add-blog'),
]
