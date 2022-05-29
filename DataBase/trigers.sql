use mydb;
DROP TRIGGER IF EXISTS `order_has_dish_update`;
delimiter $$
create trigger `order_has_dish_update` after update
on `order_has_dish` for each row
BEGIN
    call recalculate_order(new.`order_idorder`);	
END $$
delimiter ;
DROP TRIGGER IF EXISTS `order_has_dish_insert`;
delimiter $$
create trigger `order_has_dish_insert` after insert
on `order_has_dish` for each row
BEGIN
	call recalculate_order(new.`order_idorder`);	
END $$
delimiter ;
DROP TRIGGER IF EXISTS `order_has_dish_delete`;
delimiter $$
create trigger `order_has_dish_delete` after delete
on `order_has_dish` for each row
BEGIN
	call recalculate_order(old.`order_idorder`);	
END $$
delimiter ;
DROP TRIGGER IF EXISTS `products_on_store_update`;
delimiter $$
create trigger `products_on_store_update` after update
on `products_on_store` for each row
BEGIN
    set @dif = new.`num` - old.`num`;
	update `product` set `product`.`num` = `product`.`num` + @dif where `product`.`idproduct` = new.id;
END $$
delimiter ;
DROP TRIGGER IF EXISTS `products_on_store_insert`;
delimiter $$
create trigger `products_on_store_insert` after insert
on `products_on_store` for each row
BEGIN
	update `product` set `product`.`num` = `product`.`num` + new.num where `product`.`idproduct` = new.id_product;
END $$
delimiter ;
DROP TRIGGER IF EXISTS `products_on_store_delete`;
delimiter $$
create trigger `products_on_store_delete` after delete
on `products_on_store` for each row
BEGIN
	set @num = old.`num`;
	update `product` set `product`.`num` = `product`.`num` - @num where old.id_product = `product`.`idproduct`;	
END $$
delimiter ;
