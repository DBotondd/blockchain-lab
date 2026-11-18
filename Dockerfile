# Multi-stage container: Node.js (Ganache + solc-js) and Python (Streamlit + Web3.py).
FROM node:22-bookworm-slim AS node_runtime

FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    NODE_ENV=production \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=node_runtime /usr/local/bin/node /usr/local/bin/node
COPY --from=node_runtime /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

WORKDIR /app
COPY requirements-online.txt ./
RUN python -m pip install --no-cache-dir -r requirements-online.txt

COPY package.json ./
RUN npm install --omit=dev --no-audit --no-fund

COPY . .
# Compiling at image-build time saves RAM and avoids download during user clicks.
RUN node compile_for_cloud.js \
    && python -m unittest -q test_blockchain test_reszletes

RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 10000
CMD ["sh", "-c", "exec python -m streamlit run app.py --server.address 0.0.0.0 --server.port ${PORT:-10000} --server.headless true --server.fileWatcherType none --browser.gatherUsageStats false"]
