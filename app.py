# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import sys
import threading
import webbrowser
from danbooru_downloader import danbooru_downloader
from post_processor import PostProcessor

# 设置控制台编码
if sys.platform.startswith('win'):
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'Chinese_China.65001')
        except:
            pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'danbooru-simple-downloader'

# 全局实例
downloader = danbooru_downloader()
post_processor = PostProcessor()

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def start_download():
    """开始下载"""
    try:
        data = request.get_json()
        tag = data.get('tag', '').strip()
        download_dir = data.get('download_dir', '').strip()
        max_count = data.get('max_count', 50)
        
        if not tag:
            return jsonify({
                'success': False,
                'message': '请输入标签'
            })
        
        if not download_dir:
            return jsonify({
                'success': False,
                'message': '请输入下载目录'
            })
        
        # 验证最大下载数量
        try:
            max_count = int(max_count)
            if max_count < 1 or max_count > 1000:
                return jsonify({
                    'success': False,
                    'message': '最大下载数量必须在1-1000之间'
                })
        except (ValueError, TypeError):
            max_count = 50
        
        success, message = downloader.start_download(tag, download_dir, max_count)
        
        return jsonify({
            'success': success,
            'message': message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'请求处理出错: {str(e)}'
        })

@app.route('/api/status')
def get_status():
    """获取下载状态"""
    try:
        status = downloader.get_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({
            'is_downloading': False,
            'status': f'获取状态出错: {str(e)}',
            'file_count': 0,
            'gallery_dl_available': False
        })

@app.route('/api/cancel', methods=['POST'])
def cancel_download():
    """取消下载"""
    try:
        success, message = downloader.cancel_download()
        
        return jsonify({
            'success': success,
            'message': message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'取消下载出错: {str(e)}'
        })

@app.route('/api/manual_tag_process', methods=['POST'])
def manual_tag_process():
    """手动标签处理"""
    try:
        data = request.get_json()
        folder_path = data.get('folder_path', '').strip()
        remove_tags = data.get('remove_tags', [])
        remove_containing = data.get('remove_containing', [])
        add_tags = data.get('add_tags', [])
        
        if not folder_path:
            return jsonify({
                'success': False,
                'message': '请指定文件夹路径'
            })
        
        # 处理标签列表（去除空字符串）
        remove_tags = [tag.strip() for tag in remove_tags if tag.strip()]
        remove_containing = [tag.strip() for tag in remove_containing if tag.strip()]
        add_tags = [tag.strip() for tag in add_tags if tag.strip()]
        
        result = post_processor.manual_tag_process(
            folder_path, remove_tags, remove_containing, add_tags
        )
        
        success = result.success
        message = result.message
        
        return jsonify({
            'success': success,
            'message': message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'手动标签处理出错: {str(e)}'
        })

@app.route('/api/auto_standardize', methods=['POST'])
def auto_standardize():
    """自动标准化标签（无需用户确认）"""
    try:
        data = request.get_json()
        folder_path = data.get('folder_path', '').strip()
        
        if not folder_path:
            return jsonify({
                'success': False,
                'message': '请指定文件夹路径'
            })
        
        # 扫描文件
        file_infos, unpaired_files = post_processor.scan_and_match_files(folder_path)
        
        if not file_infos:
            return jsonify({
                'success': False,
                'message': '未找到可处理的文件'
            })
        
        # 执行自动标准化
        result = post_processor.standardize_tags(folder_path, file_infos)
        
        success = result.success
        message = result.message
        
        return jsonify({
            'success': success,
            'message': message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'自动标准化出错: {str(e)}'
        })


def open_browser(port):
    """延迟打开浏览器"""
    import time
    time.sleep(1.5)  # 等待服务器启动
    try:
        webbrowser.open(f'http://localhost:{port}')
    except:
        pass  # 忽略浏览器打开失败

if __name__ == '__main__':
    port = 5678
    
    print(f"\n🌐 FastDanbooruDataset已启动")
    print(f"📍 访问地址: http://localhost:{port}")
    print(f"🛑 按 Ctrl+C 停止服务器\n")
    
    # 自动打开浏览器
    browser_thread = threading.Thread(target=open_browser, args=(port,))
    browser_thread.daemon = True
    browser_thread.start()
    
    # 启动Flask应用
    app.run(debug=False, host='0.0.0.0', port=port)