CREATE TABLE IF NOT EXISTS traces
(
    id           VARCHAR(40) DEFAULT (uuid())          NOT NULL,
    trace        JSON                                  NOT NULL,
    trace_type   VARCHAR(100),
    service_name VARCHAR(255)                          NOT NULL,
    created_at   DATETIME    DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id, service_name)
);
