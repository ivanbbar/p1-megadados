-- Create DB

CREATE SCHEMA IF NOT EXISTS estoque;
USE estoque;

DROP TABLE IF EXISTS estoque.inventory ;
DROP TABLE IF EXISTS estoque.product ;
DROP TABLE IF EXISTS estoque.inventory_product ;


CREATE TABLE IF NOT EXISTS estoque.inventory (
  inventory_id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (inventory_id));

CREATE TABLE IF NOT EXISTS estoque.product (
  product_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  price FLOAT NOT NULL,
  description VARCHAR(100) NULL,
  PRIMARY KEY (product_id));

CREATE TABLE IF NOT EXISTS estoque.inventory_product (
  inventory_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  PRIMARY KEY (inventory_id, product_id),
  INDEX fk_p_idx (product_id ASC) VISIBLE,
  CONSTRAINT fk_inventory_id
    FOREIGN KEY (inventory_id)
    REFERENCES estoque.inventory (inventory_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_product_id
    FOREIGN KEY (product_id)
    REFERENCES estoque.product (product_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- Insertions

INSERT INTO inventory VALUES (1);
INSERT INTO inventory VALUES (2);
INSERT INTO inventory VALUES (3);

INSERT INTO product VALUES (1, "Guarana Jesus", "30.0", "Refri maranhense com gosto de tuti fruti");
INSERT INTO product VALUES (2, "carambola", "20.0", "Fruta que sofreu hiperinflacao");
INSERT INTO product VALUES (3, "rapadura", "1.5", "É doce mas não é mole");
INSERT INTO product VALUES (4, "bolo de rolo", "32.0", "Não é a mesma coisa que rocambole");

INSERT INTO inventory_product VALUES (1, 1, 9);
INSERT INTO inventory_product VALUES (1, 2, 13);
INSERT INTO inventory_product VALUES (2, 1, 3);
INSERT INTO inventory_product VALUES (2, 3, 5);
INSERT INTO inventory_product VALUES (2, 4, 12);
INSERT INTO inventory_product VALUES (3, 2, 13);