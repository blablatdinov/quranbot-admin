-- files.filename column
-- depends: 20230902_01_QkBQH-init-schema

ALTER TABLE public.files
  ADD COLUMN filename character varying UNIQUE;
