import os

from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename

from VersionController import VersionController

app = Flask(__name__)
FIRMWARE_PATH = 'firmware'
ALLOWED_EXTENSIONS = {'bin'}
app.config['UPLOAD_FOLDER'] = FIRMWARE_PATH
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

VC = VersionController(FIRMWARE_PATH)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/check_upgrade/<project>', methods=['POST'])
def check_upgrade(project):
    current_version = request.form.get('version')
    latest_version = VC.upgrade_latest_firmware(project)
    if latest_version == 'Project Not Found':
        return 'Project_Not_Found'
    else:
        if current_version < latest_version:
            return latest_version
        else:
            return "NO_UPDATE"


@app.route('/upload_firmware/<project>', methods=['GET', 'POST'])
def upload_file(project):
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print('Firmware saved as /' + os.path.join(app.config['UPLOAD_FOLDER'] + '/' + str(project), filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/' + str(project), filename))
            return 'Upload success'
        else:
            return 'Please upload .bin file.'
    return '''
    <!doctype html>
    <title>上传新固件</title>
    <h1>为{}项目上传新固件</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''.format(str(project))


@app.route('/install/<project>/<version>', methods=["GET"])
def post_firmware(project, version):
    return send_from_directory('firmware/{}'.format(project), '{}.bin'.format(version))


if __name__ == '__main__':
    print('固件版本控制服务器启动！')
    app.run(host='0.0.0.0', port=5550)
