-- list_glam_rock_bands.sql
SELECT band_name, 
       IF(split != '0', split - formed, 2022 - formed) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
