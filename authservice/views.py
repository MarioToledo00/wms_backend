

from django.conf import settings
from django.utils import timezone  
import json, random
from django.http import HttpResponse, JsonResponse
from .models import EmailVerified
from users.models import RequestUser, Users
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user': {
                'id': self.user.id,
                'email': self.user.email,
                'name': self.user.name,
            }
        })
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


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

def verify_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['token'].strip()
            email = data['email'].strip()

            try:
                requestUser = RequestUser.objects.get(email=email)
                verified_email = EmailVerified.objects.get(token=token, req_id=requestUser.id)

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

