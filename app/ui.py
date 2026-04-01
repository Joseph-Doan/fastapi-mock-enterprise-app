from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def login_page():
    return """
    <html>
      <body>
        <h1>Login</h1>
        <form method="post" action="/login">
          <input name="username" type="text" />
          <input name="password" type="password" />
          <button type="submit">Login</button>
        </form>
      </body>
    </html>
    """

@router.post("/login")
def login(username: str, password: str):
    if username == "admin" and password == "password":
        return {"message": "ok"}
    return {"message": "invalid"}

@router.get("/devices", response_class=HTMLResponse)
def devices_page():
    return """
    <html>
      <body>
        <h1>Devices</h1>
        <ul><li>Router-01</li><li>Switch-01</li></ul>
      </body>
    </html>
    """

@router.post("/login")
async def login_submit(...):
    # after verifying login success
    response = RedirectResponse(url="/devices", status_code=303)
    response.set_cookie(key="token", value="fake-jwt-token")
    return response