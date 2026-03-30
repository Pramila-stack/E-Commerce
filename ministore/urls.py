from django.urls import path

from ministore import views

urlpatterns = [
    path("",views.ProductListView.as_view(),name="product-list"),
    path("product-detail/<int:pk>/",views.ProductDetailView.as_view(),name="product-detail"),
    path("cart/",views.CartView.as_view(),name="cart"),
    path("add-to-cart/<int:pk>/",views.AddToCartView.as_view(),name="add-cart"),
    path("remove-cart/<int:pk>/",views.RemoveFromCartView.as_view(),name="remove-cart"),
    path("checkout/",views.CheckoutView.as_view(),name="checkout"),
    path("success-page/",views.CheckoutSuccessView.as_view(),name="success"),
    path("signup/",views.SignupView.as_view(),name="signup")
]