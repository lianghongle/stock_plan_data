-- auto-generated definition
create table pro_stock_monthly (
    id           INT(10) auto_increment
        primary key,
    ts_code      VARCHAR(10)    null comment '股票代码',
    trade_date   DATE null comment '交易日期',
    open         DECIMAL(10, 2) null comment '月开盘价',
    high         DECIMAL(10, 2) null comment '月最高价',
    low          DECIMAL(10, 2) null comment '月最低价',
    close        DECIMAL(10, 2) null comment '月收盘价',
    pre_close    DECIMAL(10, 2) null comment '上一月收盘价',
    `change`     DECIMAL(10, 2) null comment '涨跌额',
    pct_chg      DECIMAL(10, 4) null comment '涨跌幅 （未复权，如果是复权请用 通用行情接口 ）',
    vol          DECIMAL(14, 2) null comment '成交量 （手）',
    amount       DECIMAL(16, 3) null comment '成交额 （千元）',
    created_date DATE null
) COMMENT='月线行情';