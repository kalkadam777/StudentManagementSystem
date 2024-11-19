from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsStudentOrAdminOrTeacher(permissions.BasePermission):
    """
    Разрешает доступ студенту к своему профилю, а учителям и администраторам — ко всем профилям.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin' or request.user.role == 'teacher':
            return True
        return obj.user == request.user
    
class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Доступ только для учителей или администраторов.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['teacher', 'admin']
    
class CanEnrollStudent(permissions.BasePermission):
    """
    Только учитель или администратор могут записывать студентов на курсы.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['teacher', 'admin']

class IsTeacherOrAdminOrStudentViewOnly(permissions.BasePermission):
    """
    Доступ к оценкам: учителя и администраторы могут добавлять/редактировать, студенты могут только смотреть.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['teacher', 'admin']:
            return True
        return request.user.role == 'student' and obj.student.user == request.user

class IsTeacherOrAdminOrStudentViewAttendance(permissions.BasePermission):
    """
    Доступ к посещаемости: учителя и администраторы могут добавлять, студенты только смотреть.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['teacher', 'admin']:
            return True
        return request.user.role == 'student' and obj.student.user == request.user
