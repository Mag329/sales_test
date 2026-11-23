from rest_framework.permissions import BasePermission

class StrictModelPermissions(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        model = view.queryset.model
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        perms = {
            'GET': f'{app_label}.view_{model_name}',
            'POST': f'{app_label}.add_{model_name}',
            'PUT': f'{app_label}.change_{model_name}',
            'PATCH': f'{app_label}.change_{model_name}',
            'DELETE': f'{app_label}.delete_{model_name}',
        }

        required_perm = perms.get(request.method)
        return request.user.has_perm(required_perm)