-- auto-generated definition
create table pro_stock_basic (
    id           INT(10) auto_increment
        primary key,
    ts_code      VARCHAR(10)  null comment 'TS代码',
    symbol       VARCHAR(6)   not null comment '股票代码',
    name         VARCHAR(15)  null comment '股票名称',
    area         VARCHAR(10)  null comment '所在地域',
    industry     VARCHAR(10)  null comment '所属行业',
    fullname     VARCHAR(100) null comment '股票全称',
    enname       VARCHAR(100) null comment '英文全称',
    market       VARCHAR(10)  null comment '市场类型 （主板/中小板/创业板）',
    exchange     VARCHAR(10)  null comment '交易所代码',
    curr_type    VARCHAR(10)  null comment '交易货币',
    list_status  VARCHAR(1)   null comment '上市状态： L上市 D退市 P暂停上市',
    list_date    DATE null comment '上市日期',
    delist_date  DATE null comment '退市日期',
    is_hs        VARCHAR(1)   null comment '是否沪深港通标的，N否 H沪股通 S深股通',
    created_date DATE null
);

