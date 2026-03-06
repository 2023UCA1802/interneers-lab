from django.http import JsonResponse
from shared.application.greet_usecase import Greet_Usecase
from shared.adapter.greeting_service import GreetingService
from shared.domain.greeting import InvalidAgeError
from .forms import GreetForm

greeting_service=GreetingService()
usecase=Greet_Usecase(greeting_service)

def greet(request):
    params=request.GET
    # form=GreetForm(params)
        # if not form.is_valid():
        #     return JsonResponse(form.errors,status=400)
    name=params.get("name")
    age=params.get("age")
    try:
        if age is not None:
            age=int(age)
        message=usecase.execute(name,age)
        return JsonResponse({"message":message})
    except InvalidAgeError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=422)
    