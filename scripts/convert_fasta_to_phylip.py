import sys

# 获取命令行参数指定的 FASTA 文件
fasta_file = sys.argv[1]

# 存储序列 ID 的列表
seq_ids = []
# 存储序列数据的字典，键为序列 ID，值为序列字符串
seq_data = {}
# 当前处理的序列 ID 和临时存储序列行的列表
seq_id, seq_buffer = None, []

# 打开 FASTA 文件并逐行处理
with open(fasta_file, "r") as file:
    for line in file:
        line = line.strip()
        if line.startswith(">"):
            if seq_buffer:
                seq_data[seq_id] = ''.join(seq_buffer)
                seq_ids.append(seq_id)
            seq_id = line[1:]
            seq_buffer = []
        else:
            seq_buffer.append(line)

# 处理最后一个序列
seq_data[seq_id] = ''.join(seq_buffer)
seq_ids.append(seq_id)
# 获取最后一个序列的长度
seq_len = len(seq_data[seq_id])

# 输出序列数量和序列长度
print(len(seq_data), len(seq_data[seq_id]))

# 输出序列信息，每行输出 50 个字符，每 10 个字符一组
for seq_id in seq_ids:
    seq = seq_data[seq_id]
    print(f"{seq_id[:10]:<10}", end="")
    for i in range(0, min(50, seq_len), 10):
        print(f" {seq[i:i + 10]}", end="")
    print()

# 如果序列长度超过 50 个字符，继续输出后续部分，每行输出 60 个字符，每 10 个字符一组
if seq_len > 50:
    for j in range(50, seq_len, 60):
        print()
        for seq_id in seq_ids:
            seq = seq_data[seq_id]
            for i in range(j, min(j + 60, seq_len), 10):
                print(f"{' ' if i > j else ''}{seq[i:i + 10]}", end="")
            print()
