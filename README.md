## shell命令行下词典，支持中英文互相查询

#### 底层通过有道开放平台调用有道词典查询接口，并缓存至本地MySql，再次查询时不需要重新调用接口

--

#### 依赖包
##### peewee：Python下轻量级orm框架
+ 文档地址:http://docs.peewee-orm.com/en/latest/

##### requests：http请求包
+ 文档地址:http://docs.python-requests.org/en/master/

--

#### 有道API开放平台:http://ai.youdao.com/docs/api.s
--

使用方法
1. git clone https://github.com/lanxing/shell_dic.git
2. 给文件赋予可执行权限 chmod +x dic.py
3. 修改 db = MySQLDatabase('mydb', user='root')，数据库的schema及用户名，如果有密码则加上password参数
4. 修改main()函数，先调用createTable函数创建表，然后执行executeDic函数

