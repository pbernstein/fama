select concat(substring(date_format(instant,'%T'),1,2),date_format(instant,'%i')), open from histprice where eh_sk = 'template'
