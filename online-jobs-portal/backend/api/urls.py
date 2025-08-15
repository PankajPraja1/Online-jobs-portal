from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, RegisterView, ApplyView, upload_resume_and_match, score_against_job
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("jobs", JobViewSet, basename="jobs")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jobs/<int:job_pk>/apply/", ApplyView.as_view(), name="apply"),
    path("resume/match/", upload_resume_and_match, name="resume_match"),
    path("jobs/<int:job_pk>/score/", score_against_job, name="score_job"),
]
