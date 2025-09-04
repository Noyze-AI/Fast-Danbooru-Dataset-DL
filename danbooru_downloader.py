# -*- coding: utf-8 -*-
import subprocess
import os
import threading
import time
import glob
import shutil
import sys
import urllib.parse
from datetime import datetime


class danbooru_downloader:
    """化简gallery-dl，只支持Danbooru站点的核心下载功能"""
    
    def __init__(self):
        self.is_downloading = False
        self.status = "就绪"
        self.file_count = 0
        self.download_process = None
        self.download_start_time = None
        
        # 智能检测gallery-dl路径
        self.gallery_dl_path = self._find_gallery_dl()
        

    
    def _find_gallery_dl(self):
        """智能检测gallery-dl路径"""
        # 检查系统PATH
        if shutil.which("gallery-dl"):
            return "gallery-dl"
        
        # 检查Python模块方式
        try:
            import subprocess
            result = subprocess.run(["py", "-m", "gallery_dl", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return "py -m gallery_dl"
        except:
            pass
            
        # 检查常见安装路径
        try:
            username = os.getlogin()
            common_paths = [
                f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\Python*\\Scripts\\gallery-dl.exe",
                f"C:\\Users\\{username}\\AppData\\Roaming\\Python\\Python*\\Scripts\\gallery-dl.exe",
                "C:\\Python*\\Scripts\\gallery-dl.exe",
            ]
            
            for pattern in common_paths:
                matches = glob.glob(pattern)
                if matches:
                    return matches[0]
        except:
            pass
        
        return None
    
    def start_download(self, tag, download_dir, max_count=50):
        """开始下载Danbooru图片"""
        if self.is_downloading:
            return False, "已有下载任务在进行中"
        
        if not self.gallery_dl_path:
            return False, "gallery-dl 未找到，请确保已正确安装"
        
        if not tag or not tag.strip():
            return False, "请输入有效的标签"
        
        if not download_dir:
            return False, "请输入有效的下载目录"
        
        # 创建下载目录（如果不存在）
        try:
            os.makedirs(download_dir, exist_ok=True)
        except Exception as e:
            return False, f"无法创建下载目录: {str(e)}"
        
        # 验证最大下载数量
        try:
            max_count = int(max_count)
            if max_count < 1 or max_count > 1000:
                return False, "最大下载数量必须在1-1000之间"
        except (ValueError, TypeError):
            max_count = 50
        
        # 重置状态
        self.file_count = 0
        self.status = "准备下载..."
        self.download_start_time = datetime.now()
        
        # 启动下载线程
        download_thread = threading.Thread(
            target=self._run_download_process, 
            args=(tag.strip(), download_dir, max_count)
        )
        download_thread.daemon = True
        download_thread.start()
        
        return True, "下载已开始"
    
    def cancel_download(self):
        """取消当前下载"""
        if not self.is_downloading:
            return False, "当前没有正在进行的下载任务"
        
        try:
            if self.download_process and self.download_process.poll() is None:
                # 终止下载进程
                self.download_process.terminate()
                # 等待进程结束，最多等待5秒
                try:
                    self.download_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # 如果进程没有在5秒内结束，强制杀死
                    self.download_process.kill()
                    self.download_process.wait()
                
                self.status = "下载已取消"
                self.is_downloading = False
                self.download_process = None
                return True, "下载已取消"
            else:
                self.is_downloading = False
                self.status = "下载已停止"
                return True, "下载已停止"
        except Exception as e:
            self.is_downloading = False
            self.status = "取消下载时出错"
            return False, f"取消下载时出错: {e}"
    
    def get_status(self):
        """获取当前下载状态"""
        return {
            "is_downloading": self.is_downloading,
            "status": self.status,
            "file_count": self.file_count,
            "gallery_dl_available": self.gallery_dl_path is not None
        }
    
    def _count_downloaded_files(self, directory):
        """统计目录中实际下载的图片文件数量"""
        if not os.path.exists(directory):
            return 0
        
        # 统计常见图片格式文件
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
        count = 0
        
        try:
            for file in os.listdir(directory):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    count += 1
        except Exception:
            return 0
        
        return count
    
    def _run_download_process(self, tag, download_dir, max_count=50):
        """运行gallery-dl下载进程"""
        try:
            self.is_downloading = True
            self.status = "正在下载..."
            
            # 创建标签专用文件夹
            tag_folder = os.path.join(download_dir, tag)
            if not os.path.exists(tag_folder):
                os.makedirs(tag_folder)
            
            # 构建Danbooru URL
            encoded_tag = urllib.parse.quote_plus(tag)
            url = f"https://danbooru.donmai.us/posts?tags={encoded_tag}"
            
            # 构建gallery-dl命令
            if self.gallery_dl_path.startswith("py -m"):
                # 处理Python模块方式调用
                command = [
                    'py', '-m', 'gallery_dl',
                    '--directory', tag_folder,
                    '--write-tags',  # 保存标签信息
                    '--range', f'1-{max_count}',  # 限制下载数量
                    url
                ]
            else:
                # 处理直接可执行文件方式
                command = [
                    self.gallery_dl_path,
                    '--directory', tag_folder,
                    '--write-tags',  # 保存标签信息
                    '--range', f'1-{max_count}',  # 限制下载数量
                    url
                ]
            
            # 在Windows系统中设置环境变量以支持UTF-8
            env = os.environ.copy()
            if sys.platform.startswith('win'):
                env['PYTHONIOENCODING'] = 'utf-8'
                env['LANG'] = 'zh_CN.UTF-8'
            
            # 启动下载进程
            self.download_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                env=env
            )
            
            # 监控下载进程输出
            downloaded_files = 0
            for line in iter(self.download_process.stdout.readline, ''):
                if not self.is_downloading:  # 检查是否被取消
                    break
                    
                line = line.strip()
                if line:
                    # 统计下载的文件数量
                    if 'saved' in line.lower() or 'download' in line.lower():
                        downloaded_files += 1
                        self.file_count = downloaded_files
                        self.status = f"已下载 {downloaded_files} 个文件"
            
            self.download_process.stdout.close()
            return_code = self.download_process.wait()
            
            # 更新最终状态
            if return_code == 0 and self.is_downloading:
                # 统计实际下载的图片文件数量
                actual_count = self._count_downloaded_files(tag_folder)
                self.file_count = actual_count
                self.status = f"下载完成！共获取 {actual_count} 个文件"
            elif not self.is_downloading:
                self.status = "下载已取消"
            else:
                self.status = "下载出错"
            
        except FileNotFoundError:
            self.status = "gallery-dl 未找到"
        except Exception as e:
            self.status = f"下载出错: {str(e)}"
        finally:
            self.is_downloading = False
            self.download_process = None