1.需要安装python2.7 
		另外需要安装BeautifulSoup和selenium
		1）安装BeautifulSoup：使用python安装目录下 \Python27\Scripts 中easy_install安装
			运行命令  easy_install BeautifulSoup
		2)安装selenium
			a）解压phantomjs-2.1.1-windows 到D盘根目录（或者需要修改announcement.py中process函数的代码：browser=webdriver.PhantomJS(executable_path='D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')成对应路径）
			b）运行命令  easy_install selenium
2.在triggers.txt中配置关键字，关键字每行一个
3.下载pdf文件存放在当前日期的文件夹中
4.日期文件夹下会自动生成records.txt文件，用于记录已经下载文件，避免再次运行时重复下载