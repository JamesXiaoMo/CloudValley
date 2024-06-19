@app.route('/upload_firmware/<project>', methods=['POST'])
def upload_file(project):
    if 'file' not in request.files:
        return jsonify({"error": "没有文件"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        project_folder = os.path.join(app.config['UPLOAD_FOLDER'], project)
        try:
            os.makedirs(project_folder, exist_ok=True)
            file.save(os.path.join(project_folder, filename))
            logging.info(f'文件 {filename} 已上传到 {project_folder}')
            return jsonify({"message": "上传成功"}), 200
        except Exception as e:
            logging.error(f'保存文件时出错: {e}')
            return jsonify({"error": "文件保存错误"}), 500
    else:
        return jsonify({"error": "无效的文件"}), 400