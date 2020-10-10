import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import InquiryForm, BlogCreateForm
from .models import Blog

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('my_blog:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name = 'blog_list.html'
    paginate_by = 2

    def get_queryset(self):
        blogs = Blog.objects.filter(
            user=self.request.user).order_by('-created_at')
        return blogs
