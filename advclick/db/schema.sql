drop table if exists User;
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

    prime_level integer default 1,
    prime_trial_time_left integer,

    earn_count float,
    with_draw_times integer,

    alipay text not null,
    taobao text,
    wechat text,

    youmeng text

);