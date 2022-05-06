# 

> 1 使用一个py.class 产生：
    1.1 py 模型
    1.2 js 模型
        1.2.1 view
        1.2.2 module
        1.2.3 control
            这个控制不表达如何控制, 只把用户的控制信息传递给后端

> py.class:
    > m 数据, 类的定义
        m.class.
            实例的初始化(每个对象都是一个类/数组类)
            同结构不同位置的对象, 应该有不同的类名字, 继承自同一个类
        m.init
            init obj
    > v 与数据的初始化有关
        1 最好嵌套
        2   
        3 
    > c 控制
        1 每个对象都有一个独立的名字            +++++++
            所有对象通用类, 初始化自动产生 id
        2 当对象被点击/按下回车之后, 把事件发送给后端
            id + 参数
    
> 怎么产生view 函数?

> 先产生模型
    >> 产生成功
> 拆解 view
    >> 现在去掉一切的封装, 我们直接在
        def v() 里面手写所有的 return (dom)

> 关联 event
    > 把每个可点击、输入 的组件，都必须独立封装，有编号
        > 这需要我们不满足于 def v() 里面的手写内容, 而是需要让组件化的(dom)加入到v里面
        > (dom).id 要进行注册
        > (dom).id 

> compo
    > 所有的compo 都是可以关联event的
    > 如果没有event, 没有必要作为compo
    > 带参数 compo 需要把参数传递给后端, 我们暂时只支持，把compo内部的数据传递出去
    >       那么如何传递compo内部的参数, 就是我们需要的重点

    > compo:
        1 数据 字面传入()
        2 id 自动分配
        3 挂载的行为: 需要在v 里面绑定
        compo.button(
            #id=auto,
            data='self.functor_list',
            event=dict(
                OnClick=root.plan.add_functor(ReadMysql())
            )
        )
            1 这里 onClick 就是 onClick={self.call(self.idx, 'onClick')}
            2 这里的 root.xxx 是执行函数, 用来注册到事件里面
                所有事件应该和module关联

# summery
> 多任务程序 ++++
    我们考虑用户打开多个 plan
    我们必须让所有的节点都能够访问，当前plan(module.root)

    plan = get(plan_name, default_plan_maker())
    set(plan_name, plan)

> id_maker:
    用来给所有的 compo + 类, 注册key
    属于某个plan
    > 每个module = root{
        id_map, 
        data = plan
    }
> event
    1 对于前端发送的回调:
        1 obj.idx > 找到后端 obj
        2 method = method_name
        3 params = dict()
    2 如果注册的回调, 被修改了怎么办？
        (仍然用 idx:)
        约定一个修改规则:
        1 回调访问 确定的对象
            不会被修改
        2 回调访问 不确定的对象(可有可无)
            回调访问子对象
        3 回调修改 而非访问不确定对象
            回调访问确定对象, 由该对象提供标准方法
        4 其他特殊要求，先不实现

> compo:
    用来封装 event+view 的库
    这个产生和编译, compo.js





# 上班时间做什么
因为效率低下，有创造力的工作不在此时做，


> 用新框架实现一个基本页面:
    1 name/f_list/new_f_list/op
        >> 今天搞定/上午搞定

    2 new delete functors
    3 save/load
>
上午已经做通 整个流程
    >> 需要把 key-id 加上
    . 今天
-----------------------------------------------------
我们需要一个 compo 但是compo到底是什么:
1 问题:
    类方法:
        m, v
        我们根据类方法, 产生 m, v
    对象方法:
        产生 idx, clsName
    
    1 我们根据类的声明, 产生 js
    2 v 怎么和compo 关联
        根据 m 的初始化类型, 产生 v
    3 因此, m, v 都是静态变量
        >> 去修改成静态变量


