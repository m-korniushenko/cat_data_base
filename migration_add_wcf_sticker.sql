-- Migration to add WCF Sticker field to the cat table
-- Run this SQL script in your PostgreSQL database

-- Add WCF Sticker column to the cat table
ALTER TABLE cat ADD COLUMN IF NOT EXISTS wcf_sticker BOOLEAN DEFAULT FALSE;

-- Update existing records to have default value for WCF Sticker field
UPDATE cat SET wcf_sticker = FALSE WHERE wcf_sticker IS NULL;

-- Add comment to document the new field
COMMENT ON COLUMN cat.wcf_sticker IS 'WCF Sticker information';

-- Migration completed successfully
SELECT 'Migration completed successfully - WCF Sticker field added' as result;
