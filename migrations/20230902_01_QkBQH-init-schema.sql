-- Init schema
-- depends: 

CREATE TABLE public.ayats (
  ayat_id integer NOT NULL,
  public_id character varying NOT NULL,
  day integer,
  sura_id integer NOT NULL,
  audio_id character varying NOT NULL,
  ayat_number character varying(10) NOT NULL,
  content character varying NOT NULL,
  arab_text character varying NOT NULL,
  transliteration character varying NOT NULL
);

CREATE SEQUENCE public.ayats_ayat_id_seq
  AS integer
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;

ALTER SEQUENCE public.ayats_ayat_id_seq OWNED BY public.ayats.ayat_id;

CREATE TABLE public.cities (
  city_id character varying NOT NULL,
  name character varying
);

CREATE TABLE public.files (
  file_id character varying NOT NULL,
  telegram_file_id character varying,
  link character varying,
  created_at timestamp without time zone NOT NULL
);

CREATE TABLE public.messages (
  message_id bigint NOT NULL,
  message_json json NOT NULL,
  is_unknown boolean NOT NULL,
  trigger_message_id bigint
);

CREATE SEQUENCE public.messages_message_id_seq
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;

ALTER SEQUENCE public.messages_message_id_seq OWNED BY public.messages.message_id;

CREATE TABLE public.suras (
  sura_id integer NOT NULL,
  link character varying NOT NULL
);

CREATE SEQUENCE public.suras_sura_id_seq
  AS integer
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;

ALTER SEQUENCE public.suras_sura_id_seq OWNED BY public.suras.sura_id;

CREATE TABLE public.user_actions (
  user_action_id uuid NOT NULL,
  date_time timestamp without time zone NOT NULL,
  action character varying NOT NULL,
  user_id integer
);

CREATE TABLE public.users (
  chat_id bigint NOT NULL,
  is_active boolean DEFAULT true NOT NULL,
  comment character varying,
  day integer,
  city_id character varying,
  referrer_id integer,
  legacy_id integer,
  username character varying,
  password_hash character varying
);

ALTER TABLE ONLY public.ayats ALTER COLUMN ayat_id SET DEFAULT nextval('public.ayats_ayat_id_seq'::regclass);

ALTER TABLE ONLY public.messages ALTER COLUMN message_id SET DEFAULT nextval('public.messages_message_id_seq'::regclass);

ALTER TABLE ONLY public.suras ALTER COLUMN sura_id SET DEFAULT nextval('public.suras_sura_id_seq'::regclass);

ALTER TABLE ONLY public.ayats
  ADD CONSTRAINT ayats_pkey PRIMARY KEY (ayat_id);

ALTER TABLE ONLY public.cities
  ADD CONSTRAINT cities_pkey PRIMARY KEY (city_id);

ALTER TABLE ONLY public.files
  ADD CONSTRAINT files_pkey PRIMARY KEY (file_id);

ALTER TABLE ONLY public.messages
  ADD CONSTRAINT messages_pkey PRIMARY KEY (message_id);

ALTER TABLE ONLY public.suras
  ADD CONSTRAINT suras_pkey PRIMARY KEY (sura_id);

ALTER TABLE ONLY public.user_actions
  ADD CONSTRAINT user_actions_pkey PRIMARY KEY (user_action_id);

ALTER TABLE ONLY public.users
  ADD CONSTRAINT users_pkey PRIMARY KEY (chat_id);

ALTER TABLE ONLY public.ayats
  ADD CONSTRAINT ayats_audio_id_fkey FOREIGN KEY (audio_id) REFERENCES public.files(file_id);

ALTER TABLE ONLY public.ayats
  ADD CONSTRAINT ayats_sura_id_fkey FOREIGN KEY (sura_id) REFERENCES public.suras(sura_id);

ALTER TABLE ONLY public.user_actions
  ADD CONSTRAINT user_actions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(chat_id);

ALTER TABLE ONLY public.users
  ADD CONSTRAINT users_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.cities(city_id);

ALTER TABLE ONLY public.users
  ADD CONSTRAINT users_referrer_id_fkey FOREIGN KEY (referrer_id) REFERENCES public.users(chat_id);
