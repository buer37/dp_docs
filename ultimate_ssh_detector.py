#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终极SSH端口检测工具
全面扫描服务器 103.85.84.239 的SSH端口
"""

import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import subprocess
import os

class UltimateSSHDetector:
    def __init__(self, target_host, timeout=3):
        self.target_host = target_host
        self.timeout = timeout
        self.open_ports = []
        self.ssh_ports = []
        self.all_results = {}
        
    def check_port(self, port):
        """快速检测端口是否开放"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.target_host, port))
                return port, result == 0
        except:
            return port, False
    
    def detailed_port_check(self, port):
        """详细检测端口服务类型"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                sock.connect((self.target_host, port))
                
                # 先尝试接收自动发送的横幅
                banner = ""
                try:
                    sock.settimeout(2)
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                except socket.timeout:
                    pass
                
                # 如果没有自动横幅，尝试发送不同的探测请求
                if not banner:
                    # SSH探测
                    try:
                        sock.send(b'SSH-2.0-Detector\r\n')
                        sock.settimeout(3)
                        response = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                        if 'SSH' in response:
                            return port, 'SSH', response
                        banner = response
                    except:
                        pass
                
                # 判断服务类型
                banner_upper = banner.upper()
                if any(keyword in banner_upper for keyword in ['SSH-', 'OPENSSH', 'DROPBEAR']):
                    return port, 'SSH', banner
                elif 'HTTP' in banner_upper:
                    return port, 'HTTP', banner
                elif 'FTP' in banner_upper:
                    return port, 'FTP', banner
                elif 'TELNET' in banner_upper:
                    return port, 'TELNET', banner
                else:
                    return port, 'Unknown', banner
                    
        except Exception as e:
            return port, 'Error', str(e)
    
    def ping_test(self):
        """测试主机连通性"""
        print("🌐 测试主机连通性...")
        try:
            # Windows ping命令
            result = subprocess.run(['ping', '-n', '1', self.target_host], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ 主机可通过ICMP ping访问")
                return True
            else:
                print("❌ ICMP ping失败，但主机可能仍然在线")
                return False
        except:
            print("⚠️  无法执行ping测试")
            return False
    
    def scan_common_services(self):
        """扫描常见服务以确认主机在线"""
        print("\n🔍 扫描常见服务端口...")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306]
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self.check_port, port): port for port in common_ports}
            
            online_ports = []
            for future in as_completed(futures):
                port, is_open = future.result()
                if is_open:
                    online_ports.append(port)
                    print(f"✅ 端口 {port} 开放")
        
        return online_ports
    
    def comprehensive_ssh_scan(self):
        """全面SSH端口扫描"""
        print(f"\n🔍 开始全面SSH端口扫描 {self.target_host}...")
        print("=" * 70)
        
        # 第一阶段：快速扫描大量端口
        print("阶段1: 快速端口发现...")
        
        # 定义要扫描的端口范围
        port_ranges = [
            range(1, 1025),        # 知名端口
            range(1024, 5000),     # 注册端口
            range(8000, 9000),     # 常用高端口
            range(20000, 25000),   # 高端口范围
            range(49152, 50000),   # 动态端口开始范围
        ]
        
        all_ports_to_scan = []
        for port_range in port_ranges:
            all_ports_to_scan.extend(port_range)
        
        print(f"正在扫描 {len(all_ports_to_scan)} 个端口...")
        
        # 使用多线程快速扫描
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(self.check_port, port): port for port in all_ports_to_scan}
            
            discovered_ports = []
            completed = 0
            total = len(futures)
            
            for future in as_completed(futures):
                port, is_open = future.result()
                completed += 1
                
                if is_open:
                    discovered_ports.append(port)
                    print(f"✅ 发现开放端口: {port}")
                
                # 显示进度
                if completed % 1000 == 0:
                    print(f"进度: {completed}/{total} ({completed/total*100:.1f}%)")
        
        print(f"\n阶段1完成！发现 {len(discovered_ports)} 个开放端口")
        
        # 第二阶段：详细分析开放端口
        if discovered_ports:
            print(f"\n阶段2: 详细分析 {len(discovered_ports)} 个开放端口...")
            
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = {executor.submit(self.detailed_port_check, port): port for port in discovered_ports}
                
                for future in as_completed(futures):
                    port, service_type, info = future.result()
                    
                    self.open_ports.append(port)
                    self.all_results[port] = {'service': service_type, 'info': info}
                    
                    if service_type == 'SSH':
                        self.ssh_ports.append(port)
                        print(f"🎯 SSH服务发现！端口 {port} - {info[:100]}...")
                    else:
                        print(f"📋 端口 {port}: {service_type} - {info[:50]}...")
        
        return self.ssh_ports
    
    def generate_final_report(self):
        """生成最终报告"""
        print("\n" + "=" * 70)
        print("📊 最终扫描报告")
        print("=" * 70)
        print(f"目标主机: {self.target_host}")
        print(f"扫描完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"扫描超时设置: {self.timeout} 秒")
        
        if self.ssh_ports:
            print(f"\n🎯 发现SSH端口: {len(self.ssh_ports)} 个")
            print("=" * 50)
            for port in sorted(self.ssh_ports):
                info = self.all_results[port]['info']
                print(f"端口 {port}")
                print(f"  服务信息: {info}")
                print(f"  连接命令: ssh -p {port} username@{self.target_host}")
                print()
        else:
            print("\n❌ 未发现SSH端口")
            print("\n🔍 可能的原因:")
            print("1. SSH服务未启动")
            print("2. SSH端口被防火墙阻止")
            print("3. SSH服务运行在非标准端口（需要服务器管理员确认）")
            print("4. 服务器配置了端口敲门或其他安全措施")
        
        if self.open_ports:
            other_ports = [p for p in self.open_ports if p not in self.ssh_ports]
            if other_ports:
                print(f"\n📋 其他开放端口: {len(other_ports)} 个")
                print("=" * 50)
                for port in sorted(other_ports)[:10]:  # 只显示前10个
                    service = self.all_results[port]['service']
                    info = self.all_results[port]['info'][:50]
                    print(f"端口 {port}: {service} - {info}")
                
                if len(other_ports) > 10:
                    print(f"... 还有 {len(other_ports) - 10} 个端口")

def main():
    target_host = "103.85.84.239"
    
    print("🚀 终极SSH端口检测工具")
    print("=" * 70)
    print(f"目标主机: {target_host}")
    print("注意：此工具将进行全面扫描，可能需要几分钟时间")
    print("=" * 70)
    
    detector = UltimateSSHDetector(target_host)
    
    # 1. 连通性测试
    detector.ping_test()
    
    # 2. 常见服务扫描
    common_services = detector.scan_common_services()
    
    if not common_services:
        print("⚠️  未发现任何开放端口，主机可能离线或有严格的防火墙设置")
        choice = input("是否仍要继续全面扫描？(y/n): ")
        if choice.lower() != 'y':
            return
    
    # 3. 全面SSH扫描
    ssh_ports = detector.comprehensive_ssh_scan()
    
    # 4. 生成报告
    detector.generate_final_report()
    
    # 5. 提供建议
    if not ssh_ports:
        print("\n💡 下一步建议:")
        print("1. 联系服务器管理员确认SSH配置")
        print("2. 检查服务器防火墙日志")
        print("3. 确认SSH服务状态: systemctl status ssh")
        print("4. 查看SSH配置: cat /etc/ssh/sshd_config")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  扫描被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        sys.exit(1) 