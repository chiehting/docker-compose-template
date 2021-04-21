Use db;

DROP TABLE IF EXISTS data;
CREATE TABLE data (
  id int NOT NULL AUTO_INCREMENT,
  create_time datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '建立日期',
  update_time datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日期',
  value VARCHAR(32) NOT NULL,
  PRIMARY KEY (id) USING BTREE
) ENGINE = InnoDB;

INSERT INTO data (value) VALUES ('insert'), ('insert');
UPDATE data SET value='update' WHERE id=1;

