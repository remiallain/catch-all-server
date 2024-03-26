# Catch-all Server

This is a catch-all server that could be used to return a custom response for any request.

## Example

```yaml
services:
  not-found:
    image: ghcr.io/remiallain/catch-all-server:latest
    environment:
      SERVER_NAME: "Not Found"
      STATUS_CODE: 404
      PORT: 8000
      TYPE: text/html
      CONTENT: >
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Not Found</title>
        </head>
        <body>
            <h1>Not Found</h1>
        </body>
        </html>
    ports:
      - "8000:8000"
```

You can serve a JSON instead of HTML

```yaml
TYPE: application/json
CONTENT: '{"error": "not-found"}'
```

## Use with Traefik redirect

This server can be used with Traefik to redirect to a custom 404 page when there is no route to a service (wildcard routing).

```yaml
services:
    not-found:
        image: ghcr.io/remiallain/catch-all-server:latest
        environment:
            CONTENT: "<h1>Oops, this service does not exist</h1>"
        labels:
            # Middleware redirect to not-found.$DOMAIN
            - "traefik.http.middlewares.catch-all-redirectregex.redirectregex.regex=.*"
            - "traefik.http.middlewares.catch-all-redirectregex.redirectregex.replacement=http://not-found.${DOMAIN}"
            - "traefik.http.middlewares.catch-all-redirectregex.redirectregex.permanent=false"
            # Catch-all route -> Non-existing service (Priority low = last rule to execute)
            - "traefik.http.routers.catch-all-not-found.rule=HostRegexp(`{host:.+}`)"
            - "traefik.http.routers.catch-all-not-found.priority=1"
            - "traefik.http.routers.catch-all-not-found.service=noop@internal"
            - "traefik.http.routers.catch-all-not-found.entrypoints=http"
            - "traefik.http.routers.catch-all-not-found.middlewares=catch-all-redirectregex"
            # Router not-found.$DOMAIN
            - "traefik.enable=true"
            - "traefik.http.services.not-found-svc.loadbalancer.server.port=8000"
            - "traefik.http.routers.not-found.rule=Host(`not-found.${DOMAIN}`)"
            - "traefik.http.routers.not-found.service=not-found-svc"
            - "traefik.http.routers.not-found.entrypoints=http"
```
