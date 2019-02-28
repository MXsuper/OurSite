# 青光眼诊断项目 
网址: [https://www.killglaucoma.cn](https://www.killglaucoma.cn)
## 虚拟环境配置
### python版本为3.7
### 安装pytorch
```python
pip install https://download.pytorch.org/whl/cpu/torch-1.0.1-cp37-cp37m-win_amd64.whl
pip install torchvision
```
### 其他模块
```
djangorestframework
Markdown
Pillow
django-cors-headers # 后端服务器解决跨域问题的方法
django-guardian # drf对象级别的权限支持
djangorestframework-jwt # json web token方式完成用户认证
django-redis # django对redis的支持
drf-extensions # 缓存
selenium # 自动化测试
Django 
django-filter
coreapi  # drf的文档支持
torch
torchvision
channels_redis # websocket 先装这个不然下面的channels会失败
channels # websocket
```
> windows需要安装pypiwin32, 是channels需要