INSERT INTO public.system_item_type_registry (system_item_id, system_item_type) VALUES ('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', 'FOLDER');
INSERT INTO public.system_item_type_registry (system_item_id, system_item_type) VALUES ('d515e43f-f3f6-4471-bb77-6b455017a2d2', 'FOLDER');
INSERT INTO public.system_item_type_registry (system_item_id, system_item_type) VALUES ('863e1a7a-1304-42ae-943b-179184c077e3', 'FILE');
INSERT INTO public.system_item_type_registry (system_item_id, system_item_type) VALUES ('b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4', 'FILE');
INSERT INTO public.system_item_type_registry (system_item_id, system_item_type) VALUES ('1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', 'FOLDER');
INSERT INTO public.system_item_type_registry (system_item_id, system_item_type) VALUES ('98883e8f-0507-482f-bce2-2fb306cf6483', 'FILE');
INSERT INTO public.system_item_type_registry (system_item_id, system_item_type) VALUES ('74b81fda-9cdc-4b63-8927-c978afed5cf4', 'FILE');
INSERT INTO public.system_item_type_registry (system_item_id, system_item_type) VALUES ('73bc3b36-02d1-4245-ab35-3106c9ee1c65', 'FILE');

INSERT INTO public.system_items (id, parent_id, date, type, url, size, deleted) VALUES ('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', null, '2022-02-01 12:00:00.000000', 'FOLDER', null, 0, false);
INSERT INTO public.system_items (id, parent_id, date, type, url, size, deleted) VALUES ('d515e43f-f3f6-4471-bb77-6b455017a2d2', '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', '2022-02-02 12:00:00.000000', 'FOLDER', null, 0, false);
INSERT INTO public.system_items (id, parent_id, date, type, url, size, deleted) VALUES ('863e1a7a-1304-42ae-943b-179184c077e3', 'd515e43f-f3f6-4471-bb77-6b455017a2d2', '2022-02-02 12:00:00.000000', 'FILE', '/file/url1', 128, false);
INSERT INTO public.system_items (id, parent_id, date, type, url, size, deleted) VALUES ('b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4', 'd515e43f-f3f6-4471-bb77-6b455017a2d2', '2022-02-02 12:00:00.000000', 'FILE', '/file/url2', 256, false);
INSERT INTO public.system_items (id, parent_id, date, type, url, size, deleted) VALUES ('1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', '2022-02-03 12:00:00.000000', 'FOLDER', null, 0, false);
INSERT INTO public.system_items (id, parent_id, date, type, url, size, deleted) VALUES ('98883e8f-0507-482f-bce2-2fb306cf6483', '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', '2022-02-03 12:00:00.000000', 'FILE', '/file/url3', 512, false);
INSERT INTO public.system_items (id, parent_id, date, type, url, size, deleted) VALUES ('74b81fda-9cdc-4b63-8927-c978afed5cf4', '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', '2022-02-03 12:00:00.000000', 'FILE', '/file/url4', 1024, false);
INSERT INTO public.system_items (id, parent_id, date, type, url, size, deleted) VALUES ('73bc3b36-02d1-4245-ab35-3106c9ee1c65', '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', '2022-02-03 15:00:00.000000', 'FILE', '/file/url5', 64, false);

INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', '2022-02-01 12:00:00.000000', 0);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('d515e43f-f3f6-4471-bb77-6b455017a2d2', 'd515e43f-f3f6-4471-bb77-6b455017a2d2', '2022-02-02 12:00:00.000000', 0);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('863e1a7a-1304-42ae-943b-179184c077e3', '863e1a7a-1304-42ae-943b-179184c077e3', '2022-02-02 12:00:00.000000', 0);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4', 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4', '2022-02-02 12:00:00.000000', 0);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', 'd515e43f-f3f6-4471-bb77-6b455017a2d2', '2022-02-02 12:00:00.000000', 1);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', '863e1a7a-1304-42ae-943b-179184c077e3', '2022-02-02 12:00:00.000000', 2);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('d515e43f-f3f6-4471-bb77-6b455017a2d2', '863e1a7a-1304-42ae-943b-179184c077e3', '2022-02-02 12:00:00.000000', 1);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4', '2022-02-02 12:00:00.000000', 2);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('d515e43f-f3f6-4471-bb77-6b455017a2d2', 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4', '2022-02-02 12:00:00.000000', 1);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', '2022-02-03 12:00:00.000000', 0);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('98883e8f-0507-482f-bce2-2fb306cf6483', '98883e8f-0507-482f-bce2-2fb306cf6483', '2022-02-03 12:00:00.000000', 0);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('74b81fda-9cdc-4b63-8927-c978afed5cf4', '74b81fda-9cdc-4b63-8927-c978afed5cf4', '2022-02-03 12:00:00.000000', 0);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', '2022-02-03 12:00:00.000000', 1);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', '98883e8f-0507-482f-bce2-2fb306cf6483', '2022-02-03 12:00:00.000000', 2);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', '98883e8f-0507-482f-bce2-2fb306cf6483', '2022-02-03 12:00:00.000000', 1);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', '74b81fda-9cdc-4b63-8927-c978afed5cf4', '2022-02-03 12:00:00.000000', 2);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', '74b81fda-9cdc-4b63-8927-c978afed5cf4', '2022-02-03 12:00:00.000000', 1);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('73bc3b36-02d1-4245-ab35-3106c9ee1c65', '73bc3b36-02d1-4245-ab35-3106c9ee1c65', '2022-02-03 15:00:00.000000', 0);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1', '73bc3b36-02d1-4245-ab35-3106c9ee1c65', '2022-02-03 15:00:00.000000', 2);
INSERT INTO public.system_item_links (parent_id, child_id, date, depth) VALUES ('1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', '73bc3b36-02d1-4245-ab35-3106c9ee1c65', '2022-02-03 15:00:00.000000', 1);
