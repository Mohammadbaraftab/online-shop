from django.urls import path, include
from . import views


bucket_urls = [
    path("", views.BucketView.as_view(), name="bucket"),
    path("delete_object/<str:key>/", views.DeleteBucketObjectView.as_view(), name="delete_bucket_object"),
    path("download_object/<str:key>/", views.DownloadBucketObjectView.as_view(), name="download_bucket_object"),
  
]

app_name = "home"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("category/<slug:slug>", views.HomeView.as_view(), name="category_filter"),
    path("bucket/", include(bucket_urls)),
   
]
