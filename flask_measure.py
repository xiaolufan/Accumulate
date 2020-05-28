# coding: utf-8
# author: fxl

from flask import Flask, request, jsonify
from flask_cors import CORS
from queue import Queue
import threading
import traceback

# 构建app，解决跨域问题
app = Flask(__name__)
CORS(app)
# 设置主队列，用于线程间信息交互
main_queue = Queue(maxsize=5)


# 设置服务端口，获取前端传入的待预测信息
@app.route("/service", methods=["GET", "POST"])
def service():

    if request.method == "GET":
        data = request.args.get("content", type=str, default=None)
    else:
        data = request.form.get("content", type=str, default=None)

    # 设置子进程，供主线程与子线程之间交互
    sub_queue = Queue()
    # 通过主队列将前端请求信息与子队列对象传递给工作模块worker
    main_queue.put((data, sub_queue))
    # 由队列获取模型预测信息
    success, result = sub_queue.get()

    # 向前端返回预测结果
    if success:
        return jsonify(status="success", result=result)
    else:
        return jsonify(status="error", result=result)


def worker():
    '''
    加载模型对传入数据进行预测
    :return:
    '''
    # 加载模型到内存中，获取模型对象
    from model_util import load_model
    model = load_model()

    # 设置循环，持续处理前端发送的请求
    while True:

        # 通过主队列获取前端的请求信息和子队列
        data, sub_queue = main_queue.get()

        # 将模型执行结果传入子队列中，返回给请求接口
        try:
            result = model.predict(data)
            sub_queue.put((True, result))

        except Exception:

            trace = traceback.format_exc()
            sub_queue.put((False, trace))
            continue


if __name__ == "__main__":

    # 设置子线程，供模型加载以及模型预测
    t = threading.Thread(target=worker)
    # 设置线程守护，防止线程过载
    t.daemon = True
    # 子线程启动
    t.start()
    # 主线程运行app
    app.run(host='0.0.0.0', port='8081', threading=True)
