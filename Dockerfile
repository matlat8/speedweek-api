FROM python:3.12

# Install Rust and Cargo
RUN apt-get update && apt-get install -y curl && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    bash -c "source $HOME/.cargo/env"

ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /api
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "main:app"]