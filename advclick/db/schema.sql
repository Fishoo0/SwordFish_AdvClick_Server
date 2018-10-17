drop table if exists User;
drop table if exists Click;
drop table if exists Log;

create table User (
    id integer primary key autoincrement,
    time text not null,

    name text not null,
    password text not null,
    token text,

    cover text,
    sex text,
    gender integer,
    birth text,
    age text,
    location text,
    about text,

    im_qq text,
    alipay text not null,
    alipay_name text,

    prime_level integer default 1,
    prime_open_time integer default 0,
    prime_level_duration default -1,

    youmeng text
);

create table Click (
    id integer primary key autoincrement,
    time time not null,

    user_id integer not null,

    earn_count float default 0,
    with_draw_times integer default 0,

    foreign key (user_id) references User (id)
);

create table Log (
    id integer primary key autoincrement,
    time time not null,

    user_id integer not null,

    operation text not null,

    device text not null,
    os text,
    android_version text,

    netwrok text,
    ip text not null,
    location text,

    foreign key (user_id) references User (id)
);