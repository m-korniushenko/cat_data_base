-- Migration to add new fields to the cat table
-- Run this SQL script in your PostgreSQL database

-- Add new columns to the cat table
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_callname VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_haritage_number_2 VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_eye_colour VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_hair_type VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_tests VARCHAR(500);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_litter_size_male INTEGER;
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_litter_size_female INTEGER;
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_blood_group VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_gencode VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_features TEXT;
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_notes TEXT;
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_show_results TEXT;
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_breeding_lock BOOLEAN DEFAULT FALSE;
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_breeding_lock_date DATE;
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_breeding_animal BOOLEAN DEFAULT FALSE;
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_birth_country VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_location VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_weight FLOAT;
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_birth_weight FLOAT;
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_transfer_weight FLOAT;
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_faults_deviations VARCHAR(500);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_association VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_jaw_fault VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_hernia VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_testicles VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_death_date DATE;
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_death_cause VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_status VARCHAR(255);
ALTER TABLE cat ADD COLUMN IF NOT EXISTS cat_kitten_transfer BOOLEAN DEFAULT FALSE;

-- Update existing records to have default values for new boolean fields
UPDATE cat SET cat_breeding_lock = FALSE WHERE cat_breeding_lock IS NULL;
UPDATE cat SET cat_breeding_animal = FALSE WHERE cat_breeding_animal IS NULL;
UPDATE cat SET cat_kitten_transfer = FALSE WHERE cat_kitten_transfer IS NULL;

-- Add comments to document the new fields
COMMENT ON COLUMN cat.cat_callname IS 'Call name or nickname of the cat';
COMMENT ON COLUMN cat.cat_haritage_number_2 IS 'Second studbook number';
COMMENT ON COLUMN cat.cat_eye_colour IS 'Eye color of the cat';
COMMENT ON COLUMN cat.cat_hair_type IS 'Type of hair (Short Hair, Long Hair, etc.)';
COMMENT ON COLUMN cat.cat_tests IS 'Medical tests performed on the cat';
COMMENT ON COLUMN cat.cat_litter_size_male IS 'Number of male kittens in litter';
COMMENT ON COLUMN cat.cat_litter_size_female IS 'Number of female kittens in litter';
COMMENT ON COLUMN cat.cat_blood_group IS 'Blood group of the cat';
COMMENT ON COLUMN cat.cat_gencode IS 'Genetic code information';
COMMENT ON COLUMN cat.cat_features IS 'Physical features and characteristics';
COMMENT ON COLUMN cat.cat_notes IS 'Additional notes about the cat';
COMMENT ON COLUMN cat.cat_show_results IS 'Show competition results';
COMMENT ON COLUMN cat.cat_breeding_lock IS 'Whether the cat has breeding restrictions';
COMMENT ON COLUMN cat.cat_breeding_lock_date IS 'Date when breeding lock was applied';
COMMENT ON COLUMN cat.cat_breeding_animal IS 'Whether the cat is used for breeding';
COMMENT ON COLUMN cat.cat_birth_country IS 'Country where the cat was born';
COMMENT ON COLUMN cat.cat_location IS 'Current location of the cat';
COMMENT ON COLUMN cat.cat_weight IS 'Current weight in kilograms';
COMMENT ON COLUMN cat.cat_birth_weight IS 'Weight at birth in grams';
COMMENT ON COLUMN cat.cat_transfer_weight IS 'Weight at transfer in grams';
COMMENT ON COLUMN cat.cat_faults_deviations IS 'Faults and deviations from breed standard';
COMMENT ON COLUMN cat.cat_association IS 'Cat association or club membership';
COMMENT ON COLUMN cat.cat_jaw_fault IS 'Jaw fault information';
COMMENT ON COLUMN cat.cat_hernia IS 'Hernia information';
COMMENT ON COLUMN cat.cat_testicles IS 'Testicles condition (for male cats)';
COMMENT ON COLUMN cat.cat_death_date IS 'Date of death';
COMMENT ON COLUMN cat.cat_death_cause IS 'Cause of death';
COMMENT ON COLUMN cat.cat_status IS 'Current status (Alive, Deceased, Missing, etc.)';
COMMENT ON COLUMN cat.cat_kitten_transfer IS 'Whether kittens were transferred';

-- Migration completed successfully
SELECT 'Migration completed successfully - new cat fields added' as result;
