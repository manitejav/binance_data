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