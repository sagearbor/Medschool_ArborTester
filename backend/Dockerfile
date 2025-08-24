FROM python:3.11

WORKDIR /app

# Copy requirements first for better layer caching
COPY ./backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy everything from backend directory
COPY ./backend /app/backend/

# Copy the root alembic.ini to the working directory
COPY ./alembic.ini /app/alembic.ini

# Set Python path to include the app directory 
ENV PYTHONPATH=/app

# Create the startup script
RUN echo '#!/bin/bash' > start.sh && \
    echo 'cd /app' >> start.sh && \
    echo 'python -m alembic upgrade head' >> start.sh && \
    echo 'python -m uvicorn backend.main:app --host 0.0.0.0 --port 10000' >> start.sh && \
    chmod +x start.sh

EXPOSE 10000

CMD ["./start.sh"]
