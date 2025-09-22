from prometheus_client import Counter, Histogram, generate_latest,CONTENT_TYPE_LATEST
from fastapi import FastAPI , Response 
from starlette.middleware.base import BaseHTTPMiddleware
import time 

# define metrics
REQUESTS_COUNT = Counter('http_requests_total', 'Number of HTTP requests' , ['method','endpoint','status'])
REQUESTS_HISTOGRAM = Histogram('http_request_duration_seconds', 'HTTP Request latency', ['method','endpoint']) 

class PrometheusMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time
        endpoint = request.url.path
        REQUESTS_COUNT.labels(request.method, request.url.path, response.status_code).inc()
        REQUESTS_HISTOGRAM.labels(request.method, request.url.path).observe(duration)
        
        return response  
    
def setup_metrics(app: FastAPI) :
    app.add_middleware(PrometheusMiddleware)

    @app.get("/random_ass_name_4_security", include_in_schema=False)
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    
