#!/usr/bin/env python3 

from big_file.mysql_pymodule import mysql

# 所在市为厦门市的
# 需求1：已获得C轮以上投资的企业清单，包括企业名称、注册资本、实缴资本、法人代表、联系方式、注册地址、投资人

# 导出名单为：
#   融资新闻表 中融资轮次为C,C+,D,D+,E,E+,F,F+,G轮的融资方，
#   并且地理信息表中cityCode=350200的企业。
#   导出项为融资新闻表（融资方、投资方）、工商概况表（注册资本、实缴资本、法人代表、联系方式、注册地址）。

# 10分钟分析明白: 21.53
# 0 建立任务, 给任务分配一个名字
#       哪个微信群？什么时候?
#       
# 1 资源
#    确认, 所指涉的所有表， 是哪一个表
# 2 判断资源的数据规模
#    这个应该自动化. 或者忽略
# 3 资源join方式
#       显而易见, 用 compName



# 融资新闻表
A = mysql.db152.sy_cd_me_news_oth_financing.companyName()
        # _path = "mysql.db152.sy_cd_me_news_oth_financing"
        # _cname = "融资新闻表"
        # _sample = {'id': 1, 'incidentTitle': ' 朋友圈裂变新秀，「立问人脉」获数百万元天使轮融资', 'companyName': '立问人脉', 'companyFullName': '深圳上时科技有限公司', 'investmentName': '[{"orgname":"远望资本","identity":"3853"}]', 'investmentAmount': '数百万人民币', 'investmentTurn': '天使轮', 'financeDate': '2018-08-22', 'introduction': None, 'industryName': '企业服务', 'incidentId': 124125, 'companyId': 119524318, 'address': '深圳市南山区南山街道海德二道向南海德大厦608室', 'province': '广东省', 'city': '深圳市', 'district': '南山区', 'dataStatus': 1, 'createTime': '2020-06-15 18:36:07', 'modifyTime': '2020-06-15 18:36:09'}
        # _cols = "id,incidentTitle,companyName,companyFullName,investmentName,investmentAmount,investmentTurn,financeDate,introduction,industryName,incidentId,companyId,address,province,city,district,dataStatus,createTime,modifyTime"

# 基本概况表 (地理信息)
B = mysql.db_aliyun.sy_cd_ms_base_comp_geo_new.compName()
        #     _path = "mysql.db_aliyun.sy_cd_ms_base_comp_geo_new"
        #     _cname = "工商公司地理位置信息表"
        #     _sample = {'id': 1, 'compCode': 10000000505, 'compName': '新绛县计划生育协会', 'address': None, 'country': '中国', 'provinceName': '山西省', 'provinceCode': '140000', 'cityName': '临汾市', 'cityCode': '141000', 'district': '安泽县', 'districtCode': '141026', 'location': None, 'sourceId': 10000000505, 'dataStatus': 2, 'createTime': '2021-06-24 18:36:11', 'modifyTime': '2022-01-26 15:23:31'}
        #     _cols = "id,compCode,compName,address,country,provinceName,provinceCode,cityName,cityCode,district,districtCode,location,sourceId,dataStatus,createTime,modifyTime"
# 工商概况表
C = mysql.db_aliyun.sy_cd_ms_base_gs_comp_info_new.compName()
        # _path = "mysql.db_aliyun.sy_cd_ms_base_gs_comp_info_new"
        # _cname = "公司基本信息表"
        # _sample = {'id': 1, 'compCode': 2944200260, 'compName': '深圳市华什贸易有限公司', 'compEngName': None, 'compNewCode': None, 'aliasName': '华什贸易', 'historyNames': None, 'parentCode': None, 'stateAbbr': 'gd', 'legalPersonId': 2204795877, 'legalPersonName': '邓鹏', 'legalPersonType': 1, 'regNum': '440301117579451', 'creditCode': '91440300MA5DLQQW0F', 'orgCode': 'MA5DLQQW0', 'orgAprvUnit': None, 'compType': '有限责任公司(自然人独资)', 'orgType': 1, 'businessScope': '一般经营项目是：珠宝、服装、服饰、日用品、电子产品、数码产品的销售；国内贸易,从事货物及技术的进出口业务，许可经营项目是：', 'regStatus': 2, 'regAddr': '深圳市福田区福田街道嘉汇新城汇商中心1201', 'regCapitalAm': '50.000000万人民币', 'regCapital': 50000000.0, 'currencyCode': '人民币', 'actualCapital': nan, 'actCapCurrency': '人民币', 'regOrg': '福田局', 'estiblishDate': datetime.date(2016, 9, 27), 'aprvPublDt': datetime.date(2016, 9, 27), 'startDate': datetime.date(2016, 9, 27), 'endDate': datetime.date(2026, 9, 22), 'cancelReason': None, 'cancelDate': NaT, 'revokeDate': '2019-06-21 00:00:00', 'revokeReason': None, 'compScore': '5335', 'industryId': '521', 'lat': 114.087376701622, 'lng': 22.5446541292061, 'areaCode': 440304, 'ssfCount': nan, 'emails': None, 'phones': None, 'wechatPubNum': None, 'logo': '/logo/lll/6922ea65071d7a48d38e68989074a8b4.png@!f_200x200', 'parseTime': '2020-12-31 11:52:44', 'sourceId': 100019548, 'dataStatus': 2, 'createTime': '2021-05-06 19:58:58', 'modifyTime': '2021-06-17 15:31:39'}
        # _cols = "id,compCode,compName,compEngName,compNewCode,aliasName,historyNames,parentCode,stateAbbr,legalPersonId,legalPersonName,legalPersonType,regNum,creditCode,orgCode,orgAprvUnit,compType,orgType,businessScope,regStatus,regAddr,regCapitalAm,regCapital,currencyCode,actualCapital,actCapCurrency,regOrg,estiblishDate,aprvPublDt,startDate,endDate,cancelReason,cancelDate,revokeDate,revokeReason,compScore,industryId,lat,lng,areaCode,ssfCount,emails,phones,wechatPubNum,logo,parseTime,sourceId,dataStatus,createTime,modifyTime"

