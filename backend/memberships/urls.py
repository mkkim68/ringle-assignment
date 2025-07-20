from django.urls import path
from . import views

urlpatterns = [
    path('membership-types/create/', views.create_membership , name='create'),
    path('membership-types/<int:membership_pk>/', views.delete_membership, name='delete'),
    path('admin/assign-membership/', views.assign_membership, name='assign'),
    path('purchase/', views.purchase_membership, name='purchase'),
    path('my-membership/', views.get_my_membership, name='get_mine'),
    path('login/', views.CustomLoginView.as_view(), name='login')
]
