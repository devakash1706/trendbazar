from django.urls import path
from store import views

urlpatterns=[
    path('register/',views.SignUpView.as_view(),name="signup"),
    path('',views.SignInView.as_view(),name='signin'),
    path('home/',views.HomeView.as_view(),name='home'),
    path('products/<int:pk>/',views.ProductDetailView.as_view(),name='product-detail'),
    path('products/<int:pk>/cart/add/',views.AddToCartView.as_view(),name='add-to-cart'),
    path('cart/all/',views.CartItemListView.as_view(),name="cart-list"),
    path('basket/item/<int:pk>/remove',views.BasketItemDeleteView.as_view(),name='basket-remove'),
    path('basket/item/<int:pk>/quantity/change/',views.BasketItemUpdateView.as_view(),name='basket-item-qty-update'),
    path('checkout/',views.CheckoutView.as_view(),name='checkout'),
    path('orders/all/', views.MyOrdersView.as_view(),name='orders'),
    # path('verify/',views.PaymentVerificationView.as_view(),name='verification')
]