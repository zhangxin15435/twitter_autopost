@echo off
chcp 65001 > nul
echo 🚀 Twitter自动发布机器人 - GitHub Actions部署脚本
echo ==================================================

REM 检查是否在Git仓库中
git rev-parse --git-dir > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：当前目录不是Git仓库
    echo 请先初始化Git仓库：git init
    pause
    exit /b 1
)

REM 检查必要文件
echo 📋 检查必要文件...

set "files=main.py requirements.txt config.env.example connect_twitter.py connect_feishu.py"
for %%f in (%files%) do (
    if exist "%%f" (
        echo ✅ %%f 存在
    ) else (
        echo ❌ %%f 不存在
        pause
        exit /b 1
    )
)

REM 检查GitHub工作流文件
echo 🔧 检查GitHub工作流文件...

if exist ".github\workflows" (
    echo ✅ .github\workflows 目录存在
) else (
    echo ❌ .github\workflows 目录不存在
    echo 请确保已经创建了GitHub Actions工作流文件
    pause
    exit /b 1
)

set "workflow_files=.github\workflows\schedule_publish.yml .github\workflows\manual_publish.yml .github\workflows\ci.yml"
for %%f in (%workflow_files%) do (
    if exist "%%f" (
        echo ✅ %%f 存在
    ) else (
        echo ❌ %%f 不存在
        pause
        exit /b 1
    )
)

REM 检查Git远程仓库
echo 🔗 检查Git远程仓库...

git remote -v | findstr "github.com" > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 已配置GitHub远程仓库
    for /f "tokens=2" %%i in ('git remote get-url origin') do echo    远程仓库：%%i
) else (
    echo ❌ 未配置GitHub远程仓库
    echo 请先添加GitHub远程仓库：
    echo    git remote add origin https://github.com/用户名/仓库名.git
    pause
    exit /b 1
)

REM 提示配置Secrets
echo 🔐 GitHub Secrets配置提醒
echo ==================================================
echo 请在GitHub仓库中配置以下Secrets：
echo.
echo Twitter API配置：
echo - TWITTER_CONSUMER_KEY
echo - TWITTER_CONSUMER_SECRET
echo - TWITTER_ACCESS_TOKEN
echo - TWITTER_ACCESS_TOKEN_SECRET
echo - TWITTER_BEARER_TOKEN
echo.
echo 飞书API配置：
echo - FEISHU_APP_ID
echo - FEISHU_APP_SECRET
echo - FEISHU_BITABLE_TOKEN
echo - FEISHU_TABLE_ID
echo.
echo 配置路径：GitHub仓库 ^> Settings ^> Secrets and variables ^> Actions
echo.

REM 询问是否推送代码
set /p "push_code=是否现在推送代码到GitHub？(y/n): "
if /i "%push_code%"=="y" (
    echo 📤 推送代码到GitHub...
    
    REM 添加所有文件
    git add .
    
    REM 提交代码
    set /p "commit_message=请输入提交信息（默认：Deploy to GitHub Actions）: "
    if "%commit_message%"=="" set "commit_message=Deploy to GitHub Actions"
    
    git commit -m "%commit_message%"
    
    REM 推送到远程仓库
    git push -u origin main
    
    echo ✅ 代码推送完成
) else (
    echo ⏭️  跳过代码推送
)

echo.
echo 🎉 部署脚本执行完成！
echo ==================================================
echo 下一步操作：
echo 1. 在GitHub仓库中配置所有必需的Secrets
echo 2. 进入GitHub仓库的Actions页面
echo 3. 运行'手动发布Twitter内容'工作流的test模式
echo 4. 确认定时任务正常工作
echo.
echo 📚 详细文档：查看 GITHUB_ACTIONS_DEPLOYMENT_GUIDE.md
echo ==================================================
pause 