import os


class VersionController:
    def __init__(self, firmware_path):
        self.firmware_list = []
        self.projects_dict = {}
        self.firmware_path = firmware_path
        self.refresh_firmware_list()

    def refresh_firmware_list(self):
        try:
            projects_list = os.listdir(self.firmware_path)
            if '.DS_Store' in projects_list:
                projects_list.remove('.DS_Store')
            p_id = 0
            f_num = 0
            for project in projects_list:
                self.projects_dict[str(project)] = p_id
                p_id += 1
                firmware_list = os.listdir(self.firmware_path + '/' + project)
                f_num += len(firmware_list)
                self.firmware_list.append(firmware_list)
            print('Refresh completed!Find {} projects and {} versions of firmware'.format(str(p_id), str(f_num)))
        except NotADirectoryError as e:
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
