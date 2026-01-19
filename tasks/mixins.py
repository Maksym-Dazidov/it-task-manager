from django.contrib import messages
from django.db.models.deletion import RestrictedError
from django.shortcuts import redirect

class SafeDeleteMixin:
    success_message = "Deleted successfully."
    error_message = "Cannot delete object because it is in use."

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, self.success_message)
            return response
        except RestrictedError:
            messages.error(request, self.error_message)
            return redirect(self.success_url)