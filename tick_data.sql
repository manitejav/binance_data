CREATE TABLE IF NOT EXISTS one_tick_data (   
  time        TIMESTAMPTZ NOT NULL,   
  market      TEXT        NOT NULL,   
  Open        NUMERIC  NOT NULL,   
  Close       NUMERIC  NOT NULL,
  High        NUMERIC  NOT NULL,
  Low         NUMERIC  NOT NULL,
  Volume      NUMERIC NOT NULL,
  PRIMARY KEY(time, market)
);

CREATE TABLE IF NOT EXISTS five_tick_data (   
  time        TIMESTAMPTZ NOT NULL,   
  market      TEXT        NOT NULL,   
  Open        NUMERIC  NOT NULL,   
  Close       NUMERIC  NOT NULL,
  High        NUMERIC  NOT NULL,
  Low         NUMERIC  NOT NULL,
  Volume      NUMERIC NOT NULL,
  PRIMARY KEY(time, market)
);

CREATE TABLE IF NOT EXISTS fifteen_tick_data (   
  time        TIMESTAMPTZ NOT NULL,   
  market      TEXT        NOT NULL,   
  Open        NUMERIC  NOT NULL,   
  Close       NUMERIC  NOT NULL,
  High        NUMERIC  NOT NULL,
  Low         NUMERIC  NOT NULL,
  Volume      NUMERIC NOT NULL,
  PRIMARY KEY(time, market)
);

CREATE TABLE IF NOT EXISTS thirty_tick_data (   
  time        TIMESTAMPTZ NOT NULL,   
  market      TEXT        NOT NULL,   
  Open        NUMERIC  NOT NULL,   
  Close       NUMERIC  NOT NULL,
  High        NUMERIC  NOT NULL,
  Low         NUMERIC  NOT NULL,
  Volume      NUMERIC NOT NULL,
  PRIMARY KEY(time, market)
);

CREATE TABLE IF NOT EXISTS hour_tick_data (   
  time        TIMESTAMPTZ NOT NULL,   
  market      TEXT        NOT NULL,   
  Open        NUMERIC  NOT NULL,   
  Close       NUMERIC  NOT NULL,
  High        NUMERIC  NOT NULL,
  Low         NUMERIC  NOT NULL,
  Volume      NUMERIC NOT NULL,
  PRIMARY KEY(time, market)
);

select create_hypertable('one_tick_data', 'time', if_not_exists => TRUE);

CREATE materialized view five_min_bucket with (timescaledb.continuous) as
SELECT time_bucket('5 minute', time) as bucket,
market,
SUM(volume) as volume,
MAX(high) as high,
MIN(low) as low
FROM one_tick_data
GROUP BY bucket, market;


CREATE materialized view fifteen_min_bucket with (timescaledb.continuous) as
SELECT time_bucket('15 minute', time) as bucket,
market,
SUM(volume) as volume,
MAX(high) as high,
MIN(low) as low
FROM one_tick_data
GROUP BY bucket, market;

CREATE materialized view thirty_min_bucket with (timescaledb.continuous) as
SELECT time_bucket('30 minute', time) as bucket,
market,
SUM(volume) as volume,
MAX(high) as high,
MIN(low) as low
FROM one_tick_data
GROUP BY bucket, market;

CREATE materialized view hour_bucket with (timescaledb.continuous) as
SELECT time_bucket('1 hour', time) as bucket,
market,
SUM(volume) as volume,
MAX(high) as high,
MIN(low) as low
FROM one_tick_data
GROUP BY bucket, market;


