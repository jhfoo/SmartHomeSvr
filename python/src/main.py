# from flask import Flask, request, send_file
# core
import asyncio
from typing import Union
from time import sleep
import json
import sys

# community
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI

# custom
sys.path.append('.')
import src.route.kasa as RouteKasa
import src.route.menu as RouteMenu
import src.route.metrics as RouteMetrics
import src.route.devconfig as RouteDevConfig
import classes.KasaManager as KasaManager
from classes.DevConfig import DevConfig
# import src.lib.ProcessImage as ProcessImage

def scheduled_job():
  print("APScheduler job running...")
  
app = FastAPI()
scheduler = AsyncIOScheduler()
@app.on_event('startup')
async def onStartup():
  scheduler.add_job(scheduled_job, IntervalTrigger(seconds=30))
  scheduler.start()
  await KasaManager.init(scheduler)
#  await RouteKasa.init(scheduler)
  await RouteMenu.init()
  DevConfig.init()

  app.include_router(RouteKasa.router, prefix = '/api')
  app.include_router(RouteMenu.router, prefix = '/api')
  app.include_router(RouteMetrics.router, prefix="/api")
  app.include_router(RouteDevConfig.router, prefix="/api")

