from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


from .models import KeyManager
# Create your views here.


# Create your views here.
@login_required
@require_POST
@csrf_exempt
def create_key(request):
    user = request.user
    key_obj = KeyManager.objects.filter(status=KeyManager.Status.ACTIVE, user=request.user).exists()
    if not key_obj:
        new_key = KeyManager.objects.create(user=user, status=KeyManager.Status.ACTIVE)
        json_key = {
            "id": new_key.id,
            "key": new_key.key,
            "status": new_key.status,
            "procurement_date": new_key.procurement_date,
            "expiry_date": new_key.expiry_date,
        }
        return JsonResponse({"status": "success", "data": json_key})
    return JsonResponse({"status": "error", "message": "An active key already exist"})



class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
    

class MangeKeysListView(OwnerMixin, LoginRequiredMixin, generic.ListView):
    """
    List keys related to the requested user
    """
    model = KeyManager
    context_object_name = "keys" 
    template_name = "account/dashboard.html"


class DetailKeyView(OwnerMixin,LoginRequiredMixin, generic.DetailView):
    """
    Get detailed information on the key with the specified pk/id
    """
    model = KeyManager
    context_object_name = "key"
    template_name = "account/details.html"