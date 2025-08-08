#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面SSH端口检测工具
针对服务器 103.85.84.239 进行全面的SSH端口扫描
"""

import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import re

class FullSSHScanner:
    def __init__(self, target_host, timeout=5):
        self.target_host = target_host
        self.timeout = timeout
        self.open_ports = []
        self.ssh_ports = []
        self.scan_results = {}
        
    def scan_port_with_banner(self, port):
        """检测端口并尝试获取服务横幅"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.target_host, port))
                
                if result == 0:
                    banner = ""
                    service_type = ""
                    
                    try:
                        # 尝试接收横幅
                        sock.settimeout(3)
                        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                        
                        # 检查是否是SSH服务
                        if self.is_ssh_banner(banner):
                            service_type = "SSH"
                            self.ssh_ports.append(port)
                        elif "HTTP" in banner.upper():
                            service_type = "HTTP"
                        elif "FTP" in banner.upper():
                            service_type = "FTP"
                        elif "SMTP" in banner.upper():
                            service_type = "SMTP"
                        else:
                            service_type = "Unknown"
                            
                    except socket.timeout:
                        # 如果没有自动发送横幅，尝试发送SSH握手
                        try:
                            sock.send(b'SSH-2.0-Scanner\r\n')
                            response = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                            if self.is_ssh_banner(response):
                                service_type = "SSH"
                                banner = response
                                self.ssh_ports.append(port)
                        except:
                            pass
                    
                    self.open_ports.append(port)
                    return port, True, service_type, banner
                else:
                    return port, False, "", ""
                    
        except Exception as e:
            return port, False, "", str(e)
    
    def is_ssh_banner(self, banner):
        """检查横幅是否表明这是SSH服务"""
        if not banner:
            return False
        ssh_indicators = ['SSH-', 'OpenSSH', 'libssh', 'dropbear', 'SSH_']
        return any(indicator in banner for indicator in ssh_indicators)
    
    def scan_extended_ssh_ports(self):
        """扫描扩展的SSH端口列表"""
        extended_ssh_ports = [
            # 常用SSH端口
            22, 222, 1022, 2022, 2222, 2200, 8022,
            # 更多可能的SSH端口
            1022, 1122, 1222, 1322, 1422, 1522, 1622, 1722, 1822, 1922,
            2020, 2121, 2200, 2201, 2202, 2203, 2204, 2205, 2220, 2221,
            2323, 2424, 2525, 2626, 2727, 2828, 2929, 3030, 3131, 3232,
            4040, 4141, 4242, 4343, 4444, 5050, 5151, 5252, 5353, 5454,
            6060, 6161, 6262, 6363, 6464, 7070, 7171, 7272, 7373, 7474,
            8080, 8181, 8282, 8383, 8484, 8822, 8823, 8888, 8889, 9090,
            9191, 9292, 9393, 9494, 9595, 9696, 9797, 9898, 9999, 9922,
            10022, 10122, 10222, 11022, 11122, 11222, 12022, 12122, 12222,
            20022, 20122, 20222, 22000, 22022, 22122, 22200, 22222, 22322,
            30022, 30122, 30222, 33022, 33122, 33222, 40022, 44022, 50022,
            # 非标准但可能的端口
            60022, 65022, 65222
        ]
        
        print(f"🔍 扫描扩展SSH端口列表（{len(extended_ssh_ports)} 个端口）...")
        print("=" * 70)
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_port = {executor.submit(self.scan_port_with_banner, port): port 
                            for port in extended_ssh_ports}
            
            for future in as_completed(future_to_port):
                port, is_open, service_type, banner = future.result()
                
                if is_open:
                    self.scan_results[port] = {
                        'service': service_type,
                        'banner': banner
                    }
                    
                    if service_type == "SSH":
                        print(f"🎯 SSH端口 {port} 发现！ - {banner[:100]}...")
                    else:
                        print(f"✅ 端口 {port} 开放 ({service_type})")
                        
        return self.ssh_ports
    
    def scan_sequential_ranges(self):
        """按范围顺序扫描，优先检查可能的SSH端口范围"""
        ranges_to_scan = [
            (1, 100),       # 特权端口
            (1000, 1100),   # 用户端口开始
            (2000, 2100),   # 常用SSH替代端口
            (8000, 8100),   # 高位常用端口
            (9000, 9100),   # 高位常用端口
            (10000, 10100), # 五位数端口
            (20000, 20100), # 高位端口
            (22000, 22100), # SSH相关端口
        ]
        
        for start, end in ranges_to_scan:
            print(f"\n🔍 扫描端口范围 {start}-{end}...")
            found_ssh = False
            
            with ThreadPoolExecutor(max_workers=30) as executor:
                future_to_port = {executor.submit(self.scan_port_with_banner, port): port 
                                for port in range(start, end + 1)}
                
                for future in as_completed(future_to_port):
                    port, is_open, service_type, banner = future.result()
                    
                    if is_open:
                        self.scan_results[port] = {
                            'service': service_type,
                            'banner': banner
                        }
                        
                        if service_type == "SSH":
                            print(f"🎯 SSH端口 {port} 发现！ - {banner[:100]}...")
                            found_ssh = True
                        else:
                            print(f"✅ 端口 {port} 开放 ({service_type})")
            
            # 如果在某个范围内找到了SSH端口，可以选择停止扫描
            if found_ssh:
                user_choice = input(f"\n在范围 {start}-{end} 中发现SSH端口，是否继续扫描其他范围？(y/n): ")
                if user_choice.lower() != 'y':
                    break
                    
        return self.ssh_ports
    
    def generate_detailed_report(self):
        """生成详细扫描报告"""
        print("\n" + "=" * 70)
        print("📊 详细扫描报告")
        print("=" * 70)
        print(f"目标主机: {self.target_host}")
        print(f"扫描时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"超时设置: {self.timeout} 秒")
        print(f"总计扫描端口数: {len(self.scan_results)}")
        
        if self.ssh_ports:
            print(f"\n🎯 发现 {len(self.ssh_ports)} 个SSH端口:")
            for port in sorted(self.ssh_ports):
                banner = self.scan_results[port]['banner']
                print(f"   端口 {port} - SSH服务")
                print(f"      横幅: {banner}")
                print(f"      连接命令: ssh -p {port} username@{self.target_host}")
                print()
        else:
            print("\n❌ 未发现SSH端口")
        
        # 显示其他开放端口
        other_ports = [port for port in self.open_ports if port not in self.ssh_ports]
        if other_ports:
            print(f"\n📋 其他开放端口 ({len(other_ports)} 个):")
            for port in sorted(other_ports):
                service = self.scan_results[port]['service']
                banner = self.scan_results[port]['banner'][:50] + "..." if len(self.scan_results[port]['banner']) > 50 else self.scan_results[port]['banner']
                print(f"   端口 {port} - {service} - {banner}")

def main():
    target_host = "103.85.84.239"
    
    print("🚀 全面SSH端口扫描工具")
    print("=" * 70)
    print(f"目标主机: {target_host}")
    print(f"注意：此工具将进行全面扫描以找到SSH端口")
    print("=" * 70)
    
    scanner = FullSSHScanner(target_host, timeout=5)
    
    # 1. 先扫描扩展的SSH端口列表
    print("阶段1: 扫描扩展SSH端口列表")
    ssh_ports = scanner.scan_extended_ssh_ports()
    
    if ssh_ports:
        print(f"\n🎉 在扩展列表中发现 {len(ssh_ports)} 个SSH端口！")
        scanner.generate_detailed_report()
        return
    
    # 2. 如果没找到，进行范围扫描
    print("\n阶段2: 按范围扫描端口")
    print("未在常用SSH端口中找到服务，开始范围扫描...")
    
    ssh_ports = scanner.scan_sequential_ranges()
    
    # 3. 生成最终报告
    scanner.generate_detailed_report()
    
    if not ssh_ports:
        print("\n💡 建议:")
        print("1. 确认SSH服务是否已启动")
        print("2. 检查防火墙设置")
        print("3. 确认SSH配置文件中的端口设置")
        print("4. 可能SSH端口在非常用范围内，建议联系服务器管理员")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  扫描被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        sys.exit(1) 