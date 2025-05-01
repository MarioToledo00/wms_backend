from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Aquí puedes agregar tu lógica de autenticación
        return HttpResponse(f"<h1>Hello, {username}! : {password}</h1>")


def logout(request):
    return HttpResponse("<h1>This is page 2</h1>")

