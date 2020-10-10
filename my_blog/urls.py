from django.urls import path

from . import views


app_name = 'my_blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry', views.InquiryView.as_view(), name='inquiry'),
    path('blog-list/', views.BlogListView.as_view(), name="blog_list"),
]
