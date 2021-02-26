insert into five_tick_data (time, market, open, close, high, low, volume)
select five_min_bucket.bucket as time, five_min_bucket.market as market,  otd1.open as open, otd2.close as close, five_min_bucket.high as high, five_min_bucket.low as low, five_min_bucket.volume as volume
from one_tick_data otd1
inner join five_min_bucket
on five_min_bucket.market=otd1.market and five_min_bucket.bucket=otd1.time and otd1.time>=NOW() - INTERVAL '1 HOURS'
inner join one_tick_data otd2
on five_min_bucket.market=otd2.market and five_min_bucket.bucket=otd2.time- INTERVAL '4 minutes' and otd2.time>=NOW() - INTERVAL '1 HOURS';

insert into fifteen_tick_data (time, market, open, close, high, low, volume)
select fifteen_min_bucket.bucket as time, fifteen_min_bucket.market as market,  otd1.open as open, otd2.close as close, fifteen_min_bucket.high as high, fifteen_min_bucket.low as low, fifteen_min_bucket.volume as volume
from one_tick_data otd1
inner join fifteen_min_bucket
on fifteen_min_bucket.market=otd1.market and fifteen_min_bucket.bucket=otd1.time and otd1.time>=NOW() - INTERVAL '1 HOURS'
inner join one_tick_data otd2
on fifteen_min_bucket.market=otd2.market and fifteen_min_bucket.bucket=otd2.time- INTERVAL '14 minutes' and otd2.time>=NOW() - INTERVAL '1 HOURS';

insert into thirty_tick_data (time, market, open, close, high, low, volume)
select thirty_min_bucket.bucket as time, thirty_min_bucket.market as market,  otd1.open as open, otd2.close as close, thirty_min_bucket.high as high, thirty_min_bucket.low as low, thirty_min_bucket.volume as volume
from one_tick_data otd1
inner join thirty_min_bucket
on thirty_min_bucket.market=otd1.market and thirty_min_bucket.bucket=otd1.time and otd1.time>=NOW() - INTERVAL '1 HOURS'
inner join one_tick_data otd2
on thirty_min_bucket.market=otd2.market and thirty_min_bucket.bucket=otd2.time- INTERVAL '29 minutes' and otd2.time>=NOW() - INTERVAL '1 HOURS';

insert into hour_tick_data (time, market, open, close, high, low, volume)
select hour_bucket.bucket as time, hour_bucket.market as market,  otd1.open as open, otd2.close as close, hour_bucket.high as high, hour_bucket.low as low, hour_bucket.volume as volume
from one_tick_data otd1
inner join hour_bucket
on hour_bucket.market=otd1.market and hour_bucket.bucket=otd1.time and otd1.time>=NOW() - INTERVAL '1 HOURS'
inner join one_tick_data otd2
on hour_bucket.market=otd2.market and hour_bucket.bucket=otd2.time- INTERVAL '59 minutes' and otd2.time>=NOW() - INTERVAL '1 HOURS';
