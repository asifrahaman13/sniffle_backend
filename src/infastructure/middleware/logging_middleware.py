import logging
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.infastructure.repositories.auth_repository import AuthRepository
from src.internal.use_cases.auth_service import AuthService
from src.internal.interfaces.auth_interface import AuthInterface

auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)


class PrefixMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, prefix=""):
        super().__init__(app)
        self.app = app
        self.prefix = prefix
        self.protected_routes = ["fhir", "data"]

    async def authenticate(self, request):
        auth_interface: AuthInterface = auth_service
        logging.info("############################# authenticating")
        try:
            if request.method=="POST":
                token = request.headers.get("Authorization").split(" ")[1]
            else: 
                token= request.url.path.split("/")[-1]
                print(token)

            logging.info(f"Token: {token}")
            if not token:
                raise HTTPException(status_code=401, detail="Unauthorized")
            
            result=auth_interface.decode_access_token(token)
            logging.info("The decoded token is: ", result)
            if "error" in result:
                raise HTTPException(status_code=401, detail="Unauthorized")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Unauthorized")
        

    async def dispatch(self, request, call_next):
        self.prefix=request.url.path.split("/")[1]
        print(f"Request with prefix {self.prefix}")
        if self.prefix in self.protected_routes:
            print(f"Protected route {self.protected_routes}")
            try:
                await self.authenticate(request)
                response = await call_next(request)
                return response
            except HTTPException as e:
                return JSONResponse(status_code=e.status_code, content={"message": str(e)})
        else:
            response = await call_next(request)
            return response
