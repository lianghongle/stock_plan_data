-- auto-generated definition
create table pro_stock_weekly (
    id           INT(10) auto_increment
        primary key,
    ts_code      VARCHAR(10)    null comment '股票代码',
    trade_date   DATE null comment '交易日期',
    open         DECIMAL(10, 2) null comment '周开盘价',
    high         DECIMAL(10, 2) null comment '周最高价',
    low          DECIMAL(10, 2) null comment '周最低价',
    close        DECIMAL(10, 2) null comment '周收盘价',
    pre_close    DECIMAL(10, 2) null comment '上一周收盘价',
    `change`     DECIMAL(10, 2) null comment '涨跌额',
    pct_chg      DECIMAL(10, 4) null comment '涨跌幅 （未复权，如果是复权请用 通用行情接口 ）',
    vol          DECIMAL(10, 2) null comment '成交量 （手）',
    amount       DECIMAL(12, 3) null comment '成交额 （千元）',
    created_date DATE null
)COMMENT='周线行情';