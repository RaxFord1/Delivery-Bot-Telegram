SET SQL_SAFE_UPDATES = 0;

USE `mydb` ;



-- Table `suplier`

DELETE FROM `suplier`;
ALTER TABLE `suplier` AUTO_INCREMENT = 1;

select * from `suplier`;
insert into `suplier` (`name`) values ("FortFied"), ("EatNow");

select * from `suplier`;



-- Table `product`


DELETE FROM `product`;
ALTER TABLE `product` AUTO_INCREMENT = 1;

select * from `product`;

insert into `product` (`name`, `buy_price`, `units`) values 
("Грибы", 35.7, 1000), ("Бекон", 140, 1000), ("Хлеб", 7.90, 200),
("Болгарский перец", 100.7, 2500), ("Лук", 5.2, 1000), ("Мак", 80, 100);

insert into `product` (`name`, `buy_price`, `units`) values 
("Масло", 24, 100);

select * from `product`;



-- Table `products_on_store`


DELETE FROM `products_on_store`;
ALTER TABLE `products_on_store` AUTO_INCREMENT = 1;

select * from `products_on_store`;

insert into `products_on_store` (`id_suplier`, `id_product`, `num`, `date`) values 
(1, 1, 5000, NOW()), (1, 2, 5000, NOW()), (1, 3, 1000, NOW()),
(1, 4, 10000, NOW()), (1, 5, 5000, NOW()), (1, 6, 1000, NOW());

insert into `products_on_store` (`id_suplier`, `id_product`, `num`) values 
(2, 7, 1000);

select * from `products_on_store`;



-- Table `dish`


DELETE FROM `dish`;
ALTER TABLE `dish` AUTO_INCREMENT = 1;

select * from `dish`;
insert into `dish` (`name`, `description`, `price`) values 
("Бутерброд", "Вид холодної закуски. Являє собою скибочку хліба або булки, на яку покладені додаткові харчові продукти.", 35.7),
("Ролл", "SDADSAD", 35.7),
("Суп", "Рідка страва, розповсюджена в багатьох країнах", 35.7),
("Кофе", "Напій, що виготовляється зі смаженого насіння плодів — «бобів» кавового дерева.", 35.7);

select * from `dish`;



-- Table `dish_has_product`


DELETE FROM `dish_has_product`;
ALTER TABLE `dish_has_product` AUTO_INCREMENT = 1;

select * from `dish_has_product`;
insert into `dish_has_product` (`dish_iddish`, `product_idproduct`, `product_amount`) values 
(1, 3, 35), (1, 2, 20), (1, 7, 10);

select * from `dish_has_product`;



-- Table `client`

DELETE FROM `client`;
ALTER TABLE `client` AUTO_INCREMENT = 1;

select * from `client`;
insert into `client` (`firstname`, `secondname`, `username`) values 
("Дима", "Дзундза", "RaxFord1"), ("Дима", "Хоменко", "Anon");



-- Table `order`

DELETE FROM `order`;
ALTER TABLE `order` AUTO_INCREMENT = 1;

select * from `order`;
insert into `order` (`id_client`, `datetime_ordered`) values 
(1, "2020-02-03 18:14:59.997"),
(2, "2020-02-03 18:16:59.997");

select * from `order`;



-- Table `order_has_dish`

DELETE FROM `order_has_dish`;
ALTER TABLE `order_has_dish` AUTO_INCREMENT = 1;

select * from `order_has_dish`;
insert into `order_has_dish` (`order_idorder`, `dish_iddish`, `num`) values 
(1, 1, 1), (2, 2, 4);

select * from `order_has_dish`;



-- Table `courier`

DELETE FROM `courier`;
ALTER TABLE `courier` AUTO_INCREMENT = 1;

select * from `courier`;
insert into `courier` (`fullname`, `credit`) values 
("Дима Дзундза", "458432156453135"),
("Олександр Горминк", "542312354987234"),
("Горчай Лонівнов", "842341589423546");

select * from `courier`;
