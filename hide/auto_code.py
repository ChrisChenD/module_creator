#!/usr/bin/env python3
import pandas 
from pandaUtil_mysql_chain import mysql_chain
from pandaUtil_append import chunk_append,readMysql

def f_root():
    "readMysql"
    # 工商股东表
    # 公司编码,公司名称,股东编码,股东类别编码,股东名称（冗余）,认缴金额（明细）,实缴金额（明细）,认缴的出资额,持股比例,数据来源,同步标识
    for chunk in readMysql(mysql_chain.db_aliyun)[
        "sy_cd_ms_sh_gs_shlist_new",
        "compCode,compName,shId,shTypeCode,shName,capital,actualCapital,investAmount,holdRatio,infoSource,sourceId",
        "cond_list,isValid=1,dataStatus!=3",
    ].df_chunks:
        yield chunk
def f1(chunk):
    "colAppend"
    # 公司基本信息表
    # 公司编码,公司名称,英文名,公司新名称编码,公司别名,公司历史名称,上级机构编码,省份简称,法人ID,法人姓名（冗余字段）,法人类型,工商注册码,统一社会信用代码,组织机构代码,组织机构批准单位,公司类型,机构类型,经营范围,注册状态,注册地址,注册资本（工商公示）,注册资本金额（分）,注册资本币种,实收资本金额（分）,实收资本币种,登记机关,成立日期,核准日期,营业期限开始日期,营业期限终止日期,注销原因,注销日期,吊销日期,吊销原因/吊销凭证,公司评分,国民经济行业编码,公司纬度,公司经度,行政区划码,职工参保人数,邮箱列表,电话,微信公众号,公司logo,解析完成时间,同步标识
    root_key,append_key = ,
    new_chunk = chunk_append(chunk, append_info=[
        mysql_chain.db_aliyun,
        "sy_cd_ms_base_gs_comp_info_new",
        "compCode,compName,compEngName,compNewCode,aliasName,historyNames,parentCode,stateAbbr,legalPersonId,legalPersonName,legalPersonType,regNum,creditCode,orgCode,orgAprvUnit,compType,orgType,businessScope,regStatus,regAddr,regCapitalAm,regCapital,currencyCode,actualCapital,actCapCurrency,regOrg,estiblishDate,aprvPublDt,startDate,endDate,cancelReason,cancelDate,revokeDate,revokeReason,compScore,industryId,lat,lng,areaCode,ssfCount,emails,phones,wechatPubNum,logo,parseTime,sourceId",
        "cond_list,dataStatus!=3",
    ], key=[
        root_key,append_key
    ], key_type=str)
    return new_chunk
def f_save(df):
    "saveExcel"
    print('save.df', df)

dfs = []
for i, chunk in enumerate(f_root()):
    for proc in ['f1']:
        chunk = proc(chunk)
    dfs.append(chunk)
    if i >= 2:
        break
df = pandas.concat(dfs, axis=0)
f_save(df)
# ok!
# file = "task/out2_1.xlsx"
# print('write', file)
# with pandas.ExcelWriter(file) as writer:
#     # hp1.add_sheet(writer)
#     df.to_excel(writer, sheet_name='商机明细表-常量表', index=False)
# {'name': 't12', 'functor_list': [<module.readMysql object at 0x7f6f3ee0f1c0>, <module.colAppend object at 0x7f6f3ee0f340>, <module.saveExcel object at 0x7f6f3ee0e6a0>], 'new_functor_list': [{'name': 'readMysql'}, {'name': 'colAppend'}, {'name': 'saveExcel'}], 'op': []}