-- auto-generated definition
create table pro_stock_company (
    id           INT(10) auto_increment
        primary key,
    ts_code      VARCHAR(10)  null comment '股票代码',
    exchange     VARCHAR(5)   null comment '交易所代码 ，SSE上交所 SZSE深交所',
    chairman     VARCHAR(50)  null comment '法人代表',
    manager      VARCHAR(50)  null comment '总经理',
    secretary    VARCHAR(50)  null comment '董秘',
    reg_capital  FLOAT(12, 0) null comment '注册资本',
    setup_date   DATE null comment '注册日期',
    province     VARCHAR(10)  null comment '所在省份',
    city         VARCHAR(10)  null comment '所在城市',
    introduction   VARCHAR(2000)   null comment '公司介绍',
    website      VARCHAR(100) null comment '公司主页',
    email        VARCHAR(100)  null comment '电子邮件',
    office         VARCHAR(200)   null comment '办公室',
    business_scope VARCHAR(5000)   null comment '经营范围',
    employees    INT(10)      null comment '员工人数',
    main_business  VARCHAR(2000)   null comment '主要业务及产品',
    created_date DATE null
) COMMENT='上市公司基本信息';
