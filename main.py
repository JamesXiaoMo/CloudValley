from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)
firmware_path = 'firmware'
latest_version = None


class VersionController:
    def __init__(self):
        self.firmware_list = []
        self.projects_dict = {}
        self.firmware_path = firmware_path
        self.refresh_firmware_list()

    def show_firmware_list(self):
        print('固件列表:')
        for i in self.firmware_list:
            print(i)

    def refresh_firmware_list(self):
        try:
            projects_list = os.listdir(self.firmware_path)
            p_id = 0
            for project in projects_list:
                self.projects_dict[str(project)] = p_id
                p_id += 1
            print(self.projects_dict)
            print('刷新完成!共{}个项目的{}个版本的固件'.format('6', str(len(self.firmware_list))))
        except OSError as e:
            print(e)


@app.route('/check_version', methods=['POST'])
def check_version():
    current_version = request.form.get('version')
    if current_version < latest_version:
        return latest_version
    else:
        return "NO_UPDATE"


@app.route('/upgrade/<version>', methods=["GET"])
def post_firmware(version):
    return send_from_directory('firmware', '{}.bin'.format(version))


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    a = VersionController()
