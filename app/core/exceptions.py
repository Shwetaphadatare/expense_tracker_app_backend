from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logger import logger

def register_exception_handlers(app):
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException
    ):
      
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success":False,
                "message":exc.detail
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc:RequestValidationError
    ):
        return JSONResponse(
            status_code=422,
            content={
                "success":False,
                "message":"validation error",
                "errors":exc.errors()
            }
        )
        
    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request,
        exc: Exception
    ):
        logger.exception(
            f"Unhandled server error at {request.url.path}: {str(exc)}"
        )
        return JSONResponse(
            status_code=500,
            content={
                "success":False,
                "message":"Internal server error"
            }
        )