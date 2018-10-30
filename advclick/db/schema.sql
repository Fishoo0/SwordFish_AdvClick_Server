drop table if exists User;
drop table if exists Click;
drop table if exists Youmeng;
drop table if exists Log;

create table User (
    id integer primary key autoincrement,
    time text not null,

    name text not null,
    password text not null,
    token text,

    cover text,
    gender integer,
    birth text,
    age text,
    location text,
    about text,
    telephone text,

    is_admin integer default 0,

    im_qq text not null,
    alipay text not null,
    alipay_name text,

    prime_level integer default 0,
    prime_open_time long default 0,
    prime_end_time long default 0,

    youmeng_checked integer default 0,

    server_time long

);

create table Click (
    id integer primary key autoincrement,
    time time not null,

    user_id integer not null,

    earn_amount float default 0.0,

    with_draw_times_left integer default 1,

    request_with_draw_amount float default 0.0,
    request_with_draw_time time,

    manager_deal_time time,

    foreign key (user_id) references User (id)
);

create table Log (
    id integer primary key autoincrement,
    time time not null,

    user_id integer not null,

    operation text not null,

    device text,
    os text,
    android_version text,

    network text,
    ip text not null,
    location text

);