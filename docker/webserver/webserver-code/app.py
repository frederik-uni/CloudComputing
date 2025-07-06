import json
import os

import redis
from flask import Flask, redirect, url_for, make_response
from flask import render_template
from flask import request
from datetime import datetime
from uuid import uuid4

app = Flask(__name__)

r = redis.Redis(host=os.environ['REDIS_NAME'],
                port=6379, decode_responses=True,
                password=os.environ['REDIS_PASSWORD'])


@app.route("/")
@app.route("/create-poll")
def create_poll():
    return render_template("create-poll.html")


@app.route("/api/create-poll", methods=['POST'])
def api_create_poll():
    newId = uuid4()
    data = {
        "title": request.form["title"],
        "date1": request.form["date1"],
        "date2": request.form["date2"],
        "date3": request.form["date3"],
        "vote1": 0,
        "vote2": 0,
        "vote3": 0,
    }
    r.hset(f"created-polls:{newId}", mapping=data)
    print(f"{newId}", r.hgetall(f"created-polls:{newId}"))
    return render_template("create-poll.html", vote_url=os.environ['DOMAIN'] + url_for("vote", uuid=newId),
                           result_url=os.environ['DOMAIN'] + url_for("result", uuid=newId))


@app.route("/api/vote/<uuid>", methods=['POST'])
def api_vote(uuid=None):
    print(uuid)
    data: dict = r.hgetall(f"created-polls:{uuid}")
    data["vote1"] = int(data["vote1"]) + (1 if request.form.get("date1") == "on" else 0)
    data["vote2"] = int(data["vote2"]) + (1 if request.form.get("date2") == "on" else 0)
    data["vote3"] = int(data["vote3"]) + (1 if request.form.get("date3") == "on" else 0)
    r.hset(f"created-polls:{uuid}", mapping=data)
    print(r.hgetall(f"created-polls:{uuid}"))
    resp = make_response(redirect(request.referrer))
    resp.set_cookie(f"voted:{uuid}", "True")
    return resp


@app.route("/vote/<uuid>")
def vote(uuid=None):
    title = r.hget(f"created-polls:{uuid}", "title")
    date1 = r.hget(f"created-polls:{uuid}", "date1")
    date2 = r.hget(f"created-polls:{uuid}", "date2")
    date3 = r.hget(f"created-polls:{uuid}", "date3")
    is_disabled = request.cookies.get(f'voted:{uuid}') == "True"
    return render_template("vote.html", title=title, date1=datetime_human_readable(date1),
                           date2=datetime_human_readable(date2), date3=datetime_human_readable(date3), uuid=uuid,
                           disabled="disabled" if is_disabled else "")


@app.route("/result/<uuid>")
def result(uuid=None):
    title = r.hget(f"created-polls:{uuid}", "title")
    date1 = r.hget(f"created-polls:{uuid}", "date1")
    date2 = r.hget(f"created-polls:{uuid}", "date2")
    date3 = r.hget(f"created-polls:{uuid}", "date3")
    vote1 = r.hget(f"created-polls:{uuid}", "vote1")
    vote2 = r.hget(f"created-polls:{uuid}", "vote2")
    vote3 = r.hget(f"created-polls:{uuid}", "vote3")
    return render_template("results.html", title=title, date1=datetime_human_readable(date1),
                           date2=datetime_human_readable(date2), date3=datetime_human_readable(date3), vote1=vote1,
                           vote2=vote2, vote3=vote3, total=int(vote1) + int(vote2) + int(vote3))


def datetime_human_readable(timestamp: str):
    try:
        dt_object = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M")
    except ValueError:
        return None
    return dt_object.strftime("%d.%m.%Y at %H:%M")
