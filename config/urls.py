from django.urls                import path, include

from addresses                  import views

urlpatterns = [

    path('login/', views.login),
    path('addresses/', views.address_list),
    path('addresses/<int:pk>', views.address_detail),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]