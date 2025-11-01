from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from database import engine, get_db
from models import Base, List, Item


app = Flask(__name__)
Base.metadata.create_all(bind=engine)

@app.route("/")
def home():
    db = next(get_db())
    lists = db.query(List).order_by(List.name.asc()).all()
    return render_template("index.html", lists=lists)

@app.post("/lists")
def create_list():
    name = request.form.get("name", "").strip()
    if not name:
        return redirect(url_for("home"))
    db = next(get_db())
    db.add(List(name=name))
    db.commit()
    return redirect(url_for("home"))

@app.post("/lists/<int:list_id>/rename")
def rename_list(list_id):
    name = request.form.get("name", "").strip()
    db = next(get_db())
    lst = db.get(List, list_id)
    if not lst:
        abort(404)
    if name:
        lst.name = name
        db.commit()
    return redirect(url_for("home"))

@app.post("/lists/<int:list_id>/delete")
def delete_list(list_id):
    db = next(get_db())
    lst = db.get(List, list_id)
    if not lst:
        abort(404)
    db.delete(lst)
    db.commit()
    return redirect(url_for("home"))

@app.get("/lists/<int:list_id>")
def view_list(list_id):
    db = next(get_db())
    lst = db.get(List, list_id)
    if not lst:
        abort(404)
    items = db.query(Item).filter(Item.list_id == list_id).order_by(Item.id.desc()).all()
    return render_template("list.html", lst=lst, items=items)

@app.post("/lists/<int:list_id>/items")
def add_item(list_id):
    text = request.form.get("text", "").strip()
    db = next(get_db())
    lst = db.get(List, list_id)
    if not lst:
        abort(404)
    if text:
        db.add(Item(text=text, list_id=list_id))
        db.commit()
    return redirect(url_for("view_list", list_id=list_id))

@app.post("/items/<int:item_id>/toggle")
def toggle_item(item_id):
    db = next(get_db())
    it = db.get(Item, item_id)
    if not it:
        abort(404)
    it.done = not it.done
    db.commit()
    if request.headers.get("X-Requested-With") == "fetch":
        return jsonify({"ok": True, "done": it.done})
    return redirect(url_for("view_list", list_id=it.list_id))

@app.post("/items/<int:item_id>/delete")
def delete_item(item_id):
    db = next(get_db())
    it = db.get(Item, item_id)
    if not it:
        abort(404)
    lid = it.list_id
    db.delete(it)
    db.commit()
    if request.headers.get("X-Requested-With") == "fetch":
        return jsonify({"ok": True})
    return redirect(url_for("view_list", list_id=lid))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
