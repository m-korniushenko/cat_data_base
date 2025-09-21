-- Migration to change WCF Sticker field type from Boolean to String
-- Run this SQL script in your PostgreSQL database

-- First, add a new temporary column with the new type
ALTER TABLE cat ADD COLUMN IF NOT EXISTS wcf_sticker_temp VARCHAR(255);

-- Copy data from old column to new column (convert boolean to string)
UPDATE cat SET wcf_sticker_temp = CASE 
    WHEN wcf_sticker = true THEN 'Yes'
    WHEN wcf_sticker = false THEN 'No'
    ELSE NULL
END;

-- Drop the old column
ALTER TABLE cat DROP COLUMN IF EXISTS wcf_sticker;

-- Rename the new column to the original name
ALTER TABLE cat RENAME COLUMN wcf_sticker_temp TO wcf_sticker;

-- Add comment to document the field
COMMENT ON COLUMN cat.wcf_sticker IS 'WCF Sticker number or identifier';

-- Migration completed successfully
SELECT 'Migration completed successfully - WCF Sticker field type changed to String' as result;
