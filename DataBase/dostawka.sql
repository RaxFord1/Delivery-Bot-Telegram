-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mydb` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`client`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`client` ;

CREATE TABLE IF NOT EXISTS `mydb`.`client` (
  `idclient` INT(11) NOT NULL AUTO_INCREMENT,
  `idtelegram` INT(11) NULL DEFAULT NULL,
  `firstname` VARCHAR(45) NULL DEFAULT NULL,
  `secondname` VARCHAR(45) NULL DEFAULT NULL,
  `username` VARCHAR(45) NULL DEFAULT NULL,
  `phone` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idclient`))
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`courier`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`courier` ;

CREATE TABLE IF NOT EXISTS `mydb`.`courier` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `fullname` VARCHAR(45) NOT NULL,
  `credit` VARCHAR(45) NULL DEFAULT NULL,
  `telegramid` varchar(45) null,
  PRIMARY KEY (`id`))
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`dish`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`dish` ;

CREATE TABLE IF NOT EXISTS `mydb`.`dish` (
  `iddish` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(200) NULL DEFAULT NULL,
  `price` FLOAT NULL DEFAULT '0',
  PRIMARY KEY (`iddish`))
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`product` ;

CREATE TABLE IF NOT EXISTS `mydb`.`product` (
  `idproduct` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `buy_price` FLOAT NULL DEFAULT '0',
  `units` FLOAT NULL DEFAULT '0',
  `num` FLOAT NULL DEFAULT '0',
  PRIMARY KEY (`idproduct`))
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`dish_has_product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`dish_has_product` ;

CREATE TABLE IF NOT EXISTS `mydb`.`dish_has_product` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `product_amount` INT(11) NULL DEFAULT '0',
  `dish_iddish` INT(11) NOT NULL,
  `product_idproduct` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_dish_has_product_dish1_idx` (`dish_iddish` ASC) VISIBLE,
  INDEX `fk_dish_has_product_product1_idx` (`product_idproduct` ASC) VISIBLE,
  CONSTRAINT `fk_dish_has_product_dish1`
    FOREIGN KEY (`dish_iddish`)
    REFERENCES `mydb`.`dish` (`iddish`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dish_has_product_product1`
    FOREIGN KEY (`product_idproduct`)
    REFERENCES `mydb`.`product` (`idproduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`order`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`order` ;

CREATE TABLE IF NOT EXISTS `mydb`.`order` (
  `idorder` INT(11) NOT NULL AUTO_INCREMENT,
  `id_client` INT(11) NOT NULL,
  `price` FLOAT NULL DEFAULT '0',
  `datetime_ordered` DATETIME NULL DEFAULT NULL,
  `datetime` DATETIME NULL DEFAULT NULL,
  `paid` TINYINT(4) NULL DEFAULT '0',
  `datetime_paid` DATETIME NULL DEFAULT NULL,
  `courier_id` INT(11) NULL DEFAULT NULL,
  `place` VARCHAR(45) NULL DEFAULT NULL,
  `delivered` TINYINT(4) NULL DEFAULT '0',
  PRIMARY KEY (`idorder`),
  INDEX `fk_order_client_idx` (`id_client` ASC) VISIBLE,
  INDEX `fk_order_courier1_idx` (`courier_id` ASC) VISIBLE,
  CONSTRAINT `fk_order_client`
    FOREIGN KEY (`id_client`)
    REFERENCES `mydb`.`client` (`idclient`),
  CONSTRAINT `fk_order_courier1`
    FOREIGN KEY (`courier_id`)
    REFERENCES `mydb`.`courier` (`id`))
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`order_has_dish`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`order_has_dish` ;

CREATE TABLE IF NOT EXISTS `mydb`.`order_has_dish` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `num` INT(11) NULL DEFAULT '0',
  `order_idorder` INT(11) NOT NULL,
  `dish_iddish` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_order_has_dish_order1`
    FOREIGN KEY (`order_idorder`)
    REFERENCES `mydb`.`order` (`idorder`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_has_dish_dish1`
    FOREIGN KEY (`dish_iddish`)
    REFERENCES `mydb`.`dish` (`iddish`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`suplier`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`suplier` ;

CREATE TABLE IF NOT EXISTS `mydb`.`suplier` (
  `idsuplier` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idsuplier`))
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`products_on_store`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`products_on_store` ;

CREATE TABLE IF NOT EXISTS `mydb`.`products_on_store` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `id_suplier` INT(11) NOT NULL,
  `id_product` INT(11) NOT NULL,
  `num` INT(11) NULL DEFAULT '0',
  `date` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_products_on_store_suplier1_idx` (`id_suplier` ASC) VISIBLE,
  INDEX `fk_products_on_store_product1_idx` (`id_product` ASC) VISIBLE,
  CONSTRAINT `fk_products_on_store_product1`
    FOREIGN KEY (`id_product`)
    REFERENCES `mydb`.`product` (`idproduct`),
  CONSTRAINT `fk_products_on_store_suplier1`
    FOREIGN KEY (`id_suplier`)
    REFERENCES `mydb`.`suplier` (`idsuplier`))
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
