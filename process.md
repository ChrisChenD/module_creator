
# web服务
0 全局搜索
1 一个字段 > 获取 key序列 [db].[tb].[key]
2 选择多个字段, 获取字段集select  [col1,col2,col3..]

# 代码- 特殊类
3 default 对象, raw 对象:
    default对象, 自动过滤 dataStatus
    raw对象, 全 column
4 auto_cond 对象, dataStatus!=3

# 代码- 模型
集成MySQL查询, 能够使用 代码-框架


# 代码- 框架
df1 = A(chunk=1000, chunk_limit=1).join(B
    ).reknow(B2, chunk=1000).join(C
    ).reknow(B3, chunk=1000).join(D
    ).reknow(D2, chunk=1000).find(
        E(chunk=1000).find('sptid', spt_list).list('companys')
    ).groupby(col, max/min/avg
    ).explode(lambda row:new_row
    ).setcol('col', lambda row:F.find('sptid', [row['1'],row['2']]).list['companys'])
    ).rename(col_dict
    ).df
    # 在所有过程执行的时候, 先进行一轮字段检查, reknow 要检查字段是否存在

Excel(name).save({
    name1:df1,
    name2:df2
})

# 任务命名
收到任务:
    1 回复任务命名:
    按照时间戳 + 客户 + 版本

    输出 task_时间戳.xlsx


### 进度:

今天:
0 搞定python环境
    非常 clear. 整合进我们的demo系统中
1 制作mysql模型
    >>    
2 完成web框架
3 完成符合框架代码的业务代码

调整:
今天:
完成快速开发---
实现代码版本的快速开发 , 不在web上实现
-----------------------------------------
非常美, 非常牛叉！
我需要休息一会

# 1 搜索
0 全局搜索  >> 单文件搜索
1 一个字段 > 获取 key序列 [db].[tb].[key]     >> path
2 选择多个字段, 获取字段集select  [col1,col2,col3..]    >> _cols
3 快速搜索字段, _scan

# 2 计算和表示  >>>> 这个等等
3 default 对象, raw 对象:
    default对象, 自动过滤 dataStatus
    raw对象, 全 column
4 auto_cond 对象, dataStatus!=3

# 3 框架实现, 引擎隔离    >> 
1 把 ReadSample 实现为 返回 [_sample,]
    把这个东西命名为Engine
    <!-- ReadMysql -->
2 我们解析所有的配置
    得到一个表, 通过我们的标准框架, 生成配置, 调用引擎
    引擎的使用功能, 要求和 ReadMysql 一致
3 支持流, 块, join, find
    ...

# 4 使用框架完成业务
    ...



周一:
1 实现代码框架

https://github.com/ChrisChenD/module_creator

最好能有一个 ftp 服务, 同步数据
----------------------------------------
>>
1 环境搭建
2 验证需求