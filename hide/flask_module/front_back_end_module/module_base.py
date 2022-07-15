# 程序模型设计
#url(task):
class task:
    class info:
        name = str
    class process:
        root = process.root.table
        branch_dict = dict(branch_name=process.branch.query_list)
        out = [(Case(list, table, db) , out_info)]
    
        # task.info:
        #     .name
        # task.process:
        #     .root = process.root.table  # <2.3.1.1>
        #     .branch_dict = [('branch_name', process.branch.query_list)...]
        #     .out = [(type'list/table/db', out_info)...]
#url(2.3.1.1 输入过程.表查询)
class process:
    class root:
        class table:
            class task_handle:
                task_name = str
                process_name = str

    class table_info:
        class table_chain:
            class db:
                class table:
                    class fields:
                        class base:
                            names = [str]
                            comment = [str]
                            types = [str]
                            names = [str]

            .name = [name...]
            .comment = [name...]
            .type = [name...]
            .key = [name...]
        fields.ext:
            .cond = [op...]
            .select = [bool...]

#url(2.3.1.1 输入过程.表查询)
    process.root.table:
        .task_handle:
            .task_name
            .process_name

        table_info:
            table_chain:
                .db.table
            fields.base:
                .name = [name...]
                .comment = [name...]
                .type = [name...]
                .key = [name...]
            fields.ext:
                .cond = [op...]
                .select = [bool...]

#url(2.3.2 名单查询过程):
    process.branch.query_list:
        .global_name/sub_name
        .root_list = [data...]
        .table_info:
            .table_chain:
                .db.table
            .fields.base
                .name = [name...]
                .comment = [name...]
                .type = [name...]
                .key = [name...]
            .fields.ext
                .cond = [op...]
                .select = [bool...]
