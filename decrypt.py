def decrypt_dip(input_path, output_path, key_file):
    with open(key_file, 'rb') as f:
        key_table = f.read()
    with open(input_path, 'rb') as f:
        data = bytearray(f.read())

    n4 = 4
    decrypted_data = bytearray()
    for i in range(4, len(data)):
        decrypted_byte = data[i] ^ key_table[n4 & 0x3FFFF]
        decrypted_data.append(decrypted_byte)
        n4 += 1

    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

if __name__ == '__main__':
    input_path = input('输入待解密文件路径: ').strip()
    output_path = input('输入输出文件路径: ').strip()
    decrypt_dip(input_path, output_path, "key.bin")
    print('解密完成！')
