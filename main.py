from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from function import functions

app = FastAPI()

default_function_name = '输出测试函数'

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名，应在生产中指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

class QuestionItem(BaseModel):
    question: str

standard_answer = ''
@app.get("/get_analysis_text")
async def get_analysis_text():
    global standard_answer
    return {"standard_answer": standard_answer}

def long_running_task(question: str):
    print(f"Processing question in the background: {question}")

    answer = a[default_function_name].execute(question)
    print(f"Done processing question: {question}")
    global standard_answer
    standard_answer = answer[0]

@app.post("/submit_question")
async def submit_question(background_tasks: BackgroundTasks, question_item: QuestionItem):
    print(f"Received question: {question_item.question}")
    b = functions('function.json')
    b.get_tree_json(default_function_name)
    global example_tree_data
    example_tree_data = b.get_tree_json(default_function_name)
    example_tree_data = a.get_tree_json(default_function_name)
    # 将长时间运行的任务添加到后台任务
    background_tasks.add_task(long_running_task, question_item.question)
    # 马上返回状态，不会阻塞
    return {"status": "success", "data": {"question": question_item.question}}



from fastapi.responses import JSONResponse

# 假设这是你的JSON数据
example_tree_data = {
    "tagName": "没有函数",
    "attrs": {
        "fill": "grey"
    },
    "children": []
}

@app.get("/get_tree_data")
async def get_tree_data():
    return JSONResponse(content=example_tree_data)


@app.get("/")
async def read_root():
    return {"message": "Hello from your FastAPI backend!"}

if __name__ == "__main__":
    a = functions('function.json')
    example_tree_data = a.get_tree_json(default_function_name)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)