import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, simpledialog
import subprocess
import sys
import os
import webbrowser

TSINGHUA_SOURCE = "https://pypi.tuna.tsinghua.edu.cn/simple"
URL_HOME = "https://www.bilibili.com/video/BV1y6hx6fEfU"     # 视频演示链接
URL_HELP = "https://github.com/e-CNY/PIP-management-tool-System-Virtual-Environment/blob/main/README.md"     # 使用说明链接

# ========== 链接打开函数==========
def open_home(event):
    webbrowser.open(URL_HOME)

def open_help(event):
    webbrowser.open(URL_HELP)
# ==========================================================

def log_print(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    root.update()

def get_venv_python(venv_path):
    if not venv_path or not os.path.exists(venv_path):
        return None
    if sys.platform.startswith("win"):
        py_path = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        py_path = os.path.join(venv_path, "bin", "python")
    if os.path.exists(py_path):
        return py_path
    return None

def run_pip_cmd(py_exe, args, use_mirror):
    install_cmds = {"install"}
    if use_mirror and len(args)>=2 and args[0] in install_cmds:
        args += ["-i", TSINGHUA_SOURCE]

    log_print(f">>> 使用解释器：{py_exe}")
    log_print(f">>> 命令: {' '.join(args)}")
    popen_kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
        "text": True
    }
    if sys.platform == "win32":
        popen_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

    proc = subprocess.Popen([py_exe] + args, **popen_kwargs)
    while True:
        line = proc.stdout.readline()
        if not line and proc.poll() is not None:
            break
        if line:
            log_print(line.rstrip())
    ret_code = proc.returncode
    log_print(f"<<<< 执行完成，返回码：{ret_code}\n")

# ====================== 系统环境 5个功能 ======================
def sys_install():
    pkg = entry_pkg.get().strip()
    if not pkg:
        log_print("⚠️ 请输入包名称！")
        return
    run_pip_cmd(sys.executable, ["-m", "pip", "install", pkg], var_mirror.get())

def sys_uninstall():
    pkg = entry_pkg.get().strip()
    if not pkg:
        log_print("⚠️ 请输入包名称！")
        return
    run_pip_cmd(sys.executable, ["-m", "pip", "uninstall", "-y", pkg], var_mirror.get())

def sys_upgrade_pkg():
    pkg = entry_pkg.get().strip()
    if not pkg:
        log_print("⚠️ 请输入包名称！")
        return
    run_pip_cmd(sys.executable, ["-m", "pip", "install", "--upgrade", pkg], var_mirror.get())

def sys_list():
    run_pip_cmd(sys.executable, ["-m", "pip", "list"], var_mirror.get())

def sys_upgrade_pip():
    run_pip_cmd(sys.executable, ["-m", "pip", "install", "--upgrade", "pip"], var_mirror.get())

# ====================== 虚拟环境 6个功能 ======================
def venv_install():
    pkg = entry_pkg.get().strip()
    venv_dir = entry_venv.get().strip()
    if not pkg:
        log_print("⚠️ 请输入包名称！")
        return
    py_venv = get_venv_python(venv_dir)
    if py_venv is None:
        log_print("❌ 虚拟环境目录无效，找不到python.exe！")
        return
    run_pip_cmd(py_venv, ["-m", "pip", "install", pkg], var_mirror.get())

def venv_uninstall():
    pkg = entry_pkg.get().strip()
    venv_dir = entry_venv.get().strip()
    if not pkg:
        log_print("⚠️ 请输入包名称！")
        return
    py_venv = get_venv_python(venv_dir)
    if py_venv is None:
        log_print("❌ 虚拟环境目录无效！")
        return
    run_pip_cmd(py_venv, ["-m", "pip", "uninstall", "-y", pkg], var_mirror.get())

def venv_upgrade_pkg():
    pkg = entry_pkg.get().strip()
    venv_dir = entry_venv.get().strip()
    if not pkg:
        log_print("⚠️ 请输入包名称！")
        return
    py_venv = get_venv_python(venv_dir)
    if py_venv is None:
        log_print("❌ 虚拟环境目录无效！")
        return
    run_pip_cmd(py_venv, ["-m", "pip", "install", "--upgrade", pkg], var_mirror.get())

def venv_list():
    venv_dir = entry_venv.get().strip()
    py_venv = get_venv_python(venv_dir)
    if py_venv is None:
        log_print("❌ 虚拟环境目录无效！")
        return
    run_pip_cmd(py_venv, ["-m", "pip", "list"], var_mirror.get())

def venv_upgrade_pip():
    venv_dir = entry_venv.get().strip()
    py_venv = get_venv_python(venv_dir)
    if py_venv is None:
        log_print("❌ 虚拟环境目录无效！")
        return
    run_pip_cmd(py_venv, ["-m", "pip", "install", "--upgrade", "pip"], var_mirror.get())

def venv_fix_pip():
    venv_dir = entry_venv.get().strip()
    py_venv = get_venv_python(venv_dir)
    if py_venv is None:
        log_print("❌ 虚拟环境目录无效！")
        return
    log_print("正在修复虚拟环境pip（ensurepip）...")
    run_pip_cmd(py_venv, ["-m", "ensurepip", "--upgrade"], var_mirror.get())

def browse_venv():
    folder = filedialog.askdirectory(title="选择虚拟环境存放的父文件夹")
    if folder:
        entry_venv.delete(0, tk.END)
        entry_venv.insert(0, folder)

