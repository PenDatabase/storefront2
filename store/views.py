from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import status
from .filters import ProductFilter
from .pagination import DefaultPagination
from .models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, OrderCreateSerializer, OrderSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer, CustomerSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['unit_price', 'last_update']
    search_fields = ['title', 'description']
    pagination_class = DefaultPagination

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).exists():
            return Response(
                {'error': 'Product cannot be deleted because it still has order items'},
                status=status.HTTP_400_BAD_REQUEST
                )
        return super().destroy(request, *args, **kwargs)



class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count("products")
    ).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).exists():
            return Response(
                {'error': 'Collection cannot be deleted because it still has order items'},
                status=status.HTTP_400_BAD_REQUEST
                )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_pk"]
        return Review.objects.filter(product_id=product_id)
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs["product_pk"]}



class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer



class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        cartitem = CartItem.objects.\
            filter(cart_id=self.kwargs['cart_pk'])\
            .select_related('product')\
            .all()
        return cartitem
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer
    
    def get_serializer_context(self):
        print(self.kwargs['cart_pk'])
        return {'cart_id': self.kwargs['cart_pk']}
    

class CustomerViewSet(CreateModelMixin,
                      RetrieveModelMixin,
                      UpdateModelMixin,
                      GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['GET', 'PUT', 'PATCH'])
    def me(self, request):
        customer, created = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == "PUT":
            serializer = self.get_serializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        elif request.method == "PATCH":
            serializer = self.get_serializer(customer, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        serializer = self.get_serializer(customer)
        return Response(serializer.data)



class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        
        customer_id, created = Customer.objects.only('id').get_or_create(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer #for sanitizing input
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order) # change serializer after saving to return order
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
