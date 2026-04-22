FROM us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:1.1.0

COPY db/tools.yaml /app/tools.yaml

EXPOSE 5000

CMD ["--config", "/app/tools.yaml", "--address", "0.0.0.0", "--port", "5000", "--allowed-hosts", "edgeai-toolbox.railway.internal,localhost,127.0.0.1"]
