import requests
from django.http import JsonResponse
from .models import Business,Locations
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F

from django.utils import timezone 

class BusinessView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, action=None):
        if action == "getAllBusines":
            return self.getAllBusines(request)
        elif action == "syncBusiness":
            return self.syncBusiness(request)
        elif action == "syncLocations":
            return self.syncLocations(request)
        else:
            return JsonResponse({'error': 'Acción no válida', "action": action}, status=400)
    
    def post(self, request, action=None):  
            return JsonResponse({'error': 'Acción no válida'}, status=400)
    
    def syncBusiness(self,request):
         if request.method == 'GET':

            auth_response = self.authIntegraServices(request)
            if not auth_response.get('success') or not auth_response.get('token'):
                return JsonResponse({
                    'success': False,
                    'message': 'No se pudo autenticar con Integra Services',
                    'error': auth_response.get('error', 'Token inválido o vacío')
                }, status=500)
            
            url = 'http://host.docker.internal:81/integra_services/api/fortia/Business/getBusiness'
            # token = 'tu_token_aquí'

            headers = {
                'Content-Type': 'application/json',
                # 'Authorization': f'Bearer {token}'
            }

            payload = {
                'token': auth_response['token']
            }

            try:
                response = requests.get(
                    url,
                    headers=headers,
                    json=payload,   
                    timeout=120,
                    verify=False  # Desactiva verificación SSL como en tu código original (no recomendado en producción)
                )
                status_code = response.status_code
                if status_code != 200:
                    return JsonResponse({
                        'success': False,
                        'message': response.text,
                        'status_code': status_code
                    }, status=status_code)

                businessData = response.json()
                if businessData['success'] is False:
                    return JsonResponse({
                        'success': False,
                        'message': businessData['message'],
                    }, status=status_code)
            
                for business in businessData['data']:
                    try:
                        Business.objects.update_or_create(
                            business_name_id=business['business_name_id'],  # criterio para buscar
                            defaults={
                                'rfc': business['rfc'],
                                'business_name': business['business_name'],
                                'short_name': business['short_name'],
                                'line_of_business': business['line_of_business'],
                                'phone_number': business['phone_number'],
                                'company_id': business['company_id'],
                                'company_name': business['company_name'],
                                'country': business['country'],
                                'state': business['state'],
                                'municipality': business['municipality'],
                                'city': business['city'],
                            }
                        )
                    except Exception as e:
                        return JsonResponse({
                            'success': False,
                            'message': 'Error al crear el registro',
                            'error': str(e)
                        }, status=500)

                return JsonResponse({
                    'success': True,
                    'message': 'Datos sincronizados correctamente',
                    'total': len(businessData['data'])
                })
            except  Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': 'Error al sincronizar',
                    'error': str(e)
                }, status=500)

    def syncLocations(self,request):
         if request.method == 'GET':

            auth_response = self.authIntegraServices(request)
            if not auth_response.get('success') or not auth_response.get('token'):
                return JsonResponse({
                    'success': False,
                    'message': 'No se pudo autenticar con Integra Services',
                    'error': auth_response.get('error', 'Token inválido o vacío')
                }, status=500)
            
            url = 'http://host.docker.internal:81/integra_services/api/fortia/Business/getLocations'
            

            headers = {
                'Content-Type': 'application/json',
                # 'Authorization': f'Bearer {token}'
            }

            payload = {
                'token': auth_response.get('token')
            }

            try:
                response = requests.get(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=120,
                    verify=False  # Desactiva verificación SSL como en tu código original (no recomendado en producción)
                )
                status_code = response.status_code
                locationsData = response.json()
            
                for location in locationsData['data']:
                    try:
                        Locations.objects.update_or_create(
                            location_id=location['location_id'],  # criterio para buscar
                            defaults={
                                'location_name': location['location_name'],
                                'state_register': location['state_register'],
                                'phone': location['phone'],
                                'address_street': location['address_street'],
                                'address_neighborhood': location['address_neighborhood'],
                                'address_city': location['address_city'],
                                'address_state_name': location['address_state_name'],
                                'address_postal_code': location['address_postal_code'],
                                'representative_rfc': location['representative_rfc'],
                                'representative_curp': location['representative_curp'],
                            }
                        )
                    except Exception as e:
                        return JsonResponse({
                            'success': False,
                            'message': 'Error al crear el registro',
                            'error': str(e)
                        }, status=500)

                return JsonResponse({
                    'success': True,
                    'message': 'Datos sincronizados correctamente',
                    'total': len(locationsData['data'])
                })
            except  Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': 'Error al sincronizar',
                    'error': str(e)
                }, status=500)

    def authIntegraServices(self, request):
        if request.method == 'GET':
            url = 'http://host.docker.internal:81/integra_services/api/auth/Auth/authenticate'
            # token = 'tu_token_aquí'

            headers = {
                'Content-Type': 'application/json',
                # 'Authorization': f'Bearer {token}'
            }

            payload = {
                'username': 'integra_root',
                'password': 'Integr4'
            }

            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=120,
                    verify=False  # Desactiva verificación SSL como en tu código original (no recomendado en producción)
                )
                status_code = response.status_code
                data = response.json()
                
                return {
                    'success': True,
                    'token': data.get('token')
                }
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': 'Error al autenticar',
                    'error': str(e)
                }, status=500)