from django.shortcuts import HttpResponse

        
def export(request):
    if request.method == "GET":
        pass
    
    return HttpResponse("in export")
    
    
