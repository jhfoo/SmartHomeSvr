# from flask import Flask, request, send_file
# core
import asyncio
from typing import Union
from time import sleep
import json
import sys

# community
from fastapi import FastAPI, Response

# custom
sys.path.append('.')
import src.route.kasa as RouteKasa
# import src.lib.ProcessImage as ProcessImage

app = FastAPI()
@app.on_event('startup')
async def onStartup():
  await RouteKasa.init()

app.include_router(RouteKasa.router, prefix = '/api')

