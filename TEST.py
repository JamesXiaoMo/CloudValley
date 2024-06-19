from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 配置上传文件的存储路径和允许的文件类型
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'bin'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查请求中是否包含文件部分
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # 如果用户没有选择文件，浏览器也会提交一个没有文件名的空文件
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    # 创建上传文件夹
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)