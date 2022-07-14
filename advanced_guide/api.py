import time

from fastapi import FastAPI, Response, Request, Depends
from fastapi.responses import ORJSONResponse


app = FastAPI()


class FixedContentQueryChecker:
    def __init__(self, fixed_content: list):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return q in self.fixed_content
        return False


checker = FixedContentQueryChecker(['bar', 'lil', 'met'])


@app.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_included}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    return [{"item_id": "Foo"}]


@app.get("/legacy/")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")