from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)
