from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def test_func(self):
        return self.get_object().user == self.request.user
