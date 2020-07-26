FROM g1g1/py-poetry

WORKDIR /dominion

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
# Copy in everything else:
COPY . ./
RUN poetry install

EXPOSE 50051
CMD PYTHONPATH=$PWD poetry run python grpc_networking/server/main.py