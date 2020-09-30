# danbo-backend

这是蛋博项目的后端代码库，主项目请见[蛋博](https://github.com/chty627/Software-Engineering-Project---Danbo)。

## 目录

-   [安装](#安装)
-   [使用](#使用)
-   [注意事项](#注意事项)
-   [贡献者](#贡献者)
-   [协议](#协议)

## 安装

* 安装python：版本在3.6及以上
* 安装django：版本在2.2及以上（建议3.0），pip3 install django==3.0

## 使用

* 运行指令

  python3 manage.py makemigrations

  python3 manage.py migrate

  python3 manage.py runserver

## 注意事项

-   **使用你自己的分支**
    -    **不要**随便提交或者`pull request`到 `master`分支！开发者只能在自己的分支上进行开发和测试。
-   **管理员会检查你的提交** 
    -   如果你想把你的代码合并到`master`分支，你可以从你的分支发起 `pull request` 。 **管理员会决定是否通过你的代码，所以请调试好再提交。**
-   **保持代码库干净** 
    -   **不要用**  `add .` ！你需要仔细检查你所提交的代码并一个个`add`，或者你需要检查你提交的代码列表是否没有冗余。
    -   **不要**添加 `\venv`或者`\.vscode`。这会导致代码库冗余。你可以修改 `.gitignore`来忽略不必要的文件或文件夹。
-   **勤更看板，勤写文档**
    -   所有成员**必须**每周更新一次[主仓库](https://github.com/chty627/Software-Engineering-Project---Danbo)Zenhub看板，首先给自己添加一个Issue然后根据进度往后移，在Review/QA阶段申请`pull request`，通过后即可设置为Done。
    -   所有成员**必须**对写的类、函数进行注释，注释风格请见[谷歌代码规范](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/#comments)，使用VSCode的Python Docstring Generator插件可以很容易生成。

## 贡献者

[@ryanhe312](https://github.com/ryanhe312) [@x54-729](https://github.com/x54-729) [@ZeayW](https://github.com/ZeayW)

## 协议

MIT License
