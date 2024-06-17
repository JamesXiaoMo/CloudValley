from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)
firmware_path = 'firmware'
latest_version = "1.1.0"  # 最新固件版本


class VersionControl:
    def __init__(self):
        self.firmware_path = firmware_path
        try:
            self.firmware_list = os.listdir(self.firmware_path)
            print('共找到{}个版本的固件'.format(str(len(self.firmware_list))))
        except OSError as e:
            print(e)

    def show_firmware_list(self):
        print('固件列表:\n')
        for i in self.firmware_list:
            print(i)

    def refresh_firmware_list(self):
        try:
            self.firmware_list = os.listdir(self.firmware_path)
            print('刷新完成!共找到{}个版本的固件'.format(str(len(self.firmware_list))))
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
    a = VersionControl()
    a.show_firmware_list()
