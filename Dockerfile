






# Dockerfile — Al-Haqq Protocol TCG Command Hub & Node
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "al_haqq_dashboard.py", "--server.address=0.0.0.0", "--server.headless=true"]
