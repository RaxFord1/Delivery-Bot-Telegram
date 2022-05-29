use mydb;


select * from `order`; 

-- Меняем значение "Оплачено" на "Да"
DROP PROCEDURE IF EXISTS set_paid;
delimiter //
create procedure set_paid(IN id int)
	begin
		UPDATE `order` SET `paid`= 1 WHERE `idorder` = id;
        UPDATE `order` SET `datetime_paid`= NOW() WHERE `idorder` = id;
	end //
delimiter ;
-- call set_paid(42); 

-- Пересчитать стоимость Блюда
DROP PROCEDURE IF EXISTS `recalculate_dish`;
delimiter //
create procedure `recalculate_dish`(IN id_dish int, procent float)
BEGIN
	IF EXISTS(SELECT `iddish` FROM `dish` WHERE `iddish` = id_dish)  THEN 
        set @sum = (select sum(dish_has_product.product_amount*(product.buy_price/product.units)) from dish 
		join dish_has_product on dish_has_product.dish_iddish = dish.iddish
		join product on product.idproduct = dish_has_product.product_idproduct
		WHERE dish.iddish = id_dish);
		update `dish` set `dish`.`price` = @sum+@sum*procent where `dish`.`iddish` = id_dish;
	end if;
END //
delimiter ;
-- call recalculate_dish(8,0.5);

-- Установить или изменить кур'єра
DROP PROCEDURE IF EXISTS `order_set_courier`;
delimiter //
create procedure `order_set_courier`(IN id_order int, id_courier int)
BEGIN
    if exists(select * from courier where `courier`.`id` = id_courier) then
		IF EXISTS(SELECT `idorder` FROM `order` WHERE `idorder` = id_order)  THEN 
			update `order` set `order`.`courier_id` = id_courier where (`order`.`idorder` = id_order);
        end if;
    END IF;	
END //
delimiter ;
-- call `order_set_courier`(42, 3);

-- Замовлення за певним кур’єром
DROP PROCEDURE IF EXISTS `courier_my_orders`;
delimiter //
create procedure `courier_my_orders`(IN id varchar(45))
BEGIN
	SELECT  `client`.`firstname`, `client`.`secondname`, `client`.`username`, `order`.`datetime` ,`order`.`place`, `order`.`idorder` from `order` 
join courier on `courier`.`id` = `order`.`courier_id`
join `client` on `client`.`idclient` = `order`.`id_client`	
where `courier`.`telegramid` = id and delivered = 0 and paid = 1;
END //
delimiter ;
-- call courier_my_orders('846521325');

-- Замовлення за період
DROP PROCEDURE IF EXISTS `orders_in_period`;
delimiter //
create procedure `orders_in_period`(IN first_date date, second_date date)
BEGIN
	select `order`.`idorder` as 'Айді', GROUP_CONCAT(`dish`.`name`SEPARATOR ', ') as 'Назва',`order_has_dish`.`num` as 'КоЛ-Во', `order`.`paid` as 'Оплачено' from `order`
join `order_has_dish` on `order_has_dish`.`order_idorder` = `order`.`idorder`
join `dish` on `dish`.`iddish` = `order_has_dish`.`dish_iddish`
where paid = 1 and `order`.`datetime` BETWEEN first_date AND second_date
group by `order`.`idorder` ;
END //
delimiter ;
-- call orders_in_period('2020-03-02', '2020-04-06	');

-- Продукти, яких менше заданої кількості в наявності
DROP PROCEDURE IF EXISTS `producct_lack_on_store`;
delimiter //
create procedure `producct_lack_on_store`(IN num int)
BEGIN
	select `product`.`name` as 'Назва ', `product`.`num` as 'Кількість' from `product` where `product`.`num`<=num;
END //
delimiter ;
-- call `producct_lack_on_store`(2500);

-- Продукти, яких більше заданої кількості в наявності
DROP PROCEDURE IF EXISTS `producct_overage_on_store`;
delimiter //
create procedure `producct_overage_on_store`(IN num int)
BEGIN
	select `product`.`name` as 'Назва ', `product`.`num` as 'Кількість' from `product` where `product`.`num`>=num;
END //
delimiter ;
-- call producct_overage_on_store(2500);

-- Пересчитать стоимость заказа
DROP PROCEDURE IF EXISTS `recalculate_order`;
delimiter //
create procedure `recalculate_order`(IN id_order int)
BEGIN
	IF EXISTS(SELECT `idorder` FROM `order` WHERE `idorder` = id_order)  THEN 
        set @sum = (select sum(price*num) from `order_has_dish` join `dish` on `order_has_dish`.`dish_iddish` = `dish`.`iddish` where `order_has_dish`.`order_idorder` = id_order);
		update `order` set `order`.`price` = @sum where `order`.`idorder` = id_order;
	end if;
END //
delimiter ;
-- call recalculate_order(42);

-- Змінити кількість страв у замовлені
DROP PROCEDURE IF EXISTS `order_set_dish`;
delimiter //
create procedure `order_set_dish`(IN id_order int, id_dish int, new_num int)
BEGIN
    IF EXISTS(SELECT * FROM `order` WHERE `idorder` = id_order)  THEN 
		if exists(select * from  `order_has_dish` WHERE `order_idorder` = id_order) then
			if exists(select * from  `order_has_dish` WHERE `order_has_dish`.`order_idorder` = id_order and `order_has_dish`.`dish_iddish` = id_dish) then
				update `order_has_dish` set `order_has_dish`.`num` = new_num where ( `order_has_dish`.`order_idorder` = id_order and `order_has_dish`.`dish_iddish` = id_dish);
			else
				insert into `order_has_dish` (`order_idorder`, `dish_iddish`, `num`) values (id_order, id_dish, new_num);
			end if;
		else
			insert into `order_has_dish` (`order_idorder`, `dish_iddish`, `num`) values (id_order, id_dish, new_num);
		end if;
    END IF;	
END //
delimiter ;
-- call `order_set_dish`(42, 6, 6);
