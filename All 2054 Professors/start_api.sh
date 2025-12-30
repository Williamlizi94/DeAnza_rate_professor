#!/bin/bash
# 启动API服务器（Linux/Mac脚本）

cd "$(dirname "$0")"
echo "Starting De Anza College API Server..."

# 创建logs目录
mkdir -p logs

# 后台运行
nohup python3 run_api_server.py > logs/server.log 2>&1 &

echo "API Server started. PID: $!"
echo "Logs: logs/server.log"
echo "To stop: kill $!"


