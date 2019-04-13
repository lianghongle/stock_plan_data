-- auto-generated definition
create table stock_area (
    id           INT(10) auto_increment
        primary key,
    area         VARCHAR(10) null,
    created_date DATE null,
    constraint stock_area_name_uindex
        unique (area)
) COMMENT='所在地域';

