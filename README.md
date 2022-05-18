# py-web-server

git@github.com:ShiWenber/py-web-server.git

## 前言

### 文件结构

venv 虚拟环境相关文件(不要上传)：

- Lib
- Include
- Scripts
- pyvenv.cfg

原码文件 src

### 虚拟环境的使用

在 py-web-server 目录打开命令行(推荐 powershell)

```powershell
# 命令行进入项目 py-web-server 的父目录
Set-Location py-web-server
Set-Location ..

# 创建虚拟环境
Set-Location py-web-server
python -m venv py-web-server 
# 激活虚拟环境
.\Scripts\activate
```

![image-20220518100345959](README.assets/image-20220518100345959.png)

如图表示已经进入虚拟环境，此时使用 pip 将仅在本项目文件中起作用

```powershell
# 下载虚拟环境包列表中的包
pip install -r requirements.txt
```

下载新包后更新虚拟环境的包列表

```powershell
# 导出当前环境存在的包(上传前需要进行该步骤)
pip freeze > requirements.txt
```

退出虚拟环境

```powershell
deactivate
```