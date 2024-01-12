from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_api_view),
    path('categories/', views.CategoryListAPIView.as_view()),
    path('tags/', views.TagViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('tags/<int:id>/', views.TagViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
    )),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('', views.ProductListCreateAPIView.as_view()),  # GET -> list, POST -> create
    path('<int:id>/', views.product_detail_api_view),  # GET -> item, PUT/PATCH -> update, DELETE -> destroy
]
