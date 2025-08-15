from rest_framework import viewsets, generics, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Job, Application
from .serializers import JobSerializer, JobCreateSerializer, ApplicationSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import extract_text_from_pdf, extract_text_from_docx
from django.shortcuts import get_object_or_404

User = get_user_model()

# Registration endpoint
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

# Job ViewSet
from rest_framework import mixins
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by("-created_at")
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action in ["create","update","partial_update","destroy"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action in ["create","update","partial_update"]:
            return JobCreateSerializer
        return JobSerializer

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

    # simple search
    def list(self, request, *args, **kwargs):
        qs = self.queryset
        q = request.query_params.get("q")
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q) | qs.filter(skills__icontains=q)
        return super().list(request, *args, **kwargs)

# Application Upload & Apply
class ApplyView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, job_pk=None, *args, **kwargs):
        job = get_object_or_404(Job, pk=job_pk)
        resume_file = request.FILES.get("resume")
        cover = request.data.get("cover_letter", "")
        app = Application.objects.create(job=job, candidate=request.user, resume=resume_file, cover_letter=cover)
        serializer = ApplicationSerializer(app, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Resume upload and immediate matching endpoint
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.db.models import Value as V
from django.db.models.functions import Concat

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_resume_and_match(request):
    file = request.FILES.get("resume")
    if not file:
        return Response({"detail":"No file provided"}, status=400)

    filename = file.name.lower()
    text = ""
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        try:
            text = file.read().decode("utf-8")
        except Exception:
            text = ""

    # Save a temporary Application object? optional - here we won't persist a job app
    # Build a corpus: resume + each job (title + description + skills)
    jobs = Job.objects.all()
    job_texts = []
    job_ids = []
    for j in jobs:
        doc = " ".join(filter(None, [j.title, j.description, j.skills]))
        job_texts.append(doc)
        job_ids.append(j.id)

    corpus = [text] + job_texts
    if len(corpus) <= 1:
        return Response({"matches":[]})

    vect = CountVectorizer(stop_words="english").fit_transform(corpus)
    cos_sim = cosine_similarity(vect[0:1], vect[1:]).flatten()  # resume vs each job
    # get top matches
    top_idx = np.argsort(-cos_sim)[:10]
    matches = []
    for idx in top_idx:
        score = float(cos_sim[idx])
        matches.append({
            "job_id": job_ids[idx],
            "score": score,
            "title": jobs[idx].title,
            "description": jobs[idx].description[:240],
            "skills": jobs[idx].skills
        })
    return Response({"matches": matches})

# Simple endpoint to compute match score for a given job id and resume text (optional)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def score_against_job(request, job_pk):
    resume_text = request.data.get("resume_text", "")
    job = get_object_or_404(Job, pk=job_pk)
    docs = [resume_text, " ".join([job.title, job.description, job.skills])]
    vect = CountVectorizer(stop_words="english").fit_transform(docs)
    score = float(cosine_similarity(vect[0:1], vect[1:2]).flatten()[0])
    return Response({"score": score})
