import json
from flask import Flask, Response, render_template, request, stream_with_context
from dotenv import load_dotenv

load_dotenv()

from pipeline.discovery import discover
from pipeline.scoring import score_company
from pipeline.classify import classify
from pipeline.contact import find_contact
from pipeline.email_draft import draft_email

app = Flask(__name__)


def _event(event_type: str, data: dict) -> str:
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    industry = request.args.get("industry", "")
    region   = request.args.get("region", "")

    def generate():
        try:
            yield _event("status", {"text": "Starting discovery…"})
            for company in discover(industry, region):
                name = company.get("name", "")
                yield _event("status", {"text": f"Scoring {name}…"})
                company = score_company(company)
                if company.get("score", 0) < 6:
                    continue

                yield _event("status", {"text": f"Classifying {name}…"})
                classify_result = classify(company)
                if classify_result.get("flagged"):
                    yield _event("warning", {"text": f"Flagged and skipped: {name}"})
                    continue

                yield _event("status", {"text": f"Finding contact at {name}…"})
                company["contact"] = find_contact(company)

                yield _event("status", {"text": f"Drafting email for {name}…"})
                company = draft_email(company)

                yield _event("company", company)

            yield _event("done", {"text": "Scan complete."})

        except NotImplementedError:
            yield _event("error", {"text": "Pipeline not yet implemented."})
        except Exception as exc:
            yield _event("error", {"text": str(exc)})

    return Response(
        stream_with_context(generate()),
        content_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
