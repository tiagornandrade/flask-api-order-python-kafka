CREATE table if not EXISTS order (
	id TEXT,
	name TEXT,
    description TEXT,
    price FLOAT
);

CREATE table if not EXISTS transaction (
	trsansaction_id TEXT,
	transaction json
);