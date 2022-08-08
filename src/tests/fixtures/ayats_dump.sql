INSERT INTO content_file (link_to_file, tg_file_id, name)
VALUES ('/link', 'awefa8293', 'ayat_audio');

INSERT INTO content_morningcontent (additional_content, day)
VALUES ('', 1);

INSERT INTO content_sura (number, pars_hash, link, child_elements_count)
VALUES (1, 'adsf', '/hello', 1);

INSERT INTO content_ayat (additional_content, arab_text, trans, sura_id, ayat, html, audio_id, one_day_content_id, content)
VALUES ('', '', '', 1, '1-7', '<html></html>', 1, 1, 'ayat content');
