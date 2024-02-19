from django.urls import path,include
from . import views

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('menu-items', views.MenuItemListView.as_view()),
    path('menu-items/category', views.CategoryView.as_view()),
    path('menu-items/<int:pk>', views.MenuItemDetailView.as_view()),
    path('groups/managers/users', views.ManagersAddView.as_view()),
    path('groups/managers/users/<int:pk>', views.ManagersRemoveView.as_view()),
    path('groups/delivery-crew/users', views.DeliverCrewAddView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeliverCrewRemoveView.as_view()),
    path('cart/menu-items', views.CartRequestsView.as_view()), 
    path('menu-items/orders', views.OrderRequestsView.as_view()),
    path('menu-items/orders/<int:pk>', views.SingleOrderView.as_view()),
]