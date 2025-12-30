@echo off
REM Docker启动脚本（Windows）
echo Starting De Anza College API with Docker...

REM 检查Docker是否运行
docker ps >nul 2>&1
if errorlevel 1 (
    echo [错误] Docker未运行！
    echo 请先启动Docker Desktop
    pause
    exit /b 1
)

echo [信息] Docker正在运行
echo [信息] 正在构建并启动容器...

REM 构建并启动
docker-compose up -d --build

if errorlevel 1 (
    echo [错误] 启动失败
    pause
    exit /b 1
)

echo.
echo [成功] API已启动！
echo.
echo 访问地址:
echo   - 首页: http://localhost:8000
echo   - API文档: http://localhost:8000/docs
echo   - 统计信息: http://localhost:8000/stats
echo.
echo 查看日志: docker-compose logs -f
echo 停止服务: docker-compose down
echo.
pause

