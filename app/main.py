from fastapi import FastAPI, Request, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
import random, string, datetime
from app.app_logging import app_logger as logger
from app.db import db
from app.models import USER_TABLE_DDL

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await db.disconnect()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

class LoginRequest(BaseModel):
    email: EmailStr

class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str

def generate_auth_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

@app.post("/auth/request_code")
async def request_login_code(payload: LoginRequest):
    code = generate_auth_code()
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    async with db.pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO auth_codes (email, code, expires_at)
            VALUES ($1, $2, $3)
            """, payload.email, code, expires_at
        )
        logger.info(f"Auth code generated for {payload.email}")
    # In production, send code via email. For now, return it for testing.
    return {"message": "Auth code sent", "code": code}

@app.post("/auth/verify_code")
async def verify_login_code(payload: VerifyCodeRequest):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT * FROM auth_codes WHERE email=$1 AND code=$2 AND used=FALSE AND expires_at > NOW()
            """, payload.email, payload.code
        )
        if not row:
            logger.warning(f"Failed login attempt for {payload.email}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired code.")
        await conn.execute(
            "UPDATE auth_codes SET used=TRUE WHERE id=$1", row["id"]
        )
        logger.info(f"Successful login for {payload.email}")
        # Issue a dummy session token (to be replaced with JWT or session logic)
        return {"message": "Login successful", "email": payload.email}

async def get_user_role(email: str):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT r.name FROM users u JOIN roles r ON u.role_id = r.id WHERE u.email = $1
            """, email
        )
        if row:
            return row["name"]
        return None

def role_required(required_role: str):
    async def dependency(request: Request):
        email = request.headers.get("X-User-Email")
        if not email:
            logger.warning("Missing X-User-Email header for role check")
            raise HTTPException(status_code=401, detail="Missing user email header.")
        user_role = await get_user_role(email)
        if user_role != required_role:
            logger.warning(f"Unauthorized access attempt by {email} (role: {user_role}), required: {required_role}")
            raise HTTPException(status_code=403, detail="Insufficient role.")
        logger.info(f"Role check passed for {email} as {user_role}")
    return Depends(dependency)

@app.get("/admin/protected")
async def admin_protected_endpoint(dep=role_required("admin")):
    return {"message": "You have admin access."} 