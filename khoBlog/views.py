from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.views.generic import TemplateView

from .settings.project.version import APP_VERSION_CODE


def offline(request):
    return render(request, "pwa/offline.html")


class ServiceWorkerView(TemplateView):
    template_name = "sw.js"
    content_type = "application/javascript"
    name = "sw.js"

    def get_context_data(self, **kwargs):
        return {
            "version": APP_VERSION_CODE,
            "icon_url": static("khoBlog/img/RuthinkkTooBig-small-square.png"),
            "manifest_url": static("khoBlog/manifest.json"),
            "style_url": static("/css/dist/styles.css"),
            "home_url": reverse("blog:post_list"),
            "offline_url": reverse("offline"),
        }
