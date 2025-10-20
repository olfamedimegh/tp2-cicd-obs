import logging
import os
import time
from flask import Flask, jsonify, request
from opentelemetry import trace, metrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Initialise OTel (export OTLP -> OTel Collector)
import opentelemetry_bootstrap  # noqa: F401

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# Logging JSON vers stdout (capturé par Promtail)
logging.basicConfig(
    level=logging.INFO,
    format='{"level":"%(levelname)s","message":"%(message)s","ts":"%(asctime)s"}'
)
logger = logging.getLogger("tp2")

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)
req_counter = meter.create_counter("requests_total", description="Total HTTP requests")

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/")
def home():
    req_counter.add(1, {"endpoint": "/"})
    with tracer.start_as_current_span("home_handler"):
        logger.info("Home endpoint hit")
        return jsonify({"hello": "world", "path": request.path})

@app.route("/work")
def work():
    req_counter.add(1, {"endpoint": "/work"})
    with tracer.start_as_current_span("simulate_work") as span:
        delay = float(request.args.get("delay", "0.1"))
        time.sleep(delay)
        span.set_attribute("work.delay_ms", int(delay * 1000))
        logger.info(f"Did some work in {delay}s")
        return jsonify({"done_in_seconds": delay})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=False)