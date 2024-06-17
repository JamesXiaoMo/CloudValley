from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)
firmware_path = 'firmware'


class VersionController:
    def __init__(self):
        self.firmware_list = []
        self.projects_dict = {}
        self.firmware_path = firmware_path
        self.refresh_firmware_list()

    def refresh_firmware_list(self):
        try:
            projects_list = os.listdir(self.firmware_path)
            p_id = 0
            f_num = 0
            for project in projects_list:
                self.projects_dict[str(project)] = p_id
                p_id += 1
                firmware_list = os.listdir(self.firmware_path + '/' + project)
                f_num += len(firmware_list)
                self.firmware_list.append(firmware_list)
            print('刷新完成!共{}个项目的{}个版本的固件'.format(str(p_id), str(f_num)))
        except OSError as e:
            print(e)

    def upgrade_latest_firmware(self, project):
        if project not in self.projects_dict:
            return 'Project_Not_Found'
        else:
            current_project_firmware_list = self.firmware_list[self.projects_dict[project]]
            latest_firmware_version = current_project_firmware_list[0]
            for i in current_project_firmware_list:
                if i > latest_firmware_version:
                    latest_firmware_version = i
            return latest_firmware_version


VC = VersionController()


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
