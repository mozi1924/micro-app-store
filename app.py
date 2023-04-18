from flask import Flask, render_template

import requests
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mdui')
def md_home():
    return render_template('index2.html')

@app.route('/get_apps')
def get_apps():
    # 发送 HTTP GET 请求获取 API 内容
    url = "https://api2.mina.mi.com/common_config/?configName=apk_management_preview"
    response = requests.get(url)

    # 解析响应内容
    if response.status_code == 200:
        json_data = json.loads(response.text)
        if json_data["code"] == 0:
            data = json.loads(json_data["data"])
            # 从解析后的 JSON 数据中获取需要的字段
            app_info_list = []
            for app in data:
                app_name = app["appName"]
                version_name = app["versionName"]
                download_url = app["downloadUrl"]
                package_name = app["packageName"]
                app_icon = app["iconUrl"]
                if "hardware" in app:
                    supported_models = app["hardware"]
                else:
                    supported_models = None
                if download_url and package_name != "com.xiaomi.mesh.gateway":  # 添加忽略包名为 "com.xiaomi.mesh.gateway" 的条件
                    app_info = {
                        'appName': app_name,
                        'versionName': version_name,
                        'downloadUrl': download_url,
                        'supportedModels': supported_models,
                        'packageName': package_name,
                        'iconUrl': app_icon
                    }
                    app_info_list.append(app_info)
                else:
                    print(f"已忽略 {app_name}，因为 DownloadUrl 为空或包名为 com.xiaomi.mesh.gateway。")
            return json.dumps(app_info_list)
        else:
            return "API 返回错误：" + json_data["message"]
    else:
        return "获取 API 内容失败，状态码：" + response.status_code

if __name__ == '__main__':
    app.run(debug=True)
