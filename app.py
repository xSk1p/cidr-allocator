"""
API - uvicorn api:app --reload
"""

import logging
from fastapi import FastAPI
from cidr_manipulator import next_available_range

logging.basicConfig(
        filename = 'logs/app.log',
        level = logging.INFO,
        format = '%(levelname)s:%(asctime)s:%(message)s')

app = FastAPI()

@app.get("/")
async def root():
    """root path with app instructions."""
    return 'Welcome to CIDR allocator please use /allocator?cidr=<CIDR>'

@app.get("/allocator")
async def read_items(cidr: str = 0):
    """get& process CIDR block input and returns the available next range."""
    return "Available range:", next_available_range(cidr)
