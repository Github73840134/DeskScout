from .. import const
from .. import types
import os
import json
from mods import gdr
from libs import requests
def putIntent(intent):
	requests.post(const.Service.Url.appIntent,data={'intent':intent})