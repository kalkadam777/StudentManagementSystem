from rest_framework.throttling import UserRateThrottle
from .models import ApiRequest

class CustomUserRateThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        response = super().allow_request(request, view)
        if response:
            # Записываем запрос в базу данных
            ApiRequest.objects.create(
                user=request.user if request.user.is_authenticated else None,
                endpoint=request.path,
                method=request.method,
            )
        return response
