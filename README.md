# niri-wallpaper-manager
用于 niri 窗口管理器的壁纸自动切换工具。当窗口覆盖壁纸或露出壁纸时，自动执行你指定的命令，可以实现动态壁纸的自动暂停。

## 功能：
- 监听 niri 的事件流，实时感知窗口状态变化
- 窗口被覆盖（存在焦点窗口且未打开 Overview）时执行 -c 指定的命令
- 窗口露出（无焦点窗口或 Overview 打开）时执行 -u 指定的命令
- 支持启动时执行自定义命令 -i
- 支持退出时（Ctrl+C / kill）执行自定义命令 -q

## 依赖
- Python 3.7+
- niri 窗口管理器及其 niri msg 命令
- 你的壁纸命令（如 swaybg、mpvpaper 或任何 shell 命令）

## 用法：
```bash
-i --init      初始命令（可选）
-c --covered   覆盖时
-u --uncovered 未覆盖时，包括 overview
-q --quit      退出时执行的命令（可选）
```

## 示例
```bash
nohup python3 /home/mingyang/Code/Project/niri-wallpaper-manager.py \
-i 'mpvpaper -f -o "loop=yes panscan=1.0 hwdec=auto input-ipc-server=/tmp/mpv-socket keep-open=always osd-level=0" ALL /home/mingyang/ba/ch0082.mp4' \
-c 'echo "set loop no" | socat - /tmp/mpv-socket' \
-u 'echo "set loop yes" | socat - /tmp/mpv-socket; echo "set pause no" | socat - /tmp/mpv-socket' \
-q 'pkill mpvpaper'
```
