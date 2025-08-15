# Online Jobs Portal

## Quick start

### Option A — Docker (recommended)

1. Copy `.env.example` → `.env` and edit if needed.
2. From project root:

   ```
   docker-compose up --build
   ```
3. Backend (Django API) available: `http://localhost:8000/api/`
4. Frontend available: `http://localhost:3000/`

---

### Option B — Local without Docker

#### Backend

1. Create & activate virtualenv

   ```
   cd backend
   pip install -r requirements.txt
   export POSTGRES_DB=jobsdb
   (or configure settings to use sqlite for quick test)
   ```
2. If you prefer sqlite quickly: in settings.DB, replace with sqlite3:

   ```py
   DATABASES = {"default": {"ENGINE":"django.db.backends.sqlite3","NAME": BASE_DIR / "db.sqlite3"}}
   ```
3. Run:

   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

#### Frontend

1. `cd frontend`
2. `npm install`
3. `npm start`

---

## Notes, extension ideas and cautions

* **Matching algorithm**: I used `CountVectorizer` + `cosine_similarity`. It’s simple and fast for small datasets. For production, consider:
  * cleaning resume text (remove boilerplate), extract skills with a named entity or skill lists,
  * use TF‑IDF, word embeddings (SentenceTransformers), or a learning-to-rank model,
  * index jobs in Elasticsearch for scale and fuzzy matching.
* **Resume security & privacy**: Store files securely and restrict access. Consider virus scanning for uploads.
* **File parsing**: PyPDF2 and python-docx work for many resumes but not all. For more robust parsing, look into `textract` or commercial resume parsers.
* **Authentication**: SimpleJWT configured. Add refresh token handling in frontend for better UX.
* **Permissions**: Currently any authenticated user may post jobs unless `is_employer` checks are added. In `JobViewSet.perform_create`, you can check `if not self.request.user.is_employer: raise PermissionDenied`.
* **Validation & Tests**: Add DRF serializers validation and frontend form validations.
* **Static files**: For production serve React built static files via nginx and adjust Django settings.