# 我们糟糕一点, 直接问


# 导出名单为：
#   融资新闻表(A) 中融资轮次为C,C+,D,D+,E,E+,F,F+,G轮的融资方，
#   并且地理信息表(B)中cityCode=350200的企业。
#   导出项为融资新闻表（融资方、投资方）、 工商概况表 (C)（注册资本、实缴资本、法人代表、联系方式、注册地址）。
investmentTurn_list = "C,C+,D,D+,E,E+,F,F+,G".split(",")
A = A(
        cond=f'investmentTurn in {tuple(investmentTurn_list)}',
        select=f'investmentName,companyName'
)
B = B(
        cond='cityCode=350200',
        select='cityCode'
)
C = C(
        select='',
)

# 关于工商概况表: 确认一下应该用哪个字段
# 1 注册资本应该是那个字段?
# 注册资本: [注册资本(工商公示)]regCapitalAm<varchar(50)>: mysql.db_aliyun.sy_cd_ms_base_gs_comp_info_new.regCapitalAm
# 注册资本: [注册资本金额(分)]regCapital<decimal(25?4)>: mysql.db_aliyun.sy_cd_ms_base_gs_comp_info_new.regCapital
# 注册资本: [注册资本币种]currencyCode<varchar(255)>: mysql.db_aliyun.sy_cd_ms_base_gs_comp_info_new.currencyCode
# 2 法人代表
# 法人: [法人ID]legalPersonId<bigint(20)>: mysql.db_aliyun.sy_cd_ms_base_gs_comp_info_new.legalPersonId
# 法人: [法人姓名(冗余字段)]legalPersonName<varchar(125)>: mysql.db_aliyun.sy_cd_ms_base_gs_comp_info_new.legalPersonName
# 3 实缴资本
# 资本: [注册资本(工商公示)]regCapitalAm<varchar(50)>: mysql.db_aliyun.sy_cd_ms_base_gs_comp_info_new.regCapitalAm
# 资本: [注册资本金额(分)]regCapital<decimal(25?4)>: mysql.db_aliyun.sy_cd_ms_base_gs_comp_info_new.regCapital
# 4 联系方式


# 实缴资本、法人代表、联系方式 分别对应哪个字段？
# 没有找到直接的名字

# （注册资本、实缴资本、法人代表、联系方式、注册地址）。
C._scan(*'注册资本、实缴资本、法人代表、联系方式、注册地址'.split('、'))
# C._scan(*'资本,法人'.split(','))
exit()
df1 = A(chunk=1000, chunk_n=1).join(B
).join(C
).df

Excel(__file__).save({
        'sheet1':df1
})
# A._scan('融资方')
# 融资方用哪个字段?
# ['[融资方简称]companyName<varchar(256)>: mysql.db152.sy_cd_me_news_oth_financing.companyName', '[融资方公司全称]companyFullName<varchar(256)>: mysql.db152.sy_cd_me_news_oth_financing.companyFullName']
# 投资方
# A._scan('投资方')
# ['[投资方投资方的JSONArray串，其中orgname(投资方名称)；identity(投资人id)]investmentName<text>: mysql.db152.sy_cd_me_news_oth_financing.investmentName']



# join, find, to_sheet(sheet_name)
# Excel(name).save(
#   sheet1, sheet2, sheet3
# )



# A(size=1000).join(B
#     ).reknow(B2, size=1000).join(C
#     ).reknow(B3, size=1000).join(D
#     ).reknow(D2, size=1000).find(
#         E(size=1000).find('sptid', spt_list).list('companys')
#     ).groupby(col, max/min/avg
#     ).explode(lambda row:new_row
#     ).setcol('col', lambda row:F.find('sptid', [row['1'],row['2']]).list['companys'])
#     ).rename(col_dict
#     ).add_sheet('sheet_name', Excelname=__file__)
#     # 在所有过程执行的时候, 先进行一轮字段检查, reknow 要检查字段是否存在


# 工商概况表的几个输出应该怎么取数？
# #1 注册资本
# [注册资本] result number: 3
# 注册资本: [注册资本(工商公示)]regCapitalAm<varchar(50)>
# 注册资本: [注册资本金额(分)]regCapital<decimal(25?4)>
# 注册资本: [注册资本币种]currencyCode<varchar(255)>
# #2 实缴资本
# [资本] result number: 5
# 资本: [注册资本(工商公示)]regCapitalAm<varchar(50)>
# 资本: [注册资本金额(分)]regCapital<decimal(25?4)>
# 资本: [注册资本币种]currencyCode<varchar(255)>
# 资本: [实收资本金额(分)]actualCapital<decimal(25?4)>
# 资本: [实收资本币种]actCapCurrency<varchar(255)>
# #3 法人代表
# [法人] result number: 3
# 法人: [法人ID]legalPersonId<bigint(20)>
# 法人: [法人姓名(冗余字段)]legalPersonName<varchar(125)>
# 法人: [法人类型]legalPersonType<int(4)>
# #4 联系方式



# #5 注册地址 ok
# [注册地址] result number: 1
# 注册地址: [注册地址]regAddr<varchar(255)>

