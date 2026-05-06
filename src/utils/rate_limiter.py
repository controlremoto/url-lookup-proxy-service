from fastapi import Request, HTTPException, status
from src.utils.logger import get_logger
import time
from src.config.constants import RATE_LIMIT, RATE_LIMIT_WINDOW, LOGGER_NAME

logger = get_logger(LOGGER_NAME)

_visits = {}

# Simple in-memory rate limiter based on client IP and time window
def rate_limiter(request: Request):
    ip = request.client.host
    now = int(time.time())
    window_start = now - RATE_LIMIT_WINDOW
    visits = _visits.setdefault(ip, [])
    # Remove old
    _visits[ip] = [t for t in visits if t > window_start]
    if len(_visits[ip]) >= RATE_LIMIT:
        headers = dict(request.headers)
        # Log client IP and headers and url_path for the exceeded request
        logger.warning(f"Rate limit exceeded for IP: {ip}, headers: {headers}, url_path: {request.url.path}")
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
    _visits[ip].append(now)
