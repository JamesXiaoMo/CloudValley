import os

from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename

from VersionController import VersionController

app = Flask(__name__)
FIRMWARE_PATH = 'firmware'
ALLOWED_EXTENSIONS = {'bin'}
app.config['UPLOAD_FOLDER'] = FIRMWARE_PATH
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
latest_version = ''

VC = VersionController(FIRMWARE_PATH)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/check_upgrade/<project>/<current_version>', methods=['GET'])
def check_upgrade(project, current_version):
    print('{}, {}'.format(project, current_version))
    global latest_version
    latest_version = VC.upgrade_latest_firmware(project)
    print('Latest version:' + latest_version)
    if latest_version == 'Project Not Found':
        return 'Project_Not_Found'
    else:
        if current_version < latest_version:
            return send_from_directory(FIRMWARE_PATH + '/{}'.format(str(project)),
                                       '{}.bin'.format(str(latest_version)))
        else:
            return 'NO_UPDATE'


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
            VC.refresh_firmware_list()
            global latest_version
            latest_version = VC.upgrade_latest_firmware(project)
            print('Latest version:' + latest_version)
            return 'Upload success'
        else:
            return 'Please upload .bin file.'
    return '''
    <!doctype html>
    <title>Upload new firmware</title>
    <h1>Upload a new version of firmware for {}</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''.format(str(project))


@app.route('/install/<project>/<version>', methods=["GET"])
def post_firmware(project, version):
    return send_from_directory(FIRMWARE_PATH + '/{}'.format(str(project)), '{}.bin'.format(version))


if __name__ == '__main__':
    print('Firmware version control server start！')
    app.run(host='0.0.0.0', port=5000)
