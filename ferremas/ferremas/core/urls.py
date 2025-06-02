from django.urls import path, include
from .views import agregar_al_carrito, index, login_view, carrito_view, ProductoViewSet, calcular_descuento, valor_dolar, simular_pago, registro_view
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', index),
    path('login/', login_view),
    path('carrito/', carrito_view, name='carrito'),  # <--- aquí
    path('api/', include(router.urls)),
    path('api/descuento/', calcular_descuento),
    path('api/dolar/', valor_dolar),
    path('api/webpay/', simular_pago),
    path('registro/', registro_view),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_carrito'),
]

