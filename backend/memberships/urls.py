from django.urls import path
from . import views

urlpatterns = [
    path('membership-types/', views.create_membership , name='create'),
    path('membership-types/<int:membership_pk>/', views.delete_membership, name='delete'),
    path('admin/assign-membership/', views.assign_membership, name='assign'),
    path('purchase/', views.purchase_membership, name='purchase'),
    path('my-membership/<int:user_id>/', views.get_my_membership, name='get_mine')
]
