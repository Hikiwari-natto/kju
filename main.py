from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional

# FastAPIの本体を作成します（ここから全てが始まります）
# 修正履歴：ガイドラインのテストのためにコメントを追加しました
app = FastAPI()
# HTMLテンプレート（画面のデザイン）が置いてある場所を指定します
templates = Jinja2Templates(directory="templates")

# TODO（やること）のデータの形を定義します
class Todo(BaseModel):
    id: int               # 番号
    title: str            # 内容
    completed: bool = False # 終わったかどうか（最初は「まだ」）

# データを一時的に保存しておくための場所（リスト）です
todos: List[Todo] = []
# 番号を自動で付けるためのカウンターです
id_counter = 1

# 最初の画面（トップページ）を表示する設定です
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # index.htmlを表示します。その際、todosの中身も一緒に渡します
    return templates.TemplateResponse(request, "index.html", {"todos": todos})

# 新しいTODOを追加する設定です
@app.post("/add")
async def add_todo(title: str = Form(...)):
    global id_counter
    # 新しいTODOを作成します
    new_todo = Todo(id=id_counter, title=title)
    # リストに追加します
    todos.append(new_todo)
    # 番号を1つ増やします
    id_counter += 1
    # 追加し終わったら、またトップページに戻ります
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# TODOの「完了」と「未完了」を切り替える設定です
@app.get("/complete/{todo_id}")
async def complete_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            # 完了状態を反対にします（未完了なら完了に、完了なら未完了に）
            todo.completed = not todo.completed
            break
    # 切り替えたら、トップページに戻ります
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# TODOを削除する設定です
@app.get("/delete/{todo_id}")
async def delete_todo(todo_id: int):
    global todos
    # 指定された番号以外のTODOだけを残すことで、実質的に削除します
    todos = [todo for todo in todos if todo.id != todo_id]
    # 削除したら、トップページに戻ります
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

if __name__ == "__main__":
    import uvicorn
    import socket

    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    # 直接実行された場合にサーバーを起動します
    # ポート8000が使用中の場合は8001を使用します
    port = 8000
    if is_port_in_use(port):
        port = 8001
    
    uvicorn.run(app, host="127.0.0.1", port=port)
