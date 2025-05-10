import json, random
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import RequestUser,Users,EmailVerified
from django.contrib.auth.hashers import make_password

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        return HttpResponse(f"<h1>Hello, {username}! : {password}</h1>")


def logout(request):
    return HttpResponse("<h1>This is page 2</h1>")

def request_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if verifyUserByEmail(data['email']):
                return JsonResponse({
                    'success': False,
                    'message': 'El usuario ya existe'
                }, status=400)

            try:
                existing_req = RequestUser.objects.get(email=data['email'])
                if existing_req.verified is None:
                    existing_req.delete()  # Elimina el registro si `verified` es Null
            except RequestUser.DoesNotExist:
                # Si no existe una solicitud pendiente, seguimos con la creación
                pass

            new_request = RequestUser.objects.create(
                name=data['name'],
                email=data['email'],
                password=make_password(data['password']),
                tel=data['tel']
            )

            try:
                new_verified_email = EmailVerified.objects.create(
                    token=random.randint(100000, 999999), 
                    req_id=new_request.id
                )
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': 'Error al crear el token de verificación',
                    'error': str(e)
                }, status=500)

            return JsonResponse({
                'success': True,
                'message': 'Solicitud creada',
            }, status=201)

        except KeyError as e:
            return JsonResponse({
                'success': False,
                'message': f'Falta el campo: {str(e)}'
            }, status=400)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'JSON inválido'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error al crear la solicitud',
                'error': str(e)
            }, status=500)


def verifyUserByEmail(email):
    try:
        user = Users.objects.get(email=email)
        return True 
    except Users.DoesNotExist:
        return False  
