#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json

url = 'http://localhost:8901/'

req = {
    "title": "The Supreme Court’s clear message to President Trump: Stop",
    "content": "During the past four years, President Donald Trump has challenged the integrity of the Supreme Court",
    "link_id": "4228374795428832573"
}

resp = requests.post(url, json.dumps(req))
print("status code:", resp.status_code)
print(json.dumps(resp.json(), indent=2))
