-- Initialize the database with tables and sample data

-- Create a schema for our application
CREATE SCHEMA IF NOT EXISTS app_data;

-- Create a function to update timestamps
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = now(); 
   RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a table for metadata about our data generation
CREATE TABLE IF NOT EXISTS app_data.metadata (
    id SERIAL PRIMARY KEY,
    last_run TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    records_generated INTEGER NOT NULL,
    generator_version VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create a trigger for the timestamp update
CREATE TRIGGER update_metadata_timestamp
BEFORE UPDATE ON app_data.metadata
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- Insert initial metadata
INSERT INTO app_data.metadata (records_generated, generator_version)
VALUES (0, '1.0.0');
