CREATE TABLE measurements (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	time DATETIME,
	current REAL, -- in amp
	voltage REAL, -- in volts
	battery_charge REAL, -- in amp hours
	battery_status TEXT,
	focused_window TEXT,
	screenshot BLOB
);
