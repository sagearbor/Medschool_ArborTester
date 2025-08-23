FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

# Create the startup script BEFORE CMD
RUN echo '#!/bin/bash' > start.sh && \
    echo 'python -m alembic upgrade head' >> start.sh && \
    echo 'python -m uvicorn backend.main:app --host 0.0.0.0 --port 10000' >> start.sh && \
    chmod +x start.sh

EXPOSE 10000

CMD ["./start.sh"]