def create_venv():
    base_path = entry_venv.get().strip()
    if not base_path:
        log_print("⚠️ 请先使用浏览选择父文件夹！")
        return
    if not os.path.isdir(base_path):
        log_print(f"❌ 父目录不存在：{base_path}")
        return
    env_name = simpledialog.askstring("新建虚拟环境", "请输入虚拟环境文件夹名称：", initialvalue="venv")
    if not env_name:
        log_print("ℹ️ 已取消创建")
        return
    venv_dir = os.path.join(base_path, env_name)
    if os.path.exists(venv_dir):
        log_print(f"❌ 目录 {venv_dir} 已经存在，不能重复创建！")
        return
    log_print(f">>> 开始创建虚拟环境：{venv_dir}")
    popen_kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
        "text": True
    }
    if sys.platform == "win32":
        popen_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    proc = subprocess.Popen([sys.executable, "-m", "venv", venv_dir],** popen_kwargs)
    while True:
        line = proc.stdout.readline()
        if not line and proc.poll() is not None:
            break
        if line:
            log_print(line.rstrip())
    ret_code = proc.returncode
    if ret_code == 0:
        log_print(f"✅ 虚拟环境创建成功！路径：{venv_dir}\n提示：部分python版本创建后缺少pip，可点【修复pip】")
        entry_venv.delete(0, tk.END)
        entry_venv.insert(0, venv_dir)
    else:
        log_print(f"❌ 创建虚拟环境失败，返回码：{ret_code}\n")

# ====================== UI布局 ======================
root = tk.Tk()
root.title("PIP管理工具｜系统 + 虚拟环境")
root.geometry("920x600")

var_mirror = tk.BooleanVar(value=True)

# 第1行：包名称输入 + 镜像复选框
frame1 = ttk.Frame(root)
frame1.pack(pady=6, padx=10, fill="x")
ttk.Label(frame1, text="包名称：").pack(side=tk.LEFT)
entry_pkg = ttk.Entry(frame1)
entry_pkg.pack(side=tk.LEFT, padx=6, fill="x", expand=True)
entry_pkg.insert(0, "numpy")
chk_mirror = ttk.Checkbutton(frame1, text="使用清华镜像源", variable=var_mirror)
chk_mirror.pack(side=tk.LEFT, padx=10)

# 第2行：系统环境按钮 5个
frame2 = ttk.Frame(root)
frame2.pack(pady=6, padx=10)
ttk.Label(frame2, text="系统环境：").grid(row=0, column=0)
ttk.Button(frame2, text="安装", command=sys_install).grid(row=0, column=1, padx=3)
ttk.Button(frame2, text="卸载", command=sys_uninstall).grid(row=0, column=2, padx=3)
ttk.Button(frame2, text="升级", command=sys_upgrade_pkg).grid(row=0, column=3, padx=3)
ttk.Button(frame2, text="列出所有包", command=sys_list).grid(row=0, column=4, padx=3)
ttk.Button(frame2, text="pip升级", command=sys_upgrade_pip).grid(row=0, column=5, padx=3)

# 第3行：虚拟环境目录 + 浏览 + 创建
frame3 = ttk.Frame(root)
frame3.pack(pady=6, padx=10, fill="x")
ttk.Label(frame3, text="虚拟环境目录：").pack(side=tk.LEFT)
entry_venv = ttk.Entry(frame3)
entry_venv.pack(side=tk.LEFT, padx=6, fill="x", expand=True)
ttk.Button(frame3, text="浏览", command=browse_venv).pack(side=tk.LEFT)
ttk.Button(frame3, text="创建", command=create_venv).pack(side=tk.LEFT, padx=4)

# 第4行：虚拟环境按钮 6个
frame4 = ttk.Frame(root)
frame4.pack(pady=6, padx=10)
ttk.Label(frame4, text="虚拟环境：").grid(row=0, column=0)
ttk.Button(frame4, text="安装", command=venv_install).grid(row=0, column=1, padx=3)
ttk.Button(frame4, text="卸载", command=venv_uninstall).grid(row=0, column=2, padx=3)
ttk.Button(frame4, text="升级", command=venv_upgrade_pkg).grid(row=0, column=3, padx=3)
ttk.Button(frame4, text="列出所有包", command=venv_list).grid(row=0, column=4, padx=3)
ttk.Button(frame4, text="pip升级", command=venv_upgrade_pip).grid(row=0, column=5, padx=3)
ttk.Button(frame4, text="修复pip", command=venv_fix_pip).grid(row=0, column=6, padx=3)

# 日志
ttk.Label(root, text="运行日志：").pack(anchor="w", padx=10)
log_box = scrolledtext.ScrolledText(root, height=18)
log_box.pack(padx=10, pady=4, fill="both", expand=True)

# ========== 底部链接栏==========
frame_bottom = ttk.Frame(root)
frame_bottom.pack(pady=4, padx=10, fill="x")

link_home = ttk.Label(frame_bottom, text="视频演示", foreground="blue", cursor="hand2")
link_home.pack(side=tk.LEFT)
link_home.bind("<Button-1>", open_home)

link_help = ttk.Label(frame_bottom, text="使用说明", foreground="blue", cursor="hand2")
link_help.pack(side=tk.RIGHT)
link_help.bind("<Button-1>", open_help)
# =============================================================

root.mainloop()
