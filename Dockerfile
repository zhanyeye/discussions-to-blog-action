# 使用一个轻量级的 Python 镜像  
FROM python:3.9-slim  

WORKDIR /app  

COPY requirements.txt .  

# 安装依赖  
RUN pip install --no-cache-dir -r requirements.txt  

# 复制所有文件到容器工作目录  
COPY . .  

# 调试：打印当前工作目录文件列表  
RUN echo "打印 /app 文件列表:" && ls -la /app 

# 声明入口文件 (entrypoint.py 必须存在于项目根目录)  
ENTRYPOINT ["python", "/app/entrypoint.py"]  entrypoint.py