# 第七组文档说明

注：第一次运行程序耗费时间会很大！

## 1 实现功能
本项目实现了一个基于特定语料库的搜索引擎，其支持的功能有：

- 布尔查询
- 通配查询
- 拼写校正
- 短语查询
- 同义词扩展
- 建立倒排索引和向量空间模型
- 索引压缩
- 词典索引
- TopK排序
- 在浏览器中显式地反馈搜索结构

## 2 使用说明

### 2.1 环境配置
<!--FIXME-->
- 运行环境
    |||
    |----|----|
    |操作系统|Windows10<br/>MacOS|
    |python|python3|
    |使用工具|pip|
    
- 安装库

  项目使用了WordNet开源库，首先需要安装WordNet才能开始运行程序。

  首先安装nltk库：

  ```shell
  pip install nltk
  ```

  进入python命令行中，输入下列命令：

  ```python
  import nltk
  import ssl
  
  try:
  	_create_unverified_https_context = ssl._create_unverified_context
  except AttributeError:
  	pass
  else:
  	ssl._create_default_https_context = _create_unverified_https_context
  
  nltk.download('wordnet')
  nltk.download('omw-1.4')
  ```

- 运行时若发生以下错误：
<img src="https://github.com/wys0912/WebSearch/blob/master/1.png" />
则打开`path/numpy/lib/format.py`（VSCode中`Ctrl+Click`/`Cmd+Click`可以直接跳转），将以下注释：
<img src="https://github.com/wys0912/WebSearch/blob/master/2.png" />

### 2.2 程序运行
- 进入到项目文件夹下
    ```shell
    $ cd WebSearch
    ```
- 终端输入
    ```shell
    $ python -m http.server
    ```
    启动服务器
- 新建终端，输入
    ```shell
    $ python main.py
    ```
    此时开始运行搜索引擎程序并进行搜索引擎初始化
- 搜索引擎初始化完成后共有四种选项：
    - 输入`1`，进行普通查询
    - 输入`2`，使用topK查询
    - 输入`3`，开/关向量排序
    - 输入`4`，退出程序



## 3 测试数据

### 3.1 倒排索引向量空间模型
```
查询模式选择1
education
```
查询语句如下所示：

<img src="C:\Users\jiong\Desktop\图片\5C5593F5-50F6-417c-9420-3D2FBE57D002.png" alt="5C5593F5-50F6-417c-9420-3D2FBE57D002" style="zoom:50%;" />

将按照education的倒排索引表顺序返回结果（包含了同义词扩展的结果）

查询结果如下图所示：

<img src="https://raw.githubusercontent.com/GarF1eldGo/PictureBed/main/Pictures/image-20220610174105122.png" alt="image-20220610174105122" style="zoom:50%;" />

因为我们·计算向量时采用了高IDF策略，所以忽略了高频词education，因此我们以低频词input为例。

首先选择 3 打开向量排序功能

然后选择1 进行查询

```
查询模式选择 3
查询模式选择 1
input
```

<img src="C:\Users\jiong\AppData\Roaming\Typora\typora-user-images\image-20220613171115001.png" alt="image-20220613171115001" style="zoom: 80%;" />

此时返回的便是向量相似度排序的结果：

<img src="C:\Users\jiong\Desktop\图片\input.png" alt="input" style="zoom:50%;" />



为了之后的测试速度，我们选择选择3关闭排序进行之后的计算

### 3.2 布尔查询

```
查询模式选择1
AND: government AND policy
OR:  billion OR million
NOT: NOT fall AND rise
```
查询语句如下所示：

![image-20220610172952561](https://raw.githubusercontent.com/GarF1eldGo/PictureBed/main/Pictures/image-20220610172952561.png)

查询结果如下图所示：

<img src="https://raw.githubusercontent.com/GarF1eldGo/PictureBed/main/Pictures/image-20220610172929020.png" alt="image-20220610172929020" style="zoom:50%;" />



### 3.3 通配查询

```
查询模式选择1
*put
technol*
*formatia*
```
查询语句如下所示：

![image-20220610173827183](https://raw.githubusercontent.com/GarF1eldGo/PictureBed/main/Pictures/image-20220610173827183.png)

查询结果如下所示：

<img src="https://raw.githubusercontent.com/GarF1eldGo/PictureBed/main/Pictures/image-20220610173804742.png" alt="image-20220610173804742" style="zoom:50%;" />

### 3.4 短语查询

```
查询模式选择1
information technology
```
查询语句如下所示：

![image-20220610173911679](https://raw.githubusercontent.com/GarF1eldGo/PictureBed/main/Pictures/image-20220610173911679.png)

查询结果如下所示：

<img src="https://raw.githubusercontent.com/GarF1eldGo/PictureBed/main/Pictures/image-20220610173851497.png" alt="image-20220610173851497" style="zoom:50%;" />

### 3.5 拼写校正

```
查询模式选择1
kindom
```
查询语句如下所示：

![image-20220610174033834](https://raw.githubusercontent.com/GarF1eldGo/PictureBed/main/Pictures/image-20220610174033834.png)

查询结果如下所示：

<img src="https://raw.githubusercontent.com/GarF1eldGo/PictureBed/main/Pictures/image-20220610173956145.png" alt="image-20220610173956145" style="zoom:50%;" />



### 3.6 同义词查询

```
查询模式选择1
education
```

查询语句如下所示：

![image-20220610174116866](https://raw.githubusercontent.com/GarF1eldGo/PictureBed/main/Pictures/image-20220610174116866.png)

查询结果如下所示：

<img src="https://raw.githubusercontent.com/GarF1eldGo/PictureBed/main/Pictures/image-20220610174105122.png" alt="image-20220610174105122" style="zoom:50%;" />



## 4 小组分工

|成员|分工|
|----|----|
|王越嵩|布尔查询 通配查询 拼写校正|
|邓承克|倒排索引 向量空间模型 短语查询 同义词扩展|
|李炯|TopK查询 索引压缩 词典索引|
