from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def test1():
    return ("hello world!")


@app.get("/users")
def test2():
    return [
    {"id":1,"name":"张三"},
    {"id":2,"name":"李四"},
    {"id":3,"name":"王五"}
    ]

# 启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)