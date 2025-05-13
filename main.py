import random as rd
from tkinter import messagebox as tk

def send(char):
    """加密单个字符"""
    ascii_val = ord(char)
    # 计算最大允许密钥
    max_key = 255 - ascii_val
    if max_key < 1:
        raise ValueError(f"字符 '{char}' (ASCII {ascii_val}) 超出可加密范围")
    # 生成1到min(9, max_key)的密钥
    key = rd.randint(1, min(9, max_key))
    encrypted = hex(ascii_val + key)[2:].zfill(2)
    return f"{encrypted}{key}"

def decrypt_group(group):
    """解密单个3位密文组"""
    if len(group) != 3:
        raise ValueError("无效的密文组长度")
    encrypted_part = group[:2]
    key = int(group[2])
    decrypted = int(encrypted_part, 16) - key
    if decrypted < 16 or decrypted > 255:
        raise ValueError(f"无效ASCII值: {decrypted}")
    return chr(decrypted)

# 主程序循环
while True:
    try:
        print("\n" + "="*20)
        print("1. 加密文本")
        print("2. 解密文本")
        print("3. 退出程序")
        choice = input("请选择操作 (1/2/3): ").strip()

        if choice == '1':
            plaintext = input("请输入要加密的文本: ").strip()
            
            # 增强输入验证
            if not plaintext:
                tk.showerror("错误", "输入不能为空")
                continue
                
            invalid_chars = {}
            for c in plaintext:
                ascii_val = ord(c)
                if ascii_val < 16 or ascii_val > 255:
                    invalid_chars[c] = ascii_val
                elif ascii_val > 255 - 1:  # 检查最大允许密钥1
                    invalid_chars[c] = f"{c} (ASCII {ascii_val}) 无法生成有效密钥"
            
            if invalid_chars:
                msg = "包含无效字符:\n" + "\n".join(
                    [f"{k}: {v}" if isinstance(v, int) else f"{k} {v}" 
                     for k,v in invalid_chars.items()])
                tk.showerror("错误", msg)
                continue
            
            # 执行加密
            try:
                cipher = [send(c) for c in plaintext]
                print("加密结果:", ''.join(cipher))
            except ValueError as e:
                tk.showerror("加密错误", str(e))

        elif choice == '2':
            ciphertext = input("请输入要解密的密文: ").strip()
            
            # 格式验证
            if not ciphertext:
                tk.showerror("错误", "输入不能为空")
                continue
            if len(ciphertext) % 3 != 0:
                tk.showerror("错误", f"密文长度应为3的倍数，当前长度: {len(ciphertext)}")
                continue
            if not all(c in "0123456789abcdef" for c in ciphertext[::3]) or \
               not all(c.isdigit() for c in ciphertext[2::3]):
                tk.showerror("错误", "密文格式非法")
                continue
            
            # 执行解密
            try:
                plain = []
                for i in range(0, len(ciphertext), 3):
                    group = ciphertext[i:i+3]
                    plain.append(decrypt_group(group))
                
                result = ''.join(plain)
                # 二次验证
                if any(ord(c) < 16 or ord(c) > 255 for c in result):
                    raise ValueError("包含无效ASCII字符")
                print("解密结果:", result)
            except Exception as e:
                tk.showerror("解密错误", f"无效密文: {str(e)}")

        elif choice == '3':
            print("程序退出...")
            break

        else:
            tk.showerror("错误", "无效选项，请重新选择")

    except Exception as e:
        tk.showerror("系统异常", f"程序异常: {str(e)}")