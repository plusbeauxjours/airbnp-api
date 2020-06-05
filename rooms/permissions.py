from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_objecxt_permission(self, request, view, room):
        return room.user == request.user
