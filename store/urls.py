from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from . import views
from pprint import pprint

router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet)
router.register("carts", views.CartViewSet)
router.register("customers", viewset=views.CustomerViewSet)
router.register("orders", views.OrderViewSet, basename="orders")

product_router = NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

cart_router = NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register("items", views.CartItemViewSet, basename='cart-items-detail')

# URLConf
urlpatterns = router.urls + product_router.urls + cart_router.urls