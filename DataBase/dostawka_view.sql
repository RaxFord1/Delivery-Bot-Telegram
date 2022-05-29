use `mydb`;

create OR REPLACE view `view_menu` as
select `dish`.`iddish`,`dish`.`name` as 'dish', `dish`.`description` as 'desc', `dish`.`price` as 'price' from dish 
group by `dish`.`name`
;
select * from `view_menu`;


create or replace view `view_today_orders` as select `order`.`idorder` as 'Айді', GROUP_CONCAT(`dish`.`name`SEPARATOR ', ') as 'Назва',`order_has_dish`.`num` as 'КоЛ-Во', `order`.`price` from `order`
join `order_has_dish` on `order_has_dish`.`order_idorder` = `order`.`idorder`
join `dish` on `dish`.`iddish` = `order_has_dish`.`dish_iddish`
where DAY(`order`.`datetime`) = DAY(NOW()) and MONTH(`order`.`datetime`) = MONTH(NOW()) AND paid = 1
group by `order`.`idorder`;
select * from `view_today_orders`;

create or replace view `view_today_orders_s` as select `order`.`idorder` as 'Айді', `dish`.`name`as 'Назва',`order_has_dish`.`num` as 'КоЛ-Во', `order`.`price` from `order`
join `order_has_dish` on `order_has_dish`.`order_idorder` = `order`.`idorder`
join `dish` on `dish`.`iddish` = `order_has_dish`.`dish_iddish`
where DAY(`order`.`datetime`) = DAY(NOW()) and MONTH(`order`.`datetime`) = MONTH(NOW()) AND paid = 1;
select * from `view_today_orders_s`;



create or replace view `view_last_month_orders` as select `order`.`idorder` as 'Айді', GROUP_CONCAT(`dish`.`name`SEPARATOR ', ') as 'Назва',`order_has_dish`.`num` as 'КоЛ-Во', `order`.`paid` as 'Оплачено', `order`.`price` from `order`
join `order_has_dish` on `order_has_dish`.`order_idorder` = `order`.`idorder`
join `dish` on `dish`.`iddish` = `order_has_dish`.`dish_iddish`
where MONTH(`order`.`datetime`) = MONTH(NOW()) AND paid = 1
group by `order`.`idorder`;
select * from `view_last_month_orders`;

create or replace view `view_last_month_orders_s` as select `order`.`idorder` as 'Айді', `dish`.`name` as 'Назва',`order_has_dish`.`num` as 'КоЛ-Во', `order`.`paid` as 'Оплачено', `order`.`price` from `order`
join `order_has_dish` on `order_has_dish`.`order_idorder` = `order`.`idorder`
join `dish` on `dish`.`iddish` = `order_has_dish`.`dish_iddish`
where MONTH(`order`.`datetime`) = MONTH(NOW()) AND paid = 1;
select * from `view_last_month_orders_s`;

create or replace view `view_suplies` as SELECT `product`.`name` as "Продукт", `products_on_store`.`num` as "Количество" ,`products_on_store`.`date` as "Дата" ,`suplier`.`name` as "Поставщик" 
FROM products_on_store join `suplier` on `suplier`.`idsuplier` = `products_on_store`.`id_suplier`
join `product` on `product`.`idproduct` = `products_on_store`.`id_product`;
select * from `view_suplies`;

create OR REPLACE view `view_all_clients` as
select `client`.`idclient`, `client`.`firstname`, `client`.`secondname`, `client`.`username`, sum(`order`.`price`) as "sum" from `client`
join `order` on `client`.`idclient` = `order`.`id_client`
where paid = 1
group by `client`.`idclient`
ORDER BY `idclient` asc
;
select * from `view_all_clients`;

create OR REPLACE view `view_top_10_clients` as
select `client`.`idclient`,`client`.`firstname`,`client`.`secondname`, `client`.`username`, SUM(price) suma from `order` join `client` on `client`.`idclient` = `order`.`id_client`
where `order`.`paid` = 1
group by `client`.`idclient`
ORDER BY suma desc
LIMIT 10
;
select * from `view_top_10_clients`;

create OR REPLACE view `view_paid_and_without_courier_orders` as
select `client`.`firstname`, `client`.`secondname`, `client`.`username`, `order`.`datetime` ,`order`.`place`,  GROUP_CONCAT(`dish`.`name`SEPARATOR ', ') as "Блюда", `order_has_dish`.`num`, `order`.`idorder` from `order` 
join `client` on `client`.`idclient` = `order`.`id_client`	
join `order_has_dish` on `order_has_dish`.`order_idorder` = `order`.`idorder`
join `dish` on `dish`.`iddish` = `order_has_dish`.`dish_iddish`
where paid = 1 AND courier_id is Null
group by `order`.`idorder`;
select * from `view_paid_and_without_courier_orders`;

create OR REPLACE view `view_paid_and_without_courier_orders_s` as
select `client`.`firstname`, `client`.`secondname`, `client`.`username`, `order`.`datetime` ,`order`.`place`,  `dish`.`name`as "Блюда", `order_has_dish`.`num`, `order`.`idorder` from `order` 
join `client` on `client`.`idclient` = `order`.`id_client`	
join `order_has_dish` on `order_has_dish`.`order_idorder` = `order`.`idorder`
join `dish` on `dish`.`iddish` = `order_has_dish`.`dish_iddish`
where paid = 1 AND courier_id is Null;
select * from `view_paid_and_without_courier_orders_s`;
