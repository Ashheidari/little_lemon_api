from rest_framework.permissions import BasePermission



class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.groups.filter(name = 'Managers') and request.user.is_authenticated)
    

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.groups.filter(name = 'Delivery_Crews') and request.user.is_authenticated)