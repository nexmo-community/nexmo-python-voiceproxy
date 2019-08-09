import os
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, PlainTextResponse
import uvicorn
import structlog

load_dotenv()
app = Starlette(debug=True)
log = structlog.get_logger()


@app.route("/")
class VoiceProxy(HTTPEndpoint):
    async def get(self, request):
        return JSONResponse(
            [
                {
                    "action": "connect",
                    "from": os.getenv("NEXMO_NUMBER_FROM"),
                    "endpoint": [
                        {"type": "phone", "number": os.getenv("NEXMO_NUMBER_TO")}
                    ],
                }
            ]
        )


async def post(self, request):
    event = await request.json()
    log.msg("Voice Proxy", **event)
    return PlainTextResponse()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
