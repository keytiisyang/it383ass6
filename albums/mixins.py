from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        if not user.is_authenticated:
            return False
        if getattr(obj, 'can_edit', None):
            return obj.can_edit(user)
        return False

    def handle_no_permission(self):
        return super().handle_no_permission()
