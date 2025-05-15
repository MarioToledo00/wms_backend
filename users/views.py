from django.http import JsonResponse
from django.shortcuts import render
from .models import RequestUser,Users,Roles
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.utils import timezone  


def all_request_user(request):
    if request.method == 'GET':
        request_users = RequestUser.objects.filter(verified__isnull=False,accepted__isnull=True,denied__isnull=True).values('id', 'name', 'email','tel')
        return JsonResponse(list(request_users), safe=False)
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = request.POST
        request_id = data.get('request_id')
        rol_id = data.get('rol_id')

        try:

            request = RequestUser.objects.get(id=request_id)
            
            try:
                user = Users.objects.create(
                    name=request.name,
                    email=request.email,
                    password=request.password,
                    tel=request.tel,
                    rol_id=rol_id,

                )
                user.save()
                request.accepted = timezone.now()
                request.save()

                return JsonResponse({'success':True,'message': 'User created successfully'}, status=201)
            except Exception as e:
                return JsonResponse({'error': 'Error creating user', 'details': str(e)}, status=500)
        except RequestUser.DoesNotExist:
            return JsonResponse({'error': 'Request user not found'}, status=404)
        
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



def create_user_by_post(request): 
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    # if request.method == 'POST':
    #     data = request.POST
    #     name = data.get('name')
    #     email = data.get('email')
    #     password = data.get('password')
    #     tel = data.get('tel')

    #     user = create_user(name, email, password, tel)
    #     return JsonResponse({'message': 'User created successfully', 'user_id': user.id}, status=201)
    # else:
    #     return JsonResponse({'error': 'Invalid request method'}, status=400)

def getRoles(request):
    if request.method == 'GET':
        roles = Roles.objects.all().values('id', 'name')
        return JsonResponse(list(roles), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)