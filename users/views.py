from django.http import JsonResponse
from .models import RequestUser,Users,Roles
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from django.utils import timezone  

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, action=None):
        if action == "getRequests":
            return self.all_request_user(request)
        elif action == "getRoles":
            return self.getRoles(request)
        elif action == "getAllUsers":
            return self.getAllUsers(request)
        else:
            return JsonResponse({'error': 'Acción no válida', "action": action}, status=400)
    
    def post(self, request, action=None):  
        if action == "create_user":
            return self.create_user(request)
        elif action == "create_user_by_post":
            return self.create_user_by_post(request)
        else:
            return JsonResponse({'error': 'Acción no válida'}, status=400)

    def all_request_user(serlf,request):
        if request.method == 'GET':
            request_users = RequestUser.objects.filter(verified__isnull=False,accepted__isnull=True,denied__isnull=True).values('id', 'name', 'email','tel')
            return JsonResponse(list(request_users), safe=False)
    
    def create_user(self,request):
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



    def create_user_by_post(serlf,request): 
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

    def getRoles(self,request):
        if request.method == 'GET':
            roles = Roles.objects.all().values('id', 'name')
            return JsonResponse(list(roles), safe=False)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    def getAllUsers(self,request):
        if request.method == 'GET':
            users = Users.objects.all().values('id', 'name', 'email','tel','rol')
            return JsonResponse(list(users), safe=False)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)