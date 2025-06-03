FROM python:3.13.3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Here we execute alembic before starting uvicorn Aquí ejecutamos alembic antes de arrancar uvicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]