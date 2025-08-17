from rest_framework import permissions

class IsProfileOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем профиля"""
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsModerator(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()

class IsOwnerOrModerator(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем или модератором"""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.groups.filter(name='moderators').exists()

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()

class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.groups.filter(name='moderators').exists()

class IsNotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name='moderators').exists()