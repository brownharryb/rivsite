from django.urls import path
from. import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.ApplicationFormView.as_view()),
    path('apply/',views.ApplicationFormView.as_view(), name="apply_page"),
    path('new/',views.ApplicationFormView.as_view(), name="apply_new_page"),
    path('logout/',views.logout_user, name="logout_page"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
