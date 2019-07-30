-- MySQL dump 10.13  Distrib 5.5.47, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: scrape
-- ------------------------------------------------------
-- Server version	5.5.47-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `advfn_value`
--

DROP TABLE IF EXISTS `advfn_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advfn_value` (
  `advfn_sk` int(11) NOT NULL AUTO_INCREMENT,
  `fn` varchar(64) NOT NULL,
  `exchange` varchar(8) NOT NULL,
  `symbol` varchar(8) NOT NULL,
  `attribute` varchar(64) NOT NULL,
  `date_instant` varchar(45) DEFAULT NULL,
  `date_start` varchar(45) DEFAULT NULL,
  `date_end` varchar(45) DEFAULT NULL,
  `value` varchar(45) DEFAULT NULL,
  `form` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`advfn_sk`),
  UNIQUE KEY `uc_advfn_natural` (`exchange`,`symbol`,`attribute`,`date_instant`,`date_start`,`form`),
  KEY `symbol` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=23429659 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `archive_extract_history`
--

DROP TABLE IF EXISTS `archive_extract_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `archive_extract_history` (
  `aeh_sk` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(254) NOT NULL,
  `period` char(8) NOT NULL,
  `form` varchar(32) NOT NULL,
  `date_id` bigint(20) NOT NULL,
  `path` varchar(254) DEFAULT NULL,
  `xbrl` char(1) NOT NULL,
  `cik` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`aeh_sk`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `archive_extract_history_parsed`
--

DROP TABLE IF EXISTS `archive_extract_history_parsed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `archive_extract_history_parsed` (
  `aeh_sk` int(11) NOT NULL DEFAULT '0',
  `name` varchar(254) NOT NULL,
  `period` char(8) NOT NULL,
  `form` varchar(32) NOT NULL,
  `date_id` bigint(20) NOT NULL,
  `path` varchar(254) DEFAULT NULL,
  `xbrl` char(1) NOT NULL,
  `cik` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asset_value`
--

DROP TABLE IF EXISTS `asset_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asset_value` (
  `idasset_value` int(11) NOT NULL AUTO_INCREMENT,
  `date_id` bigint(20) DEFAULT NULL,
  `asset` varchar(45) DEFAULT NULL,
  `exchange` varchar(45) DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `volume` int(11) DEFAULT NULL,
  `change` double DEFAULT NULL,
  `percent_change` double DEFAULT NULL,
  PRIMARY KEY (`idasset_value`),
  UNIQUE KEY `uc_AssetDateID` (`asset`,`date_id`),
  KEY `av_asset_index` (`asset`),
  KEY `av_date_index` (`date_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23424091 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `asset_value_dated`
--

DROP TABLE IF EXISTS `asset_value_dated`;
/*!50001 DROP VIEW IF EXISTS `asset_value_dated`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `asset_value_dated` (
  `idasset_value` tinyint NOT NULL,
  `asset` tinyint NOT NULL,
  `exchange` tinyint NOT NULL,
  `open` tinyint NOT NULL,
  `close` tinyint NOT NULL,
  `change` tinyint NOT NULL,
  `percent_change` tinyint NOT NULL,
  `volume` tinyint NOT NULL,
  `date_id` tinyint NOT NULL,
  `date` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `bins`
--

DROP TABLE IF EXISTS `bins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bins` (
  `min_value` int(11) DEFAULT NULL,
  `max_value` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `close_trade`
--

DROP TABLE IF EXISTS `close_trade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `close_trade` (
  `ft_sk` int(11) NOT NULL DEFAULT '0',
  `eh_sk` int(11) DEFAULT NULL,
  `symbol` varchar(45) NOT NULL,
  `exchange` varchar(45) NOT NULL,
  `state` int(2) DEFAULT NULL,
  `date_id` bigint(20) NOT NULL,
  `INSERT_TS` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `close_trade_test`
--

DROP TABLE IF EXISTS `close_trade_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `close_trade_test` (
  `ft_sk` int(11) NOT NULL DEFAULT '0',
  `eh_sk` int(11) DEFAULT NULL,
  `symbol` varchar(45) NOT NULL,
  `exchange` varchar(45) NOT NULL,
  `state` int(2) DEFAULT NULL,
  `date_id` bigint(20) NOT NULL,
  `INSERT_TS` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company` (
  `company_sk` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `cik` varchar(20) DEFAULT NULL,
  `industry` varchar(256) DEFAULT NULL,
  `industry_id` int(4) DEFAULT NULL,
  `corp_state` varchar(2) DEFAULT NULL,
  `address_line_1` varchar(45) DEFAULT NULL,
  `address_line_2` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `zip` varchar(10) DEFAULT NULL,
  `name_override` varchar(256) DEFAULT NULL,
  `advfn_name` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`company_sk`),
  UNIQUE KEY `uc_CompanyCIK` (`cik`),
  KEY `company_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=65660 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `company_history`
--

DROP TABLE IF EXISTS `company_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company_history` (
  `companyh_sk` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `cik` varchar(20) DEFAULT NULL,
  `form` varchar(10) DEFAULT NULL,
  `date_id` bigint(20) NOT NULL,
  `fn` varchar(256) DEFAULT NULL,
  `clean_name` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`companyh_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=10838536 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `csi_symbols`
--

DROP TABLE IF EXISTS `csi_symbols`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `csi_symbols` (
  `csi_sk` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) NOT NULL,
  `exchange` varchar(10) NOT NULL,
  `cik` varchar(20) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`csi_sk`),
  KEY `cik` (`cik`)
) ENGINE=InnoDB AUTO_INCREMENT=829652 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ct_activity`
--

DROP TABLE IF EXISTS `ct_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ct_activity` (
  `fta_sk` int(11) NOT NULL DEFAULT '0',
  `ft_sk` int(11) DEFAULT NULL,
  `symbol` varchar(10) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `price` double DEFAULT NULL,
  `action` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ct_activity_test`
--

DROP TABLE IF EXISTS `ct_activity_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ct_activity_test` (
  `fta_sk` int(11) NOT NULL DEFAULT '0',
  `ft_sk` int(11) DEFAULT NULL,
  `symbol` varchar(10) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `price` double DEFAULT NULL,
  `action` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ct_buffer`
--

DROP TABLE IF EXISTS `ct_buffer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ct_buffer` (
  `ftb_sk` int(11) NOT NULL DEFAULT '0',
  `date_id` bigint(20) DEFAULT NULL,
  `wins` int(4) NOT NULL,
  `losses` int(4) NOT NULL,
  `spent` double DEFAULT NULL,
  `previous_enter` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ct_buffer_test`
--

DROP TABLE IF EXISTS `ct_buffer_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ct_buffer_test` (
  `ftb_sk` int(11) NOT NULL DEFAULT '0',
  `date_id` bigint(20) DEFAULT NULL,
  `wins` int(4) NOT NULL,
  `losses` int(4) NOT NULL,
  `spent` double DEFAULT NULL,
  `previous_enter` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `daily_dated_returns`
--

DROP TABLE IF EXISTS `daily_dated_returns`;
/*!50001 DROP VIEW IF EXISTS `daily_dated_returns`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `daily_dated_returns` (
  `date` tinyint NOT NULL,
  `profit` tinyint NOT NULL,
  `duration` tinyint NOT NULL,
  `amount` tinyint NOT NULL,
  `fama_offset` tinyint NOT NULL,
  `min_alpha` tinyint NOT NULL,
  `min_sig` tinyint NOT NULL,
  `min_assets` tinyint NOT NULL,
  `max_assets` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `daily_dated_summed_returns`
--

DROP TABLE IF EXISTS `daily_dated_summed_returns`;
/*!50001 DROP VIEW IF EXISTS `daily_dated_summed_returns`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `daily_dated_summed_returns` (
  `date` tinyint NOT NULL,
  `amount` tinyint NOT NULL,
  `duration` tinyint NOT NULL,
  `fama_offset` tinyint NOT NULL,
  `min_alpha` tinyint NOT NULL,
  `min_sig` tinyint NOT NULL,
  `min_assets` tinyint NOT NULL,
  `max_assets` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `daily_returns`
--

DROP TABLE IF EXISTS `daily_returns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `daily_returns` (
  `iddr_value` int(11) NOT NULL AUTO_INCREMENT,
  `date_id` bigint(20) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `duration` smallint(1) DEFAULT NULL,
  `fama_offset` int(11) DEFAULT NULL,
  `min_alpha` double DEFAULT NULL,
  `min_sig` double DEFAULT NULL,
  `min_assets` int(11) DEFAULT NULL,
  `max_assets` int(11) DEFAULT NULL,
  `asset` varchar(45) DEFAULT NULL,
  `trade` tinyint(1) DEFAULT NULL,
  `allocation` int(11) DEFAULT NULL,
  `buy` double DEFAULT NULL,
  `sell` double DEFAULT NULL,
  `profit` double DEFAULT NULL,
  PRIMARY KEY (`iddr_value`),
  UNIQUE KEY `uc_daily_returns1` (`date_id`,`amount`,`duration`,`fama_offset`,`min_alpha`,`min_sig`,`min_assets`,`max_assets`,`asset`,`trade`)
) ENGINE=InnoDB AUTO_INCREMENT=221996 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `daily_returns_all`
--

DROP TABLE IF EXISTS `daily_returns_all`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `daily_returns_all` (
  `iddr_value` int(11) NOT NULL AUTO_INCREMENT,
  `date_id` bigint(20) DEFAULT NULL,
  `allocation` int(11) DEFAULT NULL,
  `duration` smallint(1) DEFAULT NULL,
  `fama_offset` int(11) DEFAULT NULL,
  `min_alpha` double DEFAULT NULL,
  `min_sig` double DEFAULT NULL,
  `min_assets` int(11) DEFAULT NULL,
  `max_assets` int(11) DEFAULT NULL,
  `asset` varchar(45) DEFAULT NULL,
  `trade` tinyint(1) DEFAULT NULL,
  `buy` double DEFAULT NULL,
  `sell` double DEFAULT NULL,
  `profit` double DEFAULT NULL,
  PRIMARY KEY (`iddr_value`),
  UNIQUE KEY `uc_daily_returns1` (`date_id`,`allocation`,`duration`,`fama_offset`,`min_alpha`,`min_sig`,`min_assets`,`max_assets`,`asset`,`trade`)
) ENGINE=InnoDB AUTO_INCREMENT=39442 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `daily_volume`
--

DROP TABLE IF EXISTS `daily_volume`;
/*!50001 DROP VIEW IF EXISTS `daily_volume`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `daily_volume` (
  `date_id` tinyint NOT NULL,
  `date` tinyint NOT NULL,
  `sum(av.volume)` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `dates`
--

DROP TABLE IF EXISTS `dates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dates` (
  `date_id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `timestamp` bigint(20) NOT NULL,
  `weekend` char(10) NOT NULL DEFAULT 'Weekday',
  `day_of_week` char(10) NOT NULL,
  `month` char(10) NOT NULL,
  `month_day` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `week_starting_monday` char(2) NOT NULL,
  `month_num` int(11) DEFAULT NULL,
  `dow_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`date_id`),
  UNIQUE KEY `date` (`date`),
  KEY `year_week` (`year`,`week_starting_monday`),
  KEY `dates_dateid_index` (`date_id`),
  KEY `dates_date_index` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dates_map`
--

DROP TABLE IF EXISTS `dates_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dates_map` (
  `date_id` bigint(20) NOT NULL,
  `old_date_id` bigint(20) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `dr`
--

DROP TABLE IF EXISTS `dr`;
/*!50001 DROP VIEW IF EXISTS `dr`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `dr` (
  `iddr_value` tinyint NOT NULL,
  `date_id` tinyint NOT NULL,
  `allocation` tinyint NOT NULL,
  `duration` tinyint NOT NULL,
  `fama_offset` tinyint NOT NULL,
  `min_alpha` tinyint NOT NULL,
  `min_sig` tinyint NOT NULL,
  `min_assets` tinyint NOT NULL,
  `max_assets` tinyint NOT NULL,
  `asset` tinyint NOT NULL,
  `trade` tinyint NOT NULL,
  `buy` tinyint NOT NULL,
  `sell` tinyint NOT NULL,
  `profit` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `extract_history`
--

DROP TABLE IF EXISTS `extract_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `extract_history` (
  `eh_sk` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(254) NOT NULL,
  `period` char(8) NOT NULL,
  `form` varchar(32) NOT NULL,
  `date_id` bigint(20) NOT NULL,
  `html` varchar(254) DEFAULT NULL,
  `html_link` varchar(254) DEFAULT NULL,
  `cik` varchar(20) DEFAULT NULL,
  `status` char(1) DEFAULT NULL,
  `INSERT_TS` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`eh_sk`),
  KEY `eh_cik` (`cik`)
) ENGINE=InnoDB AUTO_INCREMENT=1429094 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `extract_history_archive`
--

DROP TABLE IF EXISTS `extract_history_archive`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `extract_history_archive` (
  `eh_sk` int(11) NOT NULL DEFAULT '0',
  `name` varchar(254) NOT NULL,
  `period` char(8) NOT NULL,
  `form` varchar(32) NOT NULL,
  `date_id` bigint(20) NOT NULL,
  `html` varchar(254) DEFAULT NULL,
  `html_link` varchar(254) DEFAULT NULL,
  `cik` varchar(20) DEFAULT NULL,
  `status` char(1) DEFAULT NULL,
  `INSERT_TS` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `type` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fama`
--

DROP TABLE IF EXISTS `fama`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fama` (
  `idfama` int(11) NOT NULL AUTO_INCREMENT,
  `mrkt_rf` double DEFAULT NULL,
  `smb` double DEFAULT NULL,
  `hml` double DEFAULT NULL,
  `rf` double DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`idfama`),
  KEY `date_id` (`date_id`),
  CONSTRAINT `fama_ibfk_1` FOREIGN KEY (`date_id`) REFERENCES `dates` (`date_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6573 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `filing_activity`
--

DROP TABLE IF EXISTS `filing_activity`;
/*!50001 DROP VIEW IF EXISTS `filing_activity`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `filing_activity` (
  `state` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `form` tinyint NOT NULL,
  `status` tinyint NOT NULL,
  `symbol` tinyint NOT NULL,
  `insert_ts` tinyint NOT NULL,
  `date_id` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `filing_price`
--

DROP TABLE IF EXISTS `filing_price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filing_price` (
  `fp_sk` int(11) NOT NULL AUTO_INCREMENT,
  `eh_sk` int(11) NOT NULL,
  `price` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `change` double DEFAULT NULL,
  PRIMARY KEY (`fp_sk`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `filing_trade`
--

DROP TABLE IF EXISTS `filing_trade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filing_trade` (
  `ft_sk` int(11) NOT NULL AUTO_INCREMENT,
  `eh_sk` int(11) DEFAULT NULL,
  `symbol` varchar(45) NOT NULL,
  `exchange` varchar(45) NOT NULL,
  `state` int(2) DEFAULT NULL,
  `date_id` bigint(20) NOT NULL,
  `INSERT_TS` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ft_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=34635 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `filing_trade_test`
--

DROP TABLE IF EXISTS `filing_trade_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filing_trade_test` (
  `ft_sk` int(11) NOT NULL AUTO_INCREMENT,
  `eh_sk` int(11) DEFAULT NULL,
  `symbol` varchar(45) NOT NULL,
  `exchange` varchar(45) NOT NULL,
  `state` int(2) DEFAULT NULL,
  `date_id` bigint(20) NOT NULL,
  `INSERT_TS` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ft_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=2394 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ft_activity`
--

DROP TABLE IF EXISTS `ft_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ft_activity` (
  `fta_sk` int(11) NOT NULL AUTO_INCREMENT,
  `ft_sk` int(11) DEFAULT NULL,
  `symbol` varchar(10) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `price` double DEFAULT NULL,
  `action` char(1) DEFAULT NULL,
  PRIMARY KEY (`fta_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=47901 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ft_activity_test`
--

DROP TABLE IF EXISTS `ft_activity_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ft_activity_test` (
  `fta_sk` int(11) NOT NULL DEFAULT '0',
  `ft_sk` int(11) DEFAULT NULL,
  `symbol` varchar(10) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `price` double DEFAULT NULL,
  `action` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ft_activity_test_0305`
--

DROP TABLE IF EXISTS `ft_activity_test_0305`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ft_activity_test_0305` (
  `fta_sk` int(11) NOT NULL DEFAULT '0',
  `ft_sk` int(11) DEFAULT NULL,
  `symbol` varchar(10) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `price` double DEFAULT NULL,
  `action` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ft_buffer`
--

DROP TABLE IF EXISTS `ft_buffer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ft_buffer` (
  `ftb_sk` int(11) NOT NULL AUTO_INCREMENT,
  `date_id` bigint(20) DEFAULT NULL,
  `wins` int(4) NOT NULL,
  `losses` int(4) NOT NULL,
  `spent` double DEFAULT NULL,
  `previous_enter` double DEFAULT NULL,
  PRIMARY KEY (`ftb_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=417 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ft_buffer_test`
--

DROP TABLE IF EXISTS `ft_buffer_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ft_buffer_test` (
  `ftb_sk` int(11) NOT NULL AUTO_INCREMENT,
  `date_id` bigint(20) DEFAULT NULL,
  `wins` int(4) NOT NULL,
  `losses` int(4) NOT NULL,
  `spent` double DEFAULT NULL,
  `previous_enter` double DEFAULT NULL,
  PRIMARY KEY (`ftb_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=197 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `fulfilled_list`
--

DROP TABLE IF EXISTS `fulfilled_list`;
/*!50001 DROP VIEW IF EXISTS `fulfilled_list`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `fulfilled_list` (
  `company_sk` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fundamental`
--

DROP TABLE IF EXISTS `fundamental`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fundamental` (
  `f_sk` int(11) NOT NULL AUTO_INCREMENT,
  `date_id` bigint(20) DEFAULT NULL,
  `asset` varchar(45) DEFAULT NULL,
  `PtB` double DEFAULT NULL,
  `earnings` double DEFAULT NULL,
  `dividends` double DEFAULT NULL,
  `mktcap` double DEFAULT NULL,
  `assets` double DEFAULT NULL,
  `intangibles` double DEFAULT NULL,
  `book_value` double DEFAULT NULL,
  `shares` double DEFAULT NULL,
  `exchange` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`f_sk`),
  UNIQUE KEY `uc_f_AssetDateID` (`asset`,`date_id`),
  KEY `f_sk_index` (`asset`),
  KEY `f_date_index` (`date_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2143026 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `gaap_map`
--

DROP TABLE IF EXISTS `gaap_map`;
/*!50001 DROP VIEW IF EXISTS `gaap_map`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `gaap_map` (
  `company_sk` tinyint NOT NULL,
  `exchange` tinyint NOT NULL,
  `symbol` tinyint NOT NULL,
  `attribute` tinyint NOT NULL,
  `value` tinyint NOT NULL,
  `unit` tinyint NOT NULL,
  `date_value` tinyint NOT NULL,
  `date_id` tinyint NOT NULL,
  `period` tinyint NOT NULL,
  `file_date_id` tinyint NOT NULL,
  `eh_sk` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `gaap_value`
--

DROP TABLE IF EXISTS `gaap_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gaap_value` (
  `gaap_sk` int(11) NOT NULL AUTO_INCREMENT,
  `company_sk` int(11) NOT NULL,
  `attribute` varchar(1024) NOT NULL,
  `unit` varchar(45) DEFAULT NULL,
  `date_id` bigint(20) NOT NULL,
  `value` varchar(45) DEFAULT NULL,
  `file_date_id` bigint(20) DEFAULT NULL,
  `period` char(6) DEFAULT NULL,
  `load_tsp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `source` char(1) DEFAULT NULL,
  `date_value` varchar(45) DEFAULT NULL,
  `new_info` tinyint(1) DEFAULT NULL,
  `eh_sk` int(11) DEFAULT NULL,
  PRIMARY KEY (`gaap_sk`),
  KEY `company_sk` (`company_sk`),
  KEY `file_date_id` (`file_date_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18558015 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `google_scrape`
--

DROP TABLE IF EXISTS `google_scrape`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `google_scrape` (
  `google_idasset_value` int(11) NOT NULL AUTO_INCREMENT,
  `date_id` bigint(20) DEFAULT NULL,
  `asset` varchar(45) DEFAULT NULL,
  `exchange` varchar(45) DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `volume` int(11) DEFAULT NULL,
  PRIMARY KEY (`google_idasset_value`),
  UNIQUE KEY `uc_googleAssetDateID` (`asset`,`date_id`),
  KEY `google_asset_index` (`asset`),
  KEY `google_asset_date_index` (`date_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10700255 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `histprice`
--

DROP TABLE IF EXISTS `histprice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `histprice` (
  `histprice_sk` int(11) NOT NULL AUTO_INCREMENT,
  `bar_length` varchar(10) NOT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  `symbol_sk` int(11) NOT NULL,
  `instant` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `type` varchar(1) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`histprice_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=2336836 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `histprice_bkp`
--

DROP TABLE IF EXISTS `histprice_bkp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `histprice_bkp` (
  `histprice_sk` int(11) NOT NULL DEFAULT '0',
  `eh_sk` int(11) NOT NULL,
  `bar_length` varchar(10) NOT NULL,
  `instant` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `volume` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `histprice_eh`
--

DROP TABLE IF EXISTS `histprice_eh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `histprice_eh` (
  `histprice_sk` int(11) NOT NULL DEFAULT '0',
  `eh_sk` int(11) NOT NULL,
  `bar_length` varchar(10) NOT NULL,
  `instant` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `volume` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `html_ins_value`
--

DROP TABLE IF EXISTS `html_ins_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `html_ins_value` (
  `ins_sk` int(11) NOT NULL AUTO_INCREMENT,
  `company_sk` int(11) NOT NULL,
  `attribute` varchar(256) NOT NULL,
  `date_id` bigint(20) NOT NULL,
  `value` varchar(45) DEFAULT NULL,
  `period` char(6) DEFAULT NULL,
  `load_tsp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `date_instant` varchar(45) DEFAULT NULL,
  `date_start` varchar(45) DEFAULT NULL,
  `date_end` varchar(45) DEFAULT NULL,
  `form` varchar(32) NOT NULL DEFAULT '10-Q',
  PRIMARY KEY (`ins_sk`),
  UNIQUE KEY `uc_gaap_natural` (`company_sk`,`attribute`,`date_id`,`form`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `imap`
--

DROP TABLE IF EXISTS `imap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `imap` (
  `imap_sk` int(11) NOT NULL AUTO_INCREMENT,
  `company_sk` int(11) DEFAULT NULL,
  `i_attribute` varchar(256) NOT NULL,
  `filing_attribute` varchar(256) NOT NULL,
  `source` char(1) DEFAULT NULL,
  `type` char(1) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  PRIMARY KEY (`imap_sk`),
  UNIQUE KEY `uc_imap_natural_1` (`company_sk`,`i_attribute`,`priority`,`source`)
) ENGINE=InnoDB AUTO_INCREMENT=217 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `index_value`
--

DROP TABLE IF EXISTS `index_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `index_value` (
  `idasset_value` int(11) NOT NULL DEFAULT '0',
  `date_id` bigint(20) DEFAULT NULL,
  `asset` varchar(45) DEFAULT NULL,
  `exchange` varchar(45) DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `volume` int(11) DEFAULT NULL,
  `change` double DEFAULT NULL,
  `percent_change` double DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `ins_map`
--

DROP TABLE IF EXISTS `ins_map`;
/*!50001 DROP VIEW IF EXISTS `ins_map`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `ins_map` (
  `eh_sk` tinyint NOT NULL,
  `cik` tinyint NOT NULL,
  `company_sk` tinyint NOT NULL,
  `symbol` tinyint NOT NULL,
  `exchange` tinyint NOT NULL,
  `sic` tinyint NOT NULL,
  `form` tinyint NOT NULL,
  `attribute` tinyint NOT NULL,
  `value` tinyint NOT NULL,
  `load_tsp` tinyint NOT NULL,
  `date_id` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `ins_modify`
--

DROP TABLE IF EXISTS `ins_modify`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ins_modify` (
  `insm_sk` int(11) NOT NULL,
  `company_sk` int(11) NOT NULL,
  `attribute` varchar(256) NOT NULL,
  `date_id` bigint(20) NOT NULL,
  `value` varchar(45) DEFAULT NULL,
  `period` char(6) DEFAULT NULL,
  `load_tsp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `date_instant` varchar(45) DEFAULT NULL,
  `date_start` varchar(45) DEFAULT NULL,
  `date_end` varchar(45) DEFAULT NULL,
  `form` varchar(32) NOT NULL DEFAULT '10-Q',
  PRIMARY KEY (`insm_sk`),
  UNIQUE KEY `uc_gaap_natural` (`company_sk`,`attribute`,`date_id`,`form`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ins_value`
--

DROP TABLE IF EXISTS `ins_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ins_value` (
  `ins_sk` int(11) NOT NULL AUTO_INCREMENT,
  `company_sk` int(11) NOT NULL,
  `attribute` varchar(256) NOT NULL,
  `date_id` bigint(20) NOT NULL,
  `value` varchar(45) DEFAULT NULL,
  `period` char(6) DEFAULT NULL,
  `load_tsp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `date_instant` varchar(45) DEFAULT NULL,
  `date_start` varchar(45) DEFAULT NULL,
  `date_end` varchar(45) DEFAULT NULL,
  `form` varchar(32) NOT NULL,
  `eh_sk` int(11) NOT NULL,
  PRIMARY KEY (`ins_sk`),
  UNIQUE KEY `uc_gaap_natural` (`company_sk`,`attribute`,`date_id`,`form`)
) ENGINE=InnoDB AUTO_INCREMENT=241529 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `iset`
--

DROP TABLE IF EXISTS `iset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iset` (
  `iset_sk` int(11) NOT NULL AUTO_INCREMENT,
  `i_attribute` varchar(256) NOT NULL,
  `priority` int(11) DEFAULT NULL,
  `num_dates` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`iset_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `merchant`
--

DROP TABLE IF EXISTS `merchant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `merchant` (
  `merchant_sk` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `SIC` varchar(20) DEFAULT NULL,
  `symbol` varchar(45) NOT NULL,
  `exchange` varchar(45) NOT NULL,
  `active` varchar(20) DEFAULT NULL,
  `sector` varchar(20) DEFAULT NULL,
  `clean_name` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`merchant_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=11744 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `monthly_returns`
--

DROP TABLE IF EXISTS `monthly_returns`;
/*!50001 DROP VIEW IF EXISTS `monthly_returns`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `monthly_returns` (
  `year` tinyint NOT NULL,
  `month_num` tinyint NOT NULL,
  `profit` tinyint NOT NULL,
  `duration` tinyint NOT NULL,
  `fama_offset` tinyint NOT NULL,
  `min_alpha` tinyint NOT NULL,
  `min_sig` tinyint NOT NULL,
  `min_assets` tinyint NOT NULL,
  `max_assets` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `numbers`
--

DROP TABLE IF EXISTS `numbers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `numbers` (
  `number` bigint(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `numbers_small`
--

DROP TABLE IF EXISTS `numbers_small`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `numbers_small` (
  `number` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `old_fama`
--

DROP TABLE IF EXISTS `old_fama`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `old_fama` (
  `idfama` int(11) NOT NULL DEFAULT '0',
  `mrkt_rf` double DEFAULT NULL,
  `smb` double DEFAULT NULL,
  `hml` double DEFAULT NULL,
  `rf` double DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `price`
--

DROP TABLE IF EXISTS `price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `price` (
  `price_sk` int(11) NOT NULL AUTO_INCREMENT,
  `eh_sk` int(11) NOT NULL,
  `price` double DEFAULT NULL,
  `neg1hour` double DEFAULT NULL,
  `neg1hourmin` double DEFAULT NULL,
  `neg1hourmax` double DEFAULT NULL,
  `pos1hour` double DEFAULT NULL,
  `pos1hourmin` double DEFAULT NULL,
  `pos1hourmax` double DEFAULT NULL,
  `neg4hour` double DEFAULT NULL,
  `neg4hourmin` double DEFAULT NULL,
  `neg4hourmax` double DEFAULT NULL,
  `pos4hour` double DEFAULT NULL,
  `pos4hourmin` double DEFAULT NULL,
  `pos4hourmax` double DEFAULT NULL,
  PRIMARY KEY (`price_sk`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sic_ref`
--

DROP TABLE IF EXISTS `sic_ref`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sic_ref` (
  `sic_sk` int(11) NOT NULL AUTO_INCREMENT,
  `sic` int(4) NOT NULL,
  `sic_name` varchar(45) NOT NULL,
  PRIMARY KEY (`sic_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=445 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `symbol`
--

DROP TABLE IF EXISTS `symbol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symbol` (
  `symbol_sk` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `symbol` varchar(45) NOT NULL,
  `exchange` varchar(45) NOT NULL,
  `cik` varchar(20) DEFAULT NULL,
  `start_date_id` bigint(20) NOT NULL,
  `end_date_id` bigint(20) DEFAULT NULL,
  `current` tinyint(4) NOT NULL,
  `SIC` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`symbol_sk`),
  UNIQUE KEY `uc_symbol_natural` (`symbol`,`exchange`,`current`),
  KEY `symbol` (`symbol`),
  KEY `cik` (`cik`),
  KEY `start_date_id` (`start_date_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9031 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `symbol_09232014`
--

DROP TABLE IF EXISTS `symbol_09232014`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symbol_09232014` (
  `symbol_sk` int(11) NOT NULL DEFAULT '0',
  `name` varchar(256) DEFAULT NULL,
  `symbol` varchar(45) NOT NULL,
  `exchange` varchar(45) NOT NULL,
  `cik` varchar(20) DEFAULT NULL,
  `start_date_id` bigint(20) NOT NULL,
  `end_date_id` bigint(20) DEFAULT NULL,
  `current` tinyint(4) NOT NULL,
  `SIC` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `symbol_history`
--

DROP TABLE IF EXISTS `symbol_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symbol_history` (
  `symbolhs_sk` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(45) NOT NULL,
  `exchange` varchar(45) NOT NULL,
  `date_id` bigint(20) NOT NULL,
  PRIMARY KEY (`symbolhs_sk`),
  UNIQUE KEY `uc_symbol_natural` (`symbol`,`exchange`,`date_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17079934 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `symbol_map`
--

DROP TABLE IF EXISTS `symbol_map`;
/*!50001 DROP VIEW IF EXISTS `symbol_map`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `symbol_map` (
  `symbol` tinyint NOT NULL,
  `exchange` tinyint NOT NULL,
  `sic` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `company_sk` tinyint NOT NULL,
  `cik` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `symbol_price`
--

DROP TABLE IF EXISTS `symbol_price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symbol_price` (
  `sp_sk` int(8) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `volume` int(8) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `date_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`sp_sk`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `symbol_price_hist`
--

DROP TABLE IF EXISTS `symbol_price_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symbol_price_hist` (
  `sph_sk` int(8) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `volume` int(8) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `date_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`sph_sk`),
  KEY `symbol` (`symbol`),
  KEY `date_id` (`date_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10528009 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `symbol_price_hist_extract`
--

DROP TABLE IF EXISTS `symbol_price_hist_extract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symbol_price_hist_extract` (
  `sphe_sk` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) DEFAULT NULL,
  `eh_sk` int(11) NOT NULL,
  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `price` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  PRIMARY KEY (`sphe_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=5641 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `symbol_price_test`
--

DROP TABLE IF EXISTS `symbol_price_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symbol_price_test` (
  `sp_sk` int(8) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `volume` int(8) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `date_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`sp_sk`),
  KEY `symbol` (`symbol`),
  KEY `price_ts` (`price_ts`),
  KEY `price_ts_2` (`price_ts`),
  KEY `symbol_2` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=9349070 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `symbol_ticker`
--

DROP TABLE IF EXISTS `symbol_ticker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symbol_ticker` (
  `st_sk` int(11) NOT NULL AUTO_INCREMENT,
  `ft_sk` int(11) DEFAULT NULL,
  `symbol` varchar(8) DEFAULT NULL,
  `instance_id` int(4) DEFAULT NULL,
  `tickerId` int(4) DEFAULT NULL,
  PRIMARY KEY (`st_sk`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ticker_price`
--

DROP TABLE IF EXISTS `ticker_price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticker_price` (
  `tp_sk` int(11) NOT NULL AUTO_INCREMENT,
  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `price` double DEFAULT NULL,
  `instance_id` int(4) DEFAULT NULL,
  `tickerId` int(4) DEFAULT NULL,
  PRIMARY KEY (`tp_sk`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trade`
--

DROP TABLE IF EXISTS `trade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trade` (
  `trade_sk` int(11) NOT NULL AUTO_INCREMENT,
  `trade_date_id` bigint(20) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  `initiation_ts` datetime DEFAULT NULL,
  `execution_ts` datetime DEFAULT NULL,
  `reverse_trade_sk` datetime DEFAULT NULL,
  `asset` varchar(45) DEFAULT NULL,
  `exchange` varchar(45) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `shares` int(11) DEFAULT NULL,
  PRIMARY KEY (`trade_sk`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trade_action`
--

DROP TABLE IF EXISTS `trade_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trade_action` (
  `ta_sk` int(8) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) DEFAULT NULL,
  `action` varchar(20) DEFAULT NULL,
  `inquiry_date` varchar(10) DEFAULT NULL,
  `state` int(4) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ta_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=66801 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trade_action_archive`
--

DROP TABLE IF EXISTS `trade_action_archive`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trade_action_archive` (
  `ta_sk` int(8) NOT NULL DEFAULT '0',
  `symbol` varchar(10) DEFAULT NULL,
  `action` varchar(10) DEFAULT NULL,
  `state` int(4) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trade_action_pre_history`
--

DROP TABLE IF EXISTS `trade_action_pre_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trade_action_pre_history` (
  `ta_sk` int(8) NOT NULL DEFAULT '0',
  `symbol` varchar(10) DEFAULT NULL,
  `action` varchar(10) DEFAULT NULL,
  `state` int(4) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `price_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `twitter_feed`
--

DROP TABLE IF EXISTS `twitter_feed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `twitter_feed` (
  `tf_sk` int(8) NOT NULL AUTO_INCREMENT,
  `text` varchar(40) DEFAULT NULL,
  `state` int(4) DEFAULT NULL,
  `date_id` bigint(20) DEFAULT NULL,
  `feed_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`tf_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `validation`
--

DROP TABLE IF EXISTS `validation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `validation` (
  `v_sk` int(11) NOT NULL AUTO_INCREMENT,
  `company_sk` int(11) NOT NULL,
  `status` varchar(2) NOT NULL,
  `date_id` bigint(20) NOT NULL,
  `stamp_created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `stamp_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `form` varchar(32) NOT NULL,
  `eh_sk` int(11) DEFAULT NULL,
  PRIMARY KEY (`v_sk`)
) ENGINE=InnoDB AUTO_INCREMENT=18283 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `yahoo_scrape`
--

DROP TABLE IF EXISTS `yahoo_scrape`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `yahoo_scrape` (
  `yahoo_idasset_value` int(11) NOT NULL AUTO_INCREMENT,
  `date_id` bigint(20) DEFAULT NULL,
  `asset` varchar(45) DEFAULT NULL,
  `exchange` varchar(45) DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `volume` int(11) DEFAULT NULL,
  PRIMARY KEY (`yahoo_idasset_value`),
  UNIQUE KEY `uc_yahooAssetDateID` (`asset`,`date_id`),
  KEY `yahoo_asset_index` (`asset`),
  KEY `yahoo_asset_date_index` (`date_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58793809 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `yearly_returns`
--

DROP TABLE IF EXISTS `yearly_returns`;
/*!50001 DROP VIEW IF EXISTS `yearly_returns`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `yearly_returns` (
  `year` tinyint NOT NULL,
  `profit` tinyint NOT NULL,
  `duration` tinyint NOT NULL,
  `fama_offset` tinyint NOT NULL,
  `min_alpha` tinyint NOT NULL,
  `min_sig` tinyint NOT NULL,
  `min_assets` tinyint NOT NULL,
  `max_assets` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `asset_value_dated`
--

/*!50001 DROP TABLE IF EXISTS `asset_value_dated`*/;
/*!50001 DROP VIEW IF EXISTS `asset_value_dated`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `asset_value_dated` AS select `av`.`idasset_value` AS `idasset_value`,`av`.`asset` AS `asset`,`av`.`exchange` AS `exchange`,`av`.`open` AS `open`,`av`.`close` AS `close`,`av`.`change` AS `change`,`av`.`percent_change` AS `percent_change`,`av`.`volume` AS `volume`,`av`.`date_id` AS `date_id`,`dates`.`date` AS `date` from (`asset_value` `av` join `dates`) where (`av`.`date_id` = `dates`.`date_id`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `daily_dated_returns`
--

/*!50001 DROP TABLE IF EXISTS `daily_dated_returns`*/;
/*!50001 DROP VIEW IF EXISTS `daily_dated_returns`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `daily_dated_returns` AS select `dates`.`date` AS `date`,sum(`daily_returns`.`profit`) AS `profit`,`daily_returns`.`duration` AS `duration`,`daily_returns`.`amount` AS `amount`,`daily_returns`.`fama_offset` AS `fama_offset`,`daily_returns`.`min_alpha` AS `min_alpha`,`daily_returns`.`min_sig` AS `min_sig`,`daily_returns`.`min_assets` AS `min_assets`,`daily_returns`.`max_assets` AS `max_assets` from (`dates` join `daily_returns`) where (`dates`.`date_id` = `daily_returns`.`date_id`) group by `dates`.`date`,`daily_returns`.`duration`,`daily_returns`.`fama_offset`,`daily_returns`.`min_alpha`,`daily_returns`.`min_sig`,`daily_returns`.`min_assets`,`daily_returns`.`max_assets`,`daily_returns`.`amount` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `daily_dated_summed_returns`
--

/*!50001 DROP TABLE IF EXISTS `daily_dated_summed_returns`*/;
/*!50001 DROP VIEW IF EXISTS `daily_dated_summed_returns`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `daily_dated_summed_returns` AS select `dates`.`date` AS `date`,sum(`daily_returns`.`profit`) AS `amount`,`daily_returns`.`duration` AS `duration`,`daily_returns`.`fama_offset` AS `fama_offset`,`daily_returns`.`min_alpha` AS `min_alpha`,`daily_returns`.`min_sig` AS `min_sig`,`daily_returns`.`min_assets` AS `min_assets`,`daily_returns`.`max_assets` AS `max_assets` from (`dates` join `daily_returns`) where (`dates`.`date_id` = `daily_returns`.`date_id`) group by `dates`.`date`,`daily_returns`.`duration`,`daily_returns`.`fama_offset`,`daily_returns`.`min_alpha`,`daily_returns`.`min_sig`,`daily_returns`.`min_assets`,`daily_returns`.`max_assets` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `daily_volume`
--

/*!50001 DROP TABLE IF EXISTS `daily_volume`*/;
/*!50001 DROP VIEW IF EXISTS `daily_volume`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `daily_volume` AS select `av`.`date_id` AS `date_id`,`dates`.`date` AS `date`,sum(`av`.`volume`) AS `sum(av.volume)` from (`dates` join `asset_value` `av`) where (`av`.`date_id` = `dates`.`date_id`) group by `av`.`date_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `dr`
--

/*!50001 DROP TABLE IF EXISTS `dr`*/;
/*!50001 DROP VIEW IF EXISTS `dr`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `dr` AS select `daily_returns`.`iddr_value` AS `iddr_value`,`daily_returns`.`date_id` AS `date_id`,`daily_returns`.`allocation` AS `allocation`,`daily_returns`.`duration` AS `duration`,`daily_returns`.`fama_offset` AS `fama_offset`,`daily_returns`.`min_alpha` AS `min_alpha`,`daily_returns`.`min_sig` AS `min_sig`,`daily_returns`.`min_assets` AS `min_assets`,`daily_returns`.`max_assets` AS `max_assets`,`daily_returns`.`asset` AS `asset`,`daily_returns`.`trade` AS `trade`,`daily_returns`.`buy` AS `buy`,`daily_returns`.`sell` AS `sell`,`daily_returns`.`profit` AS `profit` from `daily_returns` where ((`daily_returns`.`fama_offset` = 30) and (`daily_returns`.`duration` = 30) and (`daily_returns`.`min_alpha` = 0.005) and (`daily_returns`.`min_sig` = 2.5) and (`daily_returns`.`max_assets` = 10) and (`daily_returns`.`min_assets` = 1)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `filing_activity`
--

/*!50001 DROP TABLE IF EXISTS `filing_activity`*/;
/*!50001 DROP VIEW IF EXISTS `filing_activity`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `filing_activity` AS select `ft`.`state` AS `state`,`eh`.`name` AS `name`,`eh`.`form` AS `form`,`eh`.`status` AS `status`,`s`.`symbol` AS `symbol`,`eh`.`INSERT_TS` AS `insert_ts`,`eh`.`date_id` AS `date_id` from ((`filing_trade` `ft` join `symbol` `s`) join `extract_history` `eh`) where ((`ft`.`eh_sk` = `eh`.`eh_sk`) and (`eh`.`cik` = `s`.`cik`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `fulfilled_list`
--

/*!50001 DROP TABLE IF EXISTS `fulfilled_list`*/;
/*!50001 DROP VIEW IF EXISTS `fulfilled_list`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `fulfilled_list` AS select `ins_value`.`company_sk` AS `company_sk` from `ins_value` group by `ins_value`.`company_sk` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `gaap_map`
--

/*!50001 DROP TABLE IF EXISTS `gaap_map`*/;
/*!50001 DROP VIEW IF EXISTS `gaap_map`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `gaap_map` AS select `c`.`company_sk` AS `company_sk`,`s`.`exchange` AS `exchange`,`s`.`symbol` AS `symbol`,`g`.`attribute` AS `attribute`,`g`.`value` AS `value`,`g`.`unit` AS `unit`,`g`.`date_value` AS `date_value`,`g`.`date_id` AS `date_id`,`g`.`period` AS `period`,`g`.`file_date_id` AS `file_date_id`,`g`.`eh_sk` AS `eh_sk` from ((`symbol` `s` join `gaap_value` `g`) join `company` `c`) where ((`s`.`cik` = `c`.`cik`) and (`s`.`current` = 1) and (`c`.`company_sk` = `g`.`company_sk`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `ins_map`
--

/*!50001 DROP TABLE IF EXISTS `ins_map`*/;
/*!50001 DROP VIEW IF EXISTS `ins_map`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `ins_map` AS select `g`.`eh_sk` AS `eh_sk`,`c`.`cik` AS `cik`,`c`.`company_sk` AS `company_sk`,`s`.`symbol` AS `symbol`,`s`.`exchange` AS `exchange`,`s`.`SIC` AS `sic`,`g`.`form` AS `form`,`g`.`attribute` AS `attribute`,`g`.`value` AS `value`,`g`.`load_tsp` AS `load_tsp`,`g`.`date_id` AS `date_id` from ((`symbol` `s` join `ins_value` `g`) join `company` `c`) where ((`s`.`cik` = `c`.`cik`) and (`s`.`current` = 1) and (`c`.`company_sk` = `g`.`company_sk`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `monthly_returns`
--

/*!50001 DROP TABLE IF EXISTS `monthly_returns`*/;
/*!50001 DROP VIEW IF EXISTS `monthly_returns`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `monthly_returns` AS select `dates`.`year` AS `year`,`dates`.`month_num` AS `month_num`,sum(`daily_returns`.`profit`) AS `profit`,`daily_returns`.`duration` AS `duration`,`daily_returns`.`fama_offset` AS `fama_offset`,`daily_returns`.`min_alpha` AS `min_alpha`,`daily_returns`.`min_sig` AS `min_sig`,`daily_returns`.`min_assets` AS `min_assets`,`daily_returns`.`max_assets` AS `max_assets` from (`dates` join `daily_returns`) where (`dates`.`date_id` = `daily_returns`.`date_id`) group by `dates`.`year`,`dates`.`month_num`,`daily_returns`.`duration`,`daily_returns`.`fama_offset`,`daily_returns`.`min_alpha`,`daily_returns`.`min_sig`,`daily_returns`.`min_assets`,`daily_returns`.`max_assets` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `symbol_map`
--

/*!50001 DROP TABLE IF EXISTS `symbol_map`*/;
/*!50001 DROP VIEW IF EXISTS `symbol_map`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `symbol_map` AS select `s`.`symbol` AS `symbol`,`s`.`exchange` AS `exchange`,`s`.`SIC` AS `sic`,`c`.`name` AS `name`,`c`.`company_sk` AS `company_sk`,`c`.`cik` AS `cik` from (`symbol` `s` join `company` `c`) where ((`c`.`cik` = `s`.`cik`) and (`s`.`current` = 1)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `yearly_returns`
--

/*!50001 DROP TABLE IF EXISTS `yearly_returns`*/;
/*!50001 DROP VIEW IF EXISTS `yearly_returns`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `yearly_returns` AS select `dates`.`year` AS `year`,sum(`daily_returns`.`profit`) AS `profit`,`daily_returns`.`duration` AS `duration`,`daily_returns`.`fama_offset` AS `fama_offset`,`daily_returns`.`min_alpha` AS `min_alpha`,`daily_returns`.`min_sig` AS `min_sig`,`daily_returns`.`min_assets` AS `min_assets`,`daily_returns`.`max_assets` AS `max_assets` from (`dates` join `daily_returns`) where (`dates`.`date_id` = `daily_returns`.`date_id`) group by `dates`.`year`,`daily_returns`.`duration`,`daily_returns`.`fama_offset`,`daily_returns`.`min_alpha`,`daily_returns`.`min_sig`,`daily_returns`.`min_assets`,`daily_returns`.`max_assets` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-19 19:06:53
