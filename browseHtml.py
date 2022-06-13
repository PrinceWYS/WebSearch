#coding:utf-8
import os
import platform
import webbrowser
from threading import Thread
# from http.server import test,SimpleHTTPRequestHandler



def openHtml(docNameList, runTime, score = None):
    if platform.system()=='Windows':
        message = """
<html>
<head lang="zh">
<style>
.first{
    font-size : 25px;
    color : black;
}
.box {
    font-size : 25px;
    color :black;
    }
.box .box1 {
    font-size : 15px;
    color : grey;
    position : relative;
    left : 50px;
    }
</style>
</head>
<body>
""" 
    else:
        message = """
<html>
<head lang="zh">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style>
.first{
    font-size : 25px;
    color : black;
}
.box {
    font-size : 25px;
    color :black;
    }
.box .box1 {
    font-size : 15px;
    color : grey;
    position : relative;
    left : 50px;
    }
</style>
</head>
<body>
""" 
    # 打印文字信息
    if len(docNameList) == 0:
        message += """
        <div class="first">
        没有搜索到相关文件！
        </div>
        """
    else:
        message += """
        <div class="first">
        搜索到了%s个文件
        </div>
        """ %(str(len(docNameList)))
    message += """
        <div class="first">
        查询用时%.3fs
        </div>
        <br>
    """ %float(runTime)

    message += '<br>'
    for i in range(len(docNameList)): # 读取文件的内容
        curPath =  os.path.abspath(os.path.dirname(__file__))  # 当前目录
        fileName = 'Reuters/'+str(docNameList[i])+'.html'
        fileName = os.path.join(curPath, fileName)
        f = open(fileName,'r',encoding='unicode_escape')  # 打开文件
        docMessage = ""
        count = 0
        # 只显示前5行
        for line in f:
            docMessage += line + '<br>'
            count += 1
            if count > 5:
                break
        if score is not None:
            basicMessage = """
            <div class="box">
                <div style="display:inline;">  <a href = %s>%s</a> </div>
                <div style="display:inline;color:#f0cb47;margin-left:300px">%.4f</div>
                <div class="box1"> 
                    <p>%s</p> 
                </div>
            </div>
            """%('../Reuters/'+str(docNameList[i])+'.html',str(docNameList[i])+'.html', score[i], docMessage)

            message += basicMessage # 添加进html文件中
        else:
            basicMessage = """
            <div class="box">
                <a href = %s>%s</a>
                <div class="box1"> 
                    <p>%s</p> 
                </div>
            </div>
            """%('../Reuters/'+str(docNameList[i])+'.html',str(docNameList[i])+'.html', docMessage)

            message += basicMessage # 添加进html文件中

    # html文档结尾
    message += """
    </body>
    </html>
    """

    #命名生成的html
    htmlFile = "test.html" 
    curPath =  os.path.abspath(os.path.dirname(__file__))  # 当前目录
    fileName = os.path.join(curPath, 'src', htmlFile)

    f = open(fileName,'w')  # 打开文件

    f.write(message)  # 写入文件
    
    f.close()  # 关闭文件
    
    # webbrowser.open('http://localhost:8000/'+'WebSearch/'+htmlFile)  # 在浏览器打开文件
    # curPath =  os.path.abspath(os.path.dirname(__file__))  # 当前目录
    # fileName = 'Reuters/'+str(docNameList[i])+'.html'
    # fileName = os.path.join(curPath, fileName)
    webbrowser.open('http://localhost:8000/src/'+htmlFile)  # 在浏览器打开文件


# def startWebServer():
#     '''
#     开启本地服务器
#     '''
#     Thread(target=test, kwargs={'HandlerClass': SimpleHTTPRequestHandler}).start()  # 启动本地服务器
