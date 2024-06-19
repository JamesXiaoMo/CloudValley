from flask import Flask, request, send_from_directory
from VersionController import VersionController

app = Flask(__name__)
firmware_path = 'firmware'

VC = VersionController(firmware_path)


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


@app.route('/install/<project>/<version>', methods=["GET"])
def post_firmware(version):
    return send_from_directory('firmware', '{}.bin'.format(version))


if __name__ == '__main__':
    print('固件版本控制服务器启动！')
    app.run(host='0.0.0.0', port=5550)
