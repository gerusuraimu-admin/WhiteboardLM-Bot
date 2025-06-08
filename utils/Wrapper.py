import functools
from fastapi.responses import JSONResponse


def handle_wrapper(func):
    @functools.wraps(func)
    async def wrapper(payload) -> JSONResponse:
        try:
            await func(payload)
            return JSONResponse(status_code=200, content={'message': 'Success'})

        except Exception as e:
            return JSONResponse(status_code=500, content={'error': str(e)})

    return wrapper
