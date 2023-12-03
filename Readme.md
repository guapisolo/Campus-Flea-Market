## Statement

This is an open source project based on [django-ecommerce-project](https://github.com/veryacademy/django-ecommerce-project) development.

这是一个基于 [django-ecommerce-project](https://github.com/veryacademy/django-ecommerce-project) 开发的开源项目。



## Setup

Make sure your python version is <= 3.9.

确保您的 python 版本 <= 3.9。

You must install the necessary packages, call the following command.

您必须安装必要的包，请调用如下指令。

```
pip install -r requirement.txt
```

Once installed, run the program by invoking the following command:

安装完毕后，调用如下指令运行程序：

```
py manage.py runserver
```



## Tips

Here is some tips maybe helpful for you.

### 1. Environment

In order to minimize any unnecessary hassle, we **strongly recommend** that you use python <= 3.9 to install the contents of requirements.txt. It is known that version 3.10 is **not compatible** with the version of the Pillow package in requirements.txt, which can lead to more complex installation issues. For example, if you find that your Django has gone to version 4.0+, please rollback.

We also recommend that you use a python virtual environment manager, such as *anaconda*, for future use.

为了减少不必要的麻烦，我们强烈建议您使用 python <= 3.9 安装 requirements.txt 的内容。已知 3.10 版本并不兼容 requirements.txt 中的 Pillow 包的版本，会导致更加复杂的环境安装问题。例如，如果您发现您的 Django 变成了 4.0+ 版本，请进行回退。

此外，我们建议您使用 python 虚拟环境管理软件，如笔者使用的 anaconda，方便日后的使用

### 2. html comments

The default comment style of html is not recognized by django, it will be converted into a stream of characters and passed to the front-end. The comments that can be recognized by django are:

html 的默认注释方式并不会被 django 识别，会全部转化成字符流传给前端。能够被 django 识别的注释方式是：

```html
{% comment %} your html code {% endcomment %}
```

But obviously, it's a pain in the ass to comment it out that way. If you are programming in vscode, download the django-html plugin. Then, change settings.json to make vscode recognize html files as django-html, so you can easily use the comment shortcut. Here is an example, note that templates is the folder where html is stored.

但显然，这样注释会很麻烦。如果你在使用 vscode 编程，请下载 django-html 插件。接着，修改 settings.json 使得 vscode 识别 html 文件为 django-html，可以便捷的使用注释快捷键了。例子如下，注意 templates 是存放 html 的文件夹

```json
    // Django Extension
    "files.associations": {
        "**/templates/*.html": "django-html",
        "**/templates/**/*.html": "django-html",
    },
```

### 3. Updating data table

When updating columns in data tables, you must make sure you **makemigrations** first, and then **migrate** to update the database.

更新数据表的列时，必须要先 **makemigrations** 再 **migrate** 更新数据库











