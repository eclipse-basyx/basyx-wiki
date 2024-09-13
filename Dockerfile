FROM objectivepartner.azurecr.io/basyx-enterprise/infra/docker-nginx-single-page-app

ENTRYPOINT ["/bin/sh", "-c", "exec nginx"]

COPY docs/build/ /app

ENV HEALTH_ENDPOINT=http://localhost:80/

HEALTHCHECK --start-period=5s --timeout=10s --interval=10s --retries=10 \
        CMD curl -s -o /dev/null -w "%{http_code}" -k $HEALTH_ENDPOINT
