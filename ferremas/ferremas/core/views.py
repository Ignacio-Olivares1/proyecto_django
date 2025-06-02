from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework import viewsets
import requests
from django.contrib.auth.models import User
from django.contrib import messages

def index(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')

def carrito_view(request):
    carrito = request.session.get('carrito', {})

    productos_carrito = []
    total = 0

    for producto_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=producto_id)
            subtotal = producto.precio * cantidad
            total += subtotal
            productos_carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        except Producto.DoesNotExist:
            pass

    return render(request, 'carrito.html', {
        'productos_carrito': productos_carrito,
        'total': total
    })

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

@api_view(['GET'])
def calcular_descuento(request):
    precio = float(request.GET.get('precio', 100))
    descuento = precio * 0.1
    return Response({'precio': precio, 'descuento': descuento})

@api_view(['GET'])
def valor_dolar(request):
    r = requests.get("https://mindicador.cl/api/dolar")
    valor = r.json()['serie'][0]['valor']
    return Response({'USD_to_CLP': valor})

@api_view(['POST'])
def simular_pago(request):
    return Response({'status': 'success', 'message': 'Pago procesado con Webpay (simulado)'})

def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Usuario creado con éxito. Inicia sesión.')
            return redirect('/login/')
    
    return render(request, 'registro.html')

def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        carrito = request.session.get('carrito', {})

        carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1

        request.session['carrito'] = carrito
        messages.success(request, f'Has agregado "{producto.nombre}" al carrito.')
        return redirect('/')
    else:
        return redirect('/')

from django.shortcuts import render

def carrito_simulado_view(request):
    # Productos simulados (hardcodeados)
    productos_carrito = [
        {
            'producto': {
                'nombre': 'Taladro Eléctrico',
                'precio': 50000,
                'imagen_url': '/static/img/taladro.webp'
            },
            'cantidad': 2,
            'subtotal': 100000
        },
        {
            'producto': {
                'nombre': 'Esmeril Angular',
                'precio': 75000,
                'imagen_url': '/static/img/esmeril angular.png'
            },
            'cantidad': 1,
            'subtotal': 75000
        }
    ]

    total = sum(item['subtotal'] for item in productos_carrito)

    return render(request, 'carrito.html', {
        'productos_carrito': productos_carrito,
        'total': total
    })
