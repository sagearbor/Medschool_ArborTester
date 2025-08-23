# Use a standard Python runtime that includes a full shell
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the dependency file
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application's code
COPY . /app

# Expose port 8000 to the outside world
EXPOSE 10000

# Command to run the application using uvicorn
# --host 0.0.0.0 makes the server accessible from outside the container
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]

# Create a simple startup script
RUN echo '#!/bin/bash\npython -m alembic upgrade head\npython -m uvicorn backend.main:app --host 0.0.0.0 --port 10000' > start.sh && chmod +x start.sh

CMD ["./start.sh"]
