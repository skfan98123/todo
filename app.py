from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["todoapp"]
tasks_collection = db["tasks"]

def get_all_tasks():
    return list(tasks_collection.find().sort("order"))

@app.route("/")
def index():
    tasks = get_all_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task_name = request.form.get("task")
    task = {"name": task_name, "completed": False, "order": len(get_all_tasks()), "due_date": None}
    tasks_collection.insert_one(task)
    return redirect("/")

@app.route("/complete/<task_id>", methods=["POST"])
def complete(task_id):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if task:
        tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"completed": not task["completed"]}})
    return redirect("/")

@app.route("/delete/<task_id>", methods=["POST"])
def delete(task_id):
    tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return redirect("/")

@app.route("/rearrange", methods=["POST"])
def rearrange():
    task_ids = request.form.getlist("taskIds[]")
    for index, task_id in enumerate(task_ids, start=1):
        tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"order": index}})
    return "OK"

@app.route("/clear", methods=["POST"])
def clear():
    tasks_collection.delete_many({"completed": True})
    return redirect("/")

@app.route("/edit/<task_id>", methods=["POST"])
def edit(task_id):
    new_task_name = request.form.get("task")
    new_due_date = request.form.get("due_date")
    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"name": new_task_name, "due_date": new_due_date}}
    )
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
