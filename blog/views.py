from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 8

    def get_queryset(self):
        # только опубликованные
        return Post.objects.filter(is_published=True).order_by("-created_at")


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # инкремент просмотров
        obj.views = (obj.views or 0) + 1
        obj.save(update_fields=["views"])
        # ⭐ доп.: можно отправлять письмо при достижении 100
        # if obj.views == 100: send_mail(...)
        return obj


class PostCreateView(CreateView):
    model = Post
    fields = ["title", "body", "preview", "is_published"]
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse("blog:detail", args=[self.object.pk])


class PostUpdateView(UpdateView):
    model = Post
    fields = ["title", "body", "preview", "is_published"]
    template_name = "blog/post_form.html"

    def get_success_url(self):
        # редирект на отредактированную статью
        return reverse("blog:detail", args=[self.object.pk])


class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:list")
