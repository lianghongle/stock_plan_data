create table stock_basic (
    id               INT(10) auto_increment
        primary key,
    code             VARCHAR(6)    not null comment '代码',
    name             VARCHAR(15)   null comment '名称',
    industry         VARCHAR(10)   null comment '所属行业',
    area             VARCHAR(10)   null comment '地区',
    pe               DOUBLE(22, 0) null comment '市盈率',
    outstanding      DOUBLE(22, 0) null comment '流通股本(亿)',
    totals           DOUBLE(22, 0) null comment '总股本(亿)',
    totalAssets      DOUBLE(22, 0) null comment '总资产(万)',
    liquidAssets     DOUBLE(22, 0) null comment '流动资产',
    fixedAssets      DOUBLE(22, 0) null comment '固定资产',
    reserved         DOUBLE(22, 0) null comment '公积金',
    reservedPerShare DOUBLE(22, 0) null comment '每股公积金',
    esp              DOUBLE(22, 0) null comment '每股收益',
    bvps             DOUBLE(22, 0) null comment '每股净资',
    pb               DOUBLE(22, 0) null comment '市净率',
    timeToMarket     INT(10)       null comment '上市日期',
    undp             DOUBLE(22, 0) null comment '未分利润',
    perundp          DOUBLE(22, 0) null comment '每股未分配',
    rev              DOUBLE(22, 0) null comment '收入同比(%)',
    profit           DOUBLE(22, 0) null comment '利润同比(%)',
    gpr              DOUBLE(22, 0) null comment '毛利率(%)',
    npr              DOUBLE(22, 0) null comment '净利润率(%)',
    holders          INT(10)       null comment '股东人数',
    created_date     DATE null
) COMMENT='股票基础信息数据';



