import os
import shutil
import platform 


# # 删除src文件夹及其包含的文件
# shutil.rmtree('src')
# 删除部分文件
syst = platform.system()
if syst=='Windows':
    if os.path.exists('src\posIndex.txt'):
        os.remove('src\posIndex.txt')
        print('成功删除文件：src/posIndex.txt')
    if os.path.exists('src\invertIndexFile.npy'):
        os.remove('src\invertIndexFile.npy')
        print('成功删除文件：src/invertIndexFile.npy')
else:
    if os.path.exists('src/posIndex.txt'):
        os.remove('src/posIndex.txt')
        print('成功删除文件：src/posIndex.txt')
    if os.path.exists('src/invertIndexFile.npy'):
        os.remove('src/invertIndexFile.npy')
        print('成功删除文件：src/invertIndexFile.npy')

# 创建src文件夹
if not os.path.exists('src'):
    os.mkdir('src')