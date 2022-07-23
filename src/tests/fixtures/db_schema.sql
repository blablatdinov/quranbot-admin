create sequence content_audiofile_id_seq
	as integer;

alter sequence content_audiofile_id_seq owner to almazilaletdinov;

create sequence content_file_id_seq;

alter sequence content_file_id_seq owner to almazilaletdinov;

create table auth_group
(
	id serial
		constraint auth_group_pkey
			primary key,
	name varchar(150) not null
		constraint auth_group_name_key
			unique
);

alter table auth_group owner to almazilaletdinov;

create index auth_group_name_a6ea08ec_like
	on auth_group (name varchar_pattern_ops);

create table auth_user
(
	id serial
		constraint auth_user_pkey
			primary key,
	password varchar(128) not null,
	last_login timestamp with time zone,
	is_superuser boolean not null,
	username varchar(150) not null
		constraint auth_user_username_key
			unique,
	first_name varchar(150) not null,
	last_name varchar(150) not null,
	email varchar(254) not null,
	is_staff boolean not null,
	is_active boolean not null,
	date_joined timestamp with time zone not null
);

alter table auth_user owner to almazilaletdinov;

create index auth_user_username_6821ab7c_like
	on auth_user (username varchar_pattern_ops);

create table auth_user_groups
(
	id serial
		constraint auth_user_groups_pkey
			primary key,
	user_id integer not null
		constraint auth_user_groups_user_id_6a12ed8b_fk_auth_user_id
			references auth_user
				deferrable initially deferred,
	group_id integer not null
		constraint auth_user_groups_group_id_97559544_fk_auth_group_id
			references auth_group
				deferrable initially deferred,
	constraint auth_user_groups_user_id_group_id_94350c0c_uniq
		unique (user_id, group_id)
);

alter table auth_user_groups owner to almazilaletdinov;

create index auth_user_groups_group_id_97559544
	on auth_user_groups (group_id);

create index auth_user_groups_user_id_6a12ed8b
	on auth_user_groups (user_id);

create table bot_init_adminmessage
(
	id bigserial
		constraint bot_init_adminmessage_pkey
			primary key,
	title varchar(128) not null,
	text text not null,
	key varchar(128) not null
);

alter table bot_init_adminmessage owner to almazilaletdinov;

create table bot_init_callbackdata
(
	id bigserial
		constraint bot_init_callbackdata_pkey
			primary key,
	date timestamp with time zone,
	call_id varchar(500) not null,
	chat_id integer not null,
	text text,
	json text not null
);

alter table bot_init_callbackdata owner to almazilaletdinov;

create table bot_init_mailing
(
	id bigserial
		constraint bot_init_mailing_pkey
			primary key,
	is_cleaned boolean not null
);

alter table bot_init_mailing owner to almazilaletdinov;

create table bot_init_message
(
	id bigserial
		constraint bot_init_message_pkey
			primary key,
	date timestamp with time zone,
	from_user_id integer not null,
	message_id integer not null,
	chat_id integer not null,
	text text,
	json text not null,
	mailing_id bigint
		constraint bot_init_message_mailing_id_c1836acc_fk
			references bot_init_mailing
				deferrable initially deferred,
	is_unknown boolean not null
);

alter table bot_init_message owner to almazilaletdinov;

create index bot_init_message_mailing_id_c1836acc
	on bot_init_message (mailing_id);

create table bot_init_subscriber_favourite_ayats
(
	id serial
		constraint bot_init_subscriber_favourite_ayats_pkey
			primary key,
	subscriber_id bigint not null,
	ayat_id bigint not null,
	constraint bot_init_subscriber_favo_subscriber_id_ayat_id_b4a5e060_uniq
		unique (subscriber_id, ayat_id)
);

alter table bot_init_subscriber_favourite_ayats owner to almazilaletdinov;

create index bot_init_subscriber_favourite_ayats_ayat_id_3da782a4
	on bot_init_subscriber_favourite_ayats (ayat_id);

create index bot_init_subscriber_favourite_ayats_subscriber_id_8dd008d5
	on bot_init_subscriber_favourite_ayats (subscriber_id);

create table content_file
(
	id bigint default nextval('content_file_id_seq'::regclass) not null
		constraint content_audiofile_pkey
			primary key,
	link_to_file varchar(512),
	tg_file_id varchar(512),
	name varchar(128)
);

alter table content_file owner to almazilaletdinov;

alter sequence content_audiofile_id_seq owned by content_file.id;

alter sequence content_file_id_seq owned by content_file.id;

create table content_morningcontent
(
	id bigserial
		constraint content_morningcontent_pkey
			primary key,
	additional_content text not null,
	day integer not null
		constraint content_morningcontent_day_3b283716_uniq
			unique
);

alter table content_morningcontent owner to almazilaletdinov;

create table content_podcast
(
	id bigserial
		constraint content_podcast_pkey
			primary key,
	title varchar(128) not null,
	audio_id bigint not null
		constraint content_podcast_audio_id_50878014_uniq
			unique
		constraint content_podcast_audio_id_50878014_fk
			references content_file
				deferrable initially deferred,
	article_link varchar(512)
);

alter table content_podcast owner to almazilaletdinov;

create table content_sura
(
	id bigserial
		constraint content_sura_pkey
			primary key,
	number integer not null,
	pars_hash varchar(64),
	link varchar(128) not null,
	child_elements_count integer not null
);

alter table content_sura owner to almazilaletdinov;

create table content_ayat
(
	id bigserial
		constraint content_ayat_pkey
			primary key,
	additional_content text not null,
	arab_text text not null,
	trans text not null,
	sura_id bigint not null
		constraint content_ayat_sura_id_6b460217_fk
			references content_sura
				deferrable initially deferred,
	ayat varchar(16),
	html text not null,
	audio_id bigint
		constraint content_ayat_audio_id_15757993_uniq
			unique
		constraint content_ayat_audio_id_15757993_fk
			references content_file
				deferrable initially deferred,
	one_day_content_id bigint
		constraint content_ayat_one_day_content_id_1f7105d0_fk
			references content_morningcontent
				deferrable initially deferred,
	content text not null
);

alter table content_ayat owner to almazilaletdinov;

create index content_ayat_one_day_content_id_1f7105d0
	on content_ayat (one_day_content_id);

create index content_ayat_sura_id_6b460217
	on content_ayat (sura_id);

create table django_content_type
(
	id serial
		constraint django_content_type_pkey
			primary key,
	app_label varchar(100) not null,
	model varchar(100) not null,
	constraint django_content_type_app_label_model_76bd3d3b_uniq
		unique (app_label, model)
);

alter table django_content_type owner to almazilaletdinov;

create table auth_permission
(
	id serial
		constraint auth_permission_pkey
			primary key,
	name varchar(255) not null,
	content_type_id integer not null
		constraint auth_permission_content_type_id_2f476e4b_fk_django_co
			references django_content_type
				deferrable initially deferred,
	codename varchar(100) not null,
	constraint auth_permission_content_type_id_codename_01ab375a_uniq
		unique (content_type_id, codename)
);

alter table auth_permission owner to almazilaletdinov;

create table auth_group_permissions
(
	id serial
		constraint auth_group_permissions_pkey
			primary key,
	group_id integer not null
		constraint auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
			references auth_group
				deferrable initially deferred,
	permission_id integer not null
		constraint auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
			references auth_permission
				deferrable initially deferred,
	constraint auth_group_permissions_group_id_permission_id_0cd325b0_uniq
		unique (group_id, permission_id)
);

alter table auth_group_permissions owner to almazilaletdinov;

create index auth_group_permissions_group_id_b120cbf9
	on auth_group_permissions (group_id);

create index auth_group_permissions_permission_id_84c5c92e
	on auth_group_permissions (permission_id);

create index auth_permission_content_type_id_2f476e4b
	on auth_permission (content_type_id);

create table auth_user_user_permissions
(
	id serial
		constraint auth_user_user_permissions_pkey
			primary key,
	user_id integer not null
		constraint auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id
			references auth_user
				deferrable initially deferred,
	permission_id integer not null
		constraint auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm
			references auth_permission
				deferrable initially deferred,
	constraint auth_user_user_permissions_user_id_permission_id_14a6b632_uniq
		unique (user_id, permission_id)
);

alter table auth_user_user_permissions owner to almazilaletdinov;

create index auth_user_user_permissions_permission_id_1fbb5f2c
	on auth_user_user_permissions (permission_id);

create index auth_user_user_permissions_user_id_a95ead1b
	on auth_user_user_permissions (user_id);

create table django_admin_log
(
	id serial
		constraint django_admin_log_pkey
			primary key,
	action_time timestamp with time zone not null,
	object_id text,
	object_repr varchar(200) not null,
	action_flag smallint not null
		constraint django_admin_log_action_flag_check
			check (action_flag >= 0),
	change_message text not null,
	content_type_id integer
		constraint django_admin_log_content_type_id_c4bce8eb_fk_django_co
			references django_content_type
				deferrable initially deferred,
	user_id integer not null
		constraint django_admin_log_user_id_c564eba6_fk_auth_user_id
			references auth_user
				deferrable initially deferred
);

alter table django_admin_log owner to almazilaletdinov;

create index django_admin_log_content_type_id_c4bce8eb
	on django_admin_log (content_type_id);

create index django_admin_log_user_id_c564eba6
	on django_admin_log (user_id);

create table django_migrations
(
	id serial
		constraint django_migrations_pkey
			primary key,
	app varchar(255) not null,
	name varchar(255) not null,
	applied timestamp with time zone not null
);

alter table django_migrations owner to almazilaletdinov;

create table django_session
(
	session_key varchar(40) not null
		constraint django_session_pkey
			primary key,
	session_data text not null,
	expire_date timestamp with time zone not null
);

alter table django_session owner to almazilaletdinov;

create index django_session_expire_date_a5c62663
	on django_session (expire_date);

create index django_session_session_key_c0390e0f_like
	on django_session (session_key varchar_pattern_ops);

create table prayer_city
(
	id bigserial
		constraint prayer_city_pkey
			primary key,
	link varchar(500) not null,
	name varchar(200) not null,
	source varchar(16) not null
);

alter table prayer_city owner to almazilaletdinov;

create table bot_init_subscriber
(
	id bigserial
		constraint bot_init_subscriber_pkey
			primary key,
	tg_chat_id integer not null
		constraint bot_init_subscriber_tg_chat_id_5eb6caa9_uniq
			unique,
	is_active boolean not null,
	comment text,
	day integer not null,
	city_id bigint
		constraint bot_init_subscriber_city_id_95701f89_fk
			references prayer_city
				deferrable initially deferred,
	step varchar(100),
	referer_id bigint
		constraint bot_init_subscriber_referer_id_da310ef3_fk
			references bot_init_subscriber
				deferrable initially deferred
);

alter table bot_init_subscriber owner to almazilaletdinov;

create table bot_init_admin
(
	id bigserial
		constraint bot_init_admin_pkey
			primary key,
	subscriber_id bigint not null
		constraint bot_init_admin_subscriber_id_key
			unique
		constraint bot_init_admin_subscriber_id_26560107_fk
			references bot_init_subscriber
				deferrable initially deferred
);

alter table bot_init_admin owner to almazilaletdinov;

create index bot_init_subscriber_city_id_95701f89
	on bot_init_subscriber (city_id);

create index bot_init_subscriber_referer_id_da310ef3
	on bot_init_subscriber (referer_id);

create table bot_init_subscriberaction
(
	id bigserial
		constraint bot_init_subscriberaction_pkey
			primary key,
	date_time timestamp with time zone not null,
	action varchar(16) not null,
	subscriber_id bigint not null
		constraint bot_init_subscriberaction_subscriber_id_a17a3e22_fk
			references bot_init_subscriber
				deferrable initially deferred
);

alter table bot_init_subscriberaction owner to almazilaletdinov;

create index bot_init_subscriberaction_subscriber_id_a17a3e22
	on bot_init_subscriberaction (subscriber_id);

create table prayer_day
(
	id bigserial
		constraint prayer_day_pkey
			primary key,
	date date not null
);

alter table prayer_day owner to almazilaletdinov;

create table prayer_prayer
(
	id bigserial
		constraint prayer_prayer_pkey
			primary key,
	time time not null,
	name varchar(10) not null,
	city_id bigint not null
		constraint prayer_prayer_city_id_8a5a0ed4_fk
			references prayer_city
				deferrable initially deferred,
	day_id bigint not null
		constraint prayer_prayer_day_id_cfa35953_fk
			references prayer_day
				deferrable initially deferred
);

alter table prayer_prayer owner to almazilaletdinov;

create index prayer_prayer_city_id_8a5a0ed4
	on prayer_prayer (city_id);

create index prayer_prayer_day_id_cfa35953
	on prayer_prayer (day_id);

create table prayer_prayeratusergroup
(
	id bigserial
		constraint prayer_prayeratusergroup_pkey
			primary key
);

alter table prayer_prayeratusergroup owner to almazilaletdinov;

create table prayer_prayeratuser
(
	id bigserial
		constraint prayer_prayeratuser_pkey
			primary key,
	is_read boolean not null,
	prayer_id bigint not null
		constraint prayer_prayeratuser_prayer_id_46e91086_fk
			references prayer_prayer
				deferrable initially deferred,
	prayer_group_id bigint not null
		constraint prayer_prayeratuser_prayer_group_id_f03cdb09_fk
			references prayer_prayeratusergroup
				deferrable initially deferred,
	subscriber_id bigint not null
		constraint prayer_prayeratuser_subscriber_id_1590e7c1_fk
			references bot_init_subscriber
				deferrable initially deferred
);

alter table prayer_prayeratuser owner to almazilaletdinov;

create index prayer_prayeratuser_prayer_group_id_f03cdb09
	on prayer_prayeratuser (prayer_group_id);

create index prayer_prayeratuser_prayer_id_46e91086
	on prayer_prayeratuser (prayer_id);

create index prayer_prayeratuser_subscriber_id_1590e7c1
	on prayer_prayeratuser (subscriber_id);

