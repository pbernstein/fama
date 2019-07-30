/* Adapted from Tom Cunningham's 'Data Warehousing with MySql' (www.meansandends.com/mysql-data-warehouse) */

###### small-numbers table
DROP TABLE IF EXISTS numbers_small;
CREATE TABLE numbers_small (number INT);
INSERT INTO numbers_small VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9);

###### main numbers table
DROP TABLE IF EXISTS numbers;
CREATE TABLE numbers (number BIGINT);
INSERT INTO numbers
SELECT thousands.number * 1000 + hundreds.number * 100 + tens.number * 10 + ones.number
  FROM numbers_small thousands, numbers_small hundreds, numbers_small tens, numbers_small ones
LIMIT 1000000;

###### date table
DROP TABLE IF EXISTS dates;

#CREATE TABLE dates (
#  date_id          BIGINT PRIMARY KEY, 
#  date             DATE NOT NULL,
#  timestamp        BIGINT NOT NULL, 
#  weekend          CHAR(10) NOT NULL DEFAULT "Weekday",
#  day_of_week      CHAR(10) NOT NULL,
#  month            CHAR(10) NOT NULL,
#  month_day        INT NOT NULL, 
#  month_num        INT NOT NULL,
#  year             INT NOT NULL,
#  week_starting_monday CHAR(2) NOT NULL,
#  dow_num          INT NOT NULL,
#  UNIQUE KEY `date` (`date`),
#  KEY `year_week` (`year`,`week_starting_monday`)
#);


CREATE TABLE `dates` (
  `date_id` bigint NOT NULL,
  `date` date NOT NULL,
  `timestamp` bigint NOT NULL,
  `weekend` char(10) NOT NULL DEFAULT 'Weekday',
  `day_of_week` char(10) NOT NULL,
  `month` char(10) NOT NULL,
  `month_day` int NOT NULL,
  `year` int NOT NULL,
  `week_starting_monday` char(2) NOT NULL,
  `month_num` int DEFAULT NULL,
  `dow_num` int DEFAULT NULL,
  PRIMARY KEY (`date_id`),
  UNIQUE KEY `date` (`date`),
  KEY `year_week` (`year`,`week_starting_monday`),
  KEY `dates_dateid_index` (`date_id`),
  KEY `dates_date_index` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

###### populate it with days
INSERT INTO dates (date_id, date)
SELECT number, DATE_ADD( '1990-01-01', INTERVAL number DAY )
  FROM numbers
  WHERE DATE_ADD( '1990-01-01', INTERVAL number DAY ) BETWEEN '1990-01-01' AND '2020-01-01'
  ORDER BY number;

###### fill in other rows
UPDATE dates SET
  timestamp =   UNIX_TIMESTAMP(date),
  day_of_week = DATE_FORMAT( date, "%W" ),
  weekend =     IF( DATE_FORMAT( date, "%W" ) IN ('Saturday','Sunday'), 'Weekend', 'Weekday'),
  month =       DATE_FORMAT( date, "%M"),
  month_num =       DATE_FORMAT( date, "%m"),
  year =        DATE_FORMAT( date, "%Y" ),
  month_day =   DATE_FORMAT( date, "%d" );
#  dow_num =     CASE DATE_FORMAT( date, "%W" ) WHEN ('Monday')  THEN 1  WHEN ('Tuesday') THEN 2 WHEN ('Wednesday') THEN 3 WHEN ('Thursday') THEN 4 WHEN ('Friday') THEN 5 WHEN ('Saturday') THEN 6 WHEN ('Sunday') THEN 7;

UPDATE dates SET week_starting_monday = DATE_FORMAT(date,'%v');
update dates set dow_num = 1 where day_of_week = 'Monday';
update dates set dow_num = 2 where day_of_week = 'Tuesday';
update dates set dow_num = 3 where day_of_week = 'Wednesday';
update dates set dow_num = 4 where day_of_week = 'Thursday';
update dates set dow_num = 5 where day_of_week = 'Friday';
update dates set dow_num = 6 where day_of_week = 'Saturday';
update dates set dow_num = 7 where day_of_week = 'Sunday';
