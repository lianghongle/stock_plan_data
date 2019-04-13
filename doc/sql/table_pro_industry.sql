-- auto-generated definition
create table pro_stock_industry (
    id           INT(10) auto_increment
        primary key,
    industry     VARCHAR(10) null,
    created_date DATE null,
    constraint stock_industry_name_uindex
        unique (industry)
) COMMENT='所属行业';

