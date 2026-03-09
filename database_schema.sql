/* ============================================================
   Event Registration & Attendance System
   Microsoft Access SQL Schema
   ============================================================ */

/* --- users ------------------------------------------------- */
CREATE TABLE users (
    id             AUTOINCREMENT  CONSTRAINT pk_users PRIMARY KEY,
    name           TEXT(255)      NOT NULL,
    email          TEXT(255)      NOT NULL,
    email_verified DATETIME,
    password       TEXT(255)      NOT NULL,
    remember_token TEXT(100),
    created_at     DATETIME,
    updated_at     DATETIME,
    CONSTRAINT uq_users_email UNIQUE (email)
);

/* --- events ------------------------------------------------ */
CREATE TABLE events (
    id         AUTOINCREMENT  CONSTRAINT pk_events PRIMARY KEY,
    title      TEXT(255)      NOT NULL,
    event_date DATETIME       NOT NULL,
    event_time TEXT(20)       NOT NULL,
    location   TEXT(255)      NOT NULL,
    created_at DATETIME,
    updated_at DATETIME
);

/* --- registrations ---------------------------------------- */
CREATE TABLE registrations (
    id            AUTOINCREMENT  CONSTRAINT pk_registrations PRIMARY KEY,
    event_id      LONG           NOT NULL,
    student_id    TEXT(255)      NOT NULL,
    name          TEXT(255)      NOT NULL,
    email         TEXT(255)      NOT NULL,
    qr_token      TEXT(255)      NOT NULL,
    checked_in_at DATETIME,
    created_at    DATETIME,
    updated_at    DATETIME,
    CONSTRAINT fk_reg_event    FOREIGN KEY (event_id) REFERENCES events (id),
    CONSTRAINT uq_reg_qr_token UNIQUE (qr_token),
    CONSTRAINT uq_reg_student  UNIQUE (event_id, student_id)
);

/* ============================================================
   Laravel Framework Tables (optional — include if needed)
   ============================================================ */

CREATE TABLE password_reset_tokens (
    email      TEXT(255)  CONSTRAINT pk_prt PRIMARY KEY,
    token      TEXT(255)  NOT NULL,
    created_at DATETIME
);

CREATE TABLE sessions (
    id            TEXT(255)  CONSTRAINT pk_sessions PRIMARY KEY,
    user_id       LONG,
    ip_address    TEXT(45),
    user_agent    MEMO,
    payload       MEMO       NOT NULL,
    last_activity LONG       NOT NULL
);

CREATE TABLE cache (
    cache_key  TEXT(255)  CONSTRAINT pk_cache PRIMARY KEY,
    value      MEMO       NOT NULL,
    expiration LONG       NOT NULL
);

CREATE TABLE jobs (
    id           AUTOINCREMENT  CONSTRAINT pk_jobs PRIMARY KEY,
    queue        TEXT(255)      NOT NULL,
    payload      MEMO           NOT NULL,
    attempts     BYTE           NOT NULL,
    reserved_at  LONG,
    available_at LONG           NOT NULL,
    created_at   LONG           NOT NULL
);
