import subprocess
import time
#from PIL import Image
import PIL.Image
#from io import BytesIO


class Adbtools:
    def __init__(self, adb_path, device_ip, port=5555, mac = None):
        """
        初始化方法，设置 ADB 路径和设备信息
        :param adb_path: ADB 命令的完整路径（例如 /usr/bin/adb 或 adb.exe）
        :param device_ip: 设备的 IP 地址（如果是 USB 连接，可设置为 'localhost'）
        :param port: 设备的 ADB 端口，默认是 5555
        """
        self.adb_path = adb_path
        self.device_ip = device_ip
        self.mac = mac
        self.port = port
        self.screen_width = 1080
        self.screen_height = 1920
        self.dpi = 180
        self.device = None  # Initialize self.device as None

        # 连接到设备
        #print(self.connect_device())

        print(f"设备分辨率: {self.screen_width}x{self.screen_height}")

    def run_adb_command(self, command):
        """
        执行 ADB 命令并返回输出
        :param command: ADB 命令
        :return: 命令输出
        """
        try:
            if self.device_ip == 'localhost':
                result = subprocess.run(
                    [self.adb_path, '-s' , f'{self.mac}' ] + command,
                    capture_output=True,
                    text=True,
                    check=True
                )
            else:
                result = subprocess.run(
                    [self.adb_path, '-s', f'{self.device_ip}:{self.port}'] + command,
                    capture_output=True,
                    text=True,
                    check=True
                )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"ADB 命令执行失败: {e}")
            return None

    def run_adb_command_bin(self, command):
        # 运行 adb 命令，捕获输出
        """
        执行 ADB 命令并返回二进制输出
        :param command: ADB 命令
        :return: 命令输出（二进制数据）
        """
        try:
            if self.device_ip == 'localhost':
                # 执行 adb 命令并捕获二进制输出
                result = subprocess.run(
                    [self.adb_path, '-s', f'{self.mac}'] + command,
                    capture_output=True,
                    check=True,
                    text=False  # 不进行文本解码，返回二进制数据
                )
            else:
                # 执行 adb 命令并捕获二进制输出
                result = subprocess.run(
                    [self.adb_path, '-s', f'{self.device_ip}:{self.port}'] + command,
                    capture_output=True,
                    check=True,
                    text=False  # 不进行文本解码，返回二进制数据
                )
            return result.stdout  # 返回二进制输出
        except subprocess.CalledProcessError as e:
            print(f"Error executing adb command: {e}")
            return None
        
    def adb_change_device_resolution(self):
        """
        更改设备的分辨率和 DPI
        """
        # 获取设备的屏幕分辨率和 DPI
        screen_info = self.run_adb_command(['shell', 'wm size {self.screen_width}x{self.screen_height} && wm density {self.dpi}'])
        print(screen_info)
        #screen_info = screen_info.split()
        #self.screen_width, self.screen_height = map(int, screen_info[2].split('x'))
        #self.dpi = int(screen_info[5])
        #print(f"设备分辨率: {self.screen_width}x{self.screen_height}")
        #print(f"设备 DPI: {self.dpi}")


        
        
    def adb_click_raw(self, x, y, duration=0):
        """
        执行屏幕点击操作（不缩放坐标）
        :param x: 点击的 x 坐标
        :param y: 点击的 y 坐标
        :param duration: 按住的时间，单位为秒
        """
        self.run_adb_command(['shell', f'input tap {x} {y}'])
        if duration != 0:
            time.sleep(duration)

    def adb_swipe_raw(self, x1, y1, x2, y2, duration):
        """
        执行滑动操作（不缩放坐标）
        :param x1: 起始点 x 坐标
        :param y1: 起始点 y 坐标
        :param x2: 结束点 x 坐标
        :param y2: 结束点 y 坐标
        :param duration: 滑动持续时间，单位为毫秒
        """
        self.run_adb_command(['shell', f'input swipe {x1} {y1} {x2} {y2} {duration}'])

    def adb_click(self, x, y, duration=0):
        """
        执行屏幕点击操作（缩放坐标）
        :param x: 点击的 x 坐标0-1 范围）
        :param y: 点击的 y 坐标0-1 范围）
        :param duration: 按住的时间，单位为秒
        """
        self.run_adb_command(['shell', f'input tap {int(x * self.screen_width)} {int(y * self.screen_height)}'])
        if duration != 0:
            time.sleep(duration)

    def adb_swipe(self, x1, y1, x2, y2, duration):
        """
        执行滑动操作（缩放坐标）
        :param x1: 起始点 x 坐标0-1 范围）
        :param y1: 起始点 y 坐标0-1 范围）
        :param x2: 结束点 x 坐标0-1 范围）
        :param y2: 结束点 y 坐标0-1 范围）
        :param duration: 滑动持续时间，单位为毫秒
        """
        self.run_adb_command([
            'shell',
            f'input swipe {int(x1 * self.screen_width)} {int(y1 * self.screen_height)} '
            f'{int(x2 * self.screen_width)} {int(y2 * self.screen_height)} {duration}'
        ])
    
    def adb_input_text(self, text):
        """
        输入文本
        :param text: 要输入的文本
        """
        self.run_adb_command(['shell', f'input text {text}'])
    
    def adb_keyevent(self, keycode):
        """
        发送按键事件
        :param keycode: 键值
        """
        self.run_adb_command(['shell', f'input keyevent {keycode}'])

    def adb_screencap_raw(self):
        # 获取截图的二进制数据
        img_data = self.run_adb_command_bin(['shell', 'screencap'])
        img_data = img_data.replace(b'\r\n', b'\n') # 将 Windows 格式的换行符替换为 Unix 格式
        width = int.from_bytes(img_data[0:4], "little")
        height = int.from_bytes(img_data[4:8], "little")
        pixel_format = int.from_bytes(img_data[8:12], "little")
        print(width, height, pixel_format)
        # 确保像素格式为 RGBA_8888
        assert pixel_format == 1, "unsupported pixel format: %s" % pixel_format
        # 使用 PIL 解析原始图像数据
        img = PIL.Image.frombuffer(
            "RGBA", (width, height), img_data[12:], "raw", "RGBX", 0, 1
            ).convert("RGBA")
        return img
    
    def get_uixml_via_stdout(self):
        """
        获取屏幕UI结构（XML），不保存到本地文件，直接从设备读取并返回 XML 字符串（已清理）
        :return: XML 字符串内容，或 None
        """
        command = ['shell', 'sh', '-c',
                '"uiautomator dump /sdcard/ui.xml && cat /sdcard/ui.xml && rm /sdcard/ui.xml"']
        
        result = self.run_adb_command_bin(command)
        
        if result is not None:
            try:
                xml_str = result.decode('utf-8', errors='ignore')
                # 清理前缀信息，只保留从 '<?xml' 开始的部分
                xml_start = xml_str.find('<?xml')
                if xml_start != -1:
                    return xml_str[xml_start:].strip()
                else:
                    print("Warning: XML header not found in ADB output.")
                    return None
            except UnicodeDecodeError as e:
                print(f"Decode error: {e}")
                return None
        else:
            return None


    
    def adb_read_xml(self, path):
        xml_data = self.run_adb_command(['shell', f"su  -c 'cat {path}'"])
        return xml_data
    
    def qidongapp(self, package_name = 'jp.pokemon.pokemontcgp' ,activity_name = 'com.unity3d.player.UnityPlayerActivity'):
         # 应用包名
        #activity_name = 'com.unity3d.player.UnityPlayerActivity'  # 主活动类名
        #Adbtools(host, port).connect()
        self.run_adb_command(['shell', f'am start -n {package_name}/{activity_name}'])  # 启动应用
        print(f"启动 {package_name} 成功")
    
    def guanbiapp(self,package_name = 'jp.pokemon.pokemontcgp'):
        self.run_adb_command(['shell', f'am force-stop {package_name}'])

    def delet_file(self,path):
        self.run_adb_command(['shell', f"su -c 'rm -r  {path}'"])
        #self.device.shell("su -c \'rm -r  path\'")
        #Adbtools(host, port).shell("su -c 'rm -r  /data/data/jp.pokemon.pokemontcgp/shared_prefs/deviceAccount:.xml'")
        
    def HelloWorld(self):
        print("Hello World")
        return "Hello World"
    
