#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH端口检测工具
用于检测指定服务器的SSH服务端口
"""

import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

class SSHPortScanner:
    def __init__(self, target_host, timeout=3):
        self.target_host = target_host
        self.timeout = timeout
        self.open_ports = []
        self.closed_ports = []
        
    def scan_port(self, port):
        """检测单个端口是否开放"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.target_host, port))
                if result == 0:
                    # 尝试获取SSH横幅信息
                    try:
                        sock.send(b'SSH-2.0-Scanner\r\n')
                        banner = sock.recv(1024).decode('utf-8', errors='ignore')
                        return port, True, banner.strip()
                    except:
                        return port, True, "连接成功但无法获取横幅"
                else:
                    return port, False, "端口关闭"
        except socket.timeout:
            return port, False, "连接超时"
        except Exception as e:
            return port, False, f"连接错误: {str(e)}"
    
    def scan_common_ssh_ports(self):
        """扫描常用SSH端口"""
        common_ssh_ports = [
            22,     # 默认SSH端口
            2022,   # 常用替代端口
            2222,   # 常用替代端口
            2200,   # 常用替代端口
            8022,   # 常用替代端口
            22000,  # 常用替代端口
            10022,  # 常用替代端口
            1022,   # 常用替代端口
            222,    # 常用替代端口
            2020,   # 常用替代端口
            2121,   # 常用替代端口
            8822,   # 常用替代端口
            9922,   # 常用替代端口
        ]
        
        print(f"🔍 开始扫描 {self.target_host} 的常用SSH端口...")
        print("=" * 60)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_port = {executor.submit(self.scan_port, port): port for port in common_ssh_ports}
            
            for future in as_completed(future_to_port):
                port, is_open, info = future.result()
                if is_open:
                    self.open_ports.append(port)
                    print(f"✅ 端口 {port} 开放！ - {info}")
                else:
                    self.closed_ports.append(port)
                    print(f"❌ 端口 {port} 关闭 - {info}")
        
        return self.open_ports
    
    def scan_port_range(self, start_port, end_port):
        """扫描指定端口范围"""
        print(f"\n🔍 扫描端口范围 {start_port}-{end_port}...")
        print("=" * 60)
        
        ports_to_scan = range(start_port, end_port + 1)
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_port = {executor.submit(self.scan_port, port): port for port in ports_to_scan}
            
            for future in as_completed(future_to_port):
                port, is_open, info = future.result()
                if is_open:
                    self.open_ports.append(port)
                    print(f"✅ 端口 {port} 开放！ - {info}")
                    
                    # 如果找到开放端口，检查是否是SSH服务
                    if self.is_ssh_service(port):
                        print(f"🎯 发现SSH服务在端口 {port}！")
    
    def is_ssh_service(self, port):
        """检查端口是否运行SSH服务"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                sock.connect((self.target_host, port))
                sock.send(b'SSH-2.0-Scanner\r\n')
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                return 'SSH' in response.upper()
        except:
            return False
    
    def check_host_connectivity(self):
        """检查主机连通性"""
        print(f"🌐 检查主机 {self.target_host} 的连通性...")
        
        # 尝试连接常见的Web端口来检查主机是否在线
        common_ports = [80, 443, 21, 25, 53, 110, 993, 995, 3389, 8080, 8443]
        
        for port in common_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(2)
                    result = sock.connect_ex((self.target_host, port))
                    if result == 0:
                        print(f"✅ 主机在线！端口 {port} 开放")
                        return True
            except:
                continue
        
        print("⚠️  主机可能离线或防火墙阻止了连接")
        return False
    
    def generate_report(self):
        """生成扫描报告"""
        print("\n" + "=" * 60)
        print("📊 扫描报告")
        print("=" * 60)
        print(f"目标主机: {self.target_host}")
        print(f"扫描时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"超时设置: {self.timeout} 秒")
        
        if self.open_ports:
            print(f"\n✅ 发现 {len(self.open_ports)} 个开放端口:")
            for port in sorted(self.open_ports):
                ssh_status = "🎯 SSH服务" if self.is_ssh_service(port) else "🔍 其他服务"
                print(f"   端口 {port} - {ssh_status}")
        else:
            print("\n❌ 未发现开放端口")
        
        print(f"\n❌ 关闭的端口数量: {len(self.closed_ports)}")

def main():
    target_host = "103.85.84.239"
    
    print("🚀 SSH端口扫描工具")
    print("=" * 60)
    print(f"目标主机: {target_host}")
    print("=" * 60)
    
    scanner = SSHPortScanner(target_host, timeout=3)
    
    # 1. 检查主机连通性
    if not scanner.check_host_connectivity():
        print("⚠️  继续进行SSH端口扫描...")
    
    print()
    
    # 2. 扫描常用SSH端口
    open_ssh_ports = scanner.scan_common_ssh_ports()
    
    if not open_ssh_ports:
        print("\n🔍 常用SSH端口未发现开放端口，开始扫描更广泛的端口范围...")
        
        # 3. 扫描更广泛的端口范围
        print("\n扫描1-1024端口范围...")
        scanner.scan_port_range(1, 1024)
        
        if not scanner.open_ports:
            print("\n扫描1024-65535端口范围（这可能需要较长时间）...")
            user_input = input("是否继续扫描全部端口？(y/n): ")
            if user_input.lower() == 'y':
                scanner.scan_port_range(1024, 65535)
    
    # 4. 生成报告
    scanner.generate_report()
    
    # 5. 提供连接建议
    if scanner.open_ports:
        print("\n💡 连接建议:")
        for port in sorted(scanner.open_ports):
            if scanner.is_ssh_service(port):
                print(f"   ssh -p {port} username@{target_host}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  扫描被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        sys.exit(1) 