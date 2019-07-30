

drop table ft_activity;
CREATE TABLE `ft_activity` (
  `fta_sk` int(11) NOT NULL AUTO_INCREMENT,
  `ft_sk` int(11) DEFAULT NULL,
  `symbol`  varchar(10)  DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `price` double DEFAULT NULL,
  `action` char(1) DEFAULT NULL,
  PRIMARY KEY (`fta_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;


drop table ticker_price;
CREATE TABLE `ticker_price` (
  `tp_sk` int(11) NOT NULL AUTO_INCREMENT,
  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `price` double DEFAULT NULL,
  `instance_id` int(4) DEFAULT NULL,
  `tickerId` int(4) DEFAULT NULL,
  PRIMARY KEY (`tp_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1 ;

drop table symbol_ticker;
CREATE TABLE `symbol_ticker` (
  `st_sk` int(11) NOT NULL AUTO_INCREMENT,
  `ft_sk` int(11) DEFAULT NULL,
  `symbol`  varchar(8)  DEFAULT NULL,
  `instance_id` int(4) DEFAULT NULL,
  `tickerId` int(4) DEFAULT NULL,
  PRIMARY KEY (`st_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1 ;


drop table trade_action;
create table trade_action ( 
  `ta_sk` int(8) NOT NULL AUTO_INCREMENT,
  `symbol`  varchar(10)  DEFAULT NULL,
  `action` varchar(10) DEFAULT NULL,
  `state` int(4) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ta_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1 ;
  	

drop table symbol_price;
create table symbol_price ( 
  `sp_sk` int(8) NOT NULL AUTO_INCREMENT,
  `symbol`  varchar(10)  DEFAULT NULL,
  `price` double DEFAULT NULL,
  `volume` int(8) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `date_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`sp_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1 ;
  	

drop table symbol_price_hist;
create table symbol_price_hist ( 
  `sph_sk` int(8) NOT NULL AUTO_INCREMENT,
  `symbol`  varchar(10)  DEFAULT NULL,
  `price` double DEFAULT NULL,
  `volume` int(8) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `date_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`sph_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1 ;
