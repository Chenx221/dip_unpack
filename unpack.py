import struct
import os

def unpack_with_signature(file_path, output_dir="extracted"):
    with open(file_path, 'rb') as f:
        data = f.read()

    offset = 0
    file_entries = []

    # 扫描索引区
    print("开始扫描索引...")
    while offset + 12 < len(data):
        if data[offset:offset+3] != b'\x00\x00\x00':
            print(f"[!] 索引区结束 @ {hex(offset)}，发现数据特征: {data[offset:offset+4].hex().upper()}")
            break
            
        # 读取头：sig_type, size, name_len
        sig_type, size, name_len = struct.unpack(">III", data[offset:offset+12])
        name_offset = offset + 12
        name = data[name_offset : name_offset + name_len].decode('utf-8', errors='ignore').strip('\x00')
        
        file_entries.append({"name": name, "size": size, "type": sig_type})
        
        offset += 12 + name_len

    # 提取数据
    data_ptr = offset
    print(f"\n开始提取数据，起始点: {hex(data_ptr)}")
    
    for entry in file_entries:
        name = entry['name']
        size = entry['size']
        sig_type = entry['type']
        
        # 文件夹条目 (0x03)
        if sig_type == 0x03:
            continue
            
        file_payload = data[data_ptr : data_ptr + size]
        
        out_path = os.path.join(output_dir, name)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        
        with open(out_path, 'wb') as out_f:
            out_f.write(file_payload)
            
        print(f"成功提取: {name} | 大小: {size} 字节 | 类型: {hex(sig_type)} | 偏移: {hex(data_ptr)}")
        
        data_ptr += size

if __name__ == '__main__':
    input_path = input('输入待解包文件路径: ').strip()
    unpack_with_signature(input_path)
    print('解包完成！')