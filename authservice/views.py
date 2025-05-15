from datetime import datetime, timedelta
import jwt
import datetime
from django.conf import settings
from django.utils import timezone  
import json, random
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import EmailVerified
from users.models import RequestUser, Users
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password

from django.utils.timezone import is_naive, make_aware

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = Users.objects.get(email=data['email'])

        except Users.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=400)

        if not check_password(data['password'], user.password):
            return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=400)

        # Generar token
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        return JsonResponse({
            'success': True,
            'message': 'Login successful',
            'user': {
                'email': user.email,
                'name': user.name,
                'access_token': token
            }
        }, status=200)

def logout(request):
    return HttpResponse("<h1>This is page 2</h1>")
@csrf_exempt
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
                    try:
                        verified_email = EmailVerified.objects.get(req_id=existing_req.id)
                        verified_email.delete()  # Elimina el token de verificación anterior
                    except EmailVerified.DoesNotExist:
                        pass
                    existing_req.delete()  # Elimina el registro si `verified` es Null
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Ya existe una solicitud pendiente con este correo electrónico'
                    }, status=400)
            except RequestUser.DoesNotExist:
                # Si no existe una solicitud pendiente, seguimos con la creación
                pass

            new_request = RequestUser.objects.create(
                name=data['name'],
                email=data['email'],
                password=make_password(data['password']),
                tel=data['tel']
            )
            
            token = random.randint(100000, 999999)

            try:
                new_verified_email = EmailVerified.objects.create(
                    token= token,
                    req_id=new_request.id,
                )
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': 'Error al crear el token de verificación',
                    'error': str(e)
                }, status=500)

            send_confirmation_email(data['email'], token)

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



@csrf_exempt
def verify_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['token'].strip()
            email = data['email'].strip()

            try:
                requestUser = RequestUser.objects.get(email=email)
                verified_email = EmailVerified.objects.get(token=token, req_id=requestUser.id)

# Fechas en formato datetime con zona horaria
                fecha_creacion = verified_email.created_at.strftime('%Y-%m-%d %H:%M:%S')
                fecha_actual = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

                # Verificar si el token ha expirado
                if fecha_creacion.split(' ')[0] != fecha_actual.split(' ')[0]:
                    return JsonResponse({
                        'success': False,
                        'message': 'Token expirado',
                        'fecha_creacion': fecha_creacion.split(' ')[0],
                        'fecha_actual': fecha_actual.split(' ')[0]
                    }, status=400)


                hora_creacion = int(fecha_creacion.split(' ')[1].split(':')[0])
                minuto_creacion = int(fecha_creacion.split(' ')[1].split(':')[1])

                hora_actual = int(fecha_actual.split(' ')[1].split(':')[0])
                minuto_actual = int(fecha_actual.split(' ')[1].split(':')[1])

                
                # Verificar la diferencia de horas
                diferencia = hora_actual - hora_creacion
                if diferencia > 1:
                    return JsonResponse({
                        'success': False,
                        'message': 'Token expirado'
                    }, status=400)
                
                if diferencia == 1:
                    if minuto_actual > minuto_creacion:
                        return JsonResponse({
                            'success': False,
                            'message': 'Token expirado'
                        }, status=400)
                    
                

                # Eliminar el token verificado
                verified_email.delete()

                requestUser.verified = timezone.now()
                requestUser.updated_at = timezone.now()

            
                requestUser.save()

                return JsonResponse({
                    'success': True,
                    'message': 'Correo verificado correctamente, espere respuesta del administrador',
                }, status=200)

            except EmailVerified.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Token inválido'
                }, status=400)

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
                'message': 'Error al verificar el correo',
                'error': str(e)
            }, status=500)
     

def send_confirmation_email(user_email, token):
    subject = 'Confirma tu correo electrónico'
    from_email = 'integra@alerta.com.mx'
    recipient_list = [user_email]

    
    # Texto plano (versión simplificada del HTML)
    text_content = (
        "Bienvenido a WMS (Warehouse Management System).\n\n"
        "Hemos detectado una solicitud de usuario asociada a esta dirección de correo.\n"
        "Si no reconoce esta solicitud, puede ignorar este mensaje.\n\n"
        f"Su código de confirmación es: {token}\n\n"
        "Gracias por elegir WMS. Estamos aquí para ayudarle a gestionar su almacén de manera eficiente.\n\n"
        "Atentamente,\n"
        "El equipo de Integra\n\n"
        "Este es un correo automático, por favor no responda.\n"
        "Contacto: integra@alerta.com.mx | Teléfono: +52 (669) 915-6010\n"
        "Sitio web: https://integra.alerta.com.mx/wms"
    )

    # Cuerpo en HTML (con estilos)
    html_content = render_to_string('confirmation_email.html', {'token': token})

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@csrf_exempt 
def create_user_by_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data['name']
            email = data['email']
            password = data['pass']
            tel = data['tel']

            if verifyUserByEmail(email):
                return JsonResponse({
                    'success': False,
                    'message': 'El usuario ya existe'
                }, status=400)

            user = Users.objects.create(
                name=name,
                email=email,
                password=make_password(password),
                tel=tel,
                rol_id=1,
                activated_by=1,
            )

            return JsonResponse({
                'success': True,
                'message': 'Usuario creado correctamente',
                'user_id': user.id
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
                'message': 'Error al crear el usuario',
                'error': str(e)
            }, status=500)

@csrf_exempt
def check_Auth(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['token']
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload['user_id']
            user = Users.objects.get(id=user_id)

            return JsonResponse({
                'success': True,
                'message': 'Token válido',
                'user': {
                    'email': user.email,
                    'name': user.name
                }
            }, status=200)

        except jwt.ExpiredSignatureError:
            return JsonResponse({
                'success': False,
                'message': 'Token expirado'
            }, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({
                'success': False,
                'message': 'Token inválido'
            }, status=401)
        except Users.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Usuario no encontrado'
            }, status=404)
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
                'message': 'Error al verificar el token',
                'error': str(e)
            }, status=500)  