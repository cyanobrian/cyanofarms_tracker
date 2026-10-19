-- Bar Chart Data 
/*
Get value and weight by week.
*/
WITH weeksums
     AS (SELECT   crop_name,
                  h.crop_id,
                  c.price,
                  week,
                  Round(Sum(weight) / 453.6, 2) AS "Weight (lb)"
         FROM     "Harvests" AS h
                  LEFT JOIN "Crops" AS c
                  ON c.crop_id = h.crop_id
         GROUP BY h.crop_id,
                  week,
                  c.price,
                  crop_name
         ORDER BY week,
                  h.crop_id)
  SELECT   week,
           crop_name                       AS "Crop",
           "Weight (lb)",
           Round("Weight (lb)" * price, 2) AS "Value ($)"
  FROM     weeksums
  ORDER BY week,
           crop_id;

/*
Get value and weight by date.
*/

with DaySums as (
SELECT   crop_name, h.crop_id, c.price,
         date,
         Round(Sum(weight) / 453.6, 2) AS "Weight (lb)"
FROM     "Harvests" AS h
         LEFT JOIN "Crops" AS c
         ON c.crop_id = h.crop_id
GROUP BY date,
         h.crop_id,
         c.price,
         crop_name
ORDER BY date,
         h.crop_id
)
select date, crop_name as "Crop", "Weight (lb)", round("Weight (lb)" * price, 2) as "Value ($)"
from DaySums
order by  date, crop_id; 

-- Cumulative Chart Data
/*
Get cumulative value and weight by week.
*/

WITH weeksums
     AS (SELECT   week,
                  Sum(weight / 453.6) AS "Weight (lb)",
                  Sum(weight * c.price / 453.6) AS "Value ($)"
         FROM     "Harvests" AS h
                  LEFT JOIN "Crops" AS c
                  ON h.crop_id = c.crop_id
         GROUP BY week
         ORDER BY week)
  SELECT week,
         Round(Sum("Weight (lb)") OVER (ORDER BY week), 2) AS "Cumulative Weight (lb)",
         Round(Sum("Value ($)") OVER (ORDER BY week), 2) AS "Cumulative Value ($)"
  FROM   weeksums;

/*
Get cumulative value and weight by date.
*/
WITH daysums
     AS (SELECT   date,
                  Sum(weight / 453.6) AS "Weight (lb)",
                  Sum(weight * c.price / 453.6) AS "Value ($)"
         FROM     "Harvests" AS h
                  LEFT JOIN "Crops" AS c
                  ON h.crop_id = c.crop_id
         GROUP BY date
         ORDER BY date)
  SELECT date,
         Round(Sum("Weight (lb)") OVER (ORDER BY date), 2) AS "Cumulative Weight (lb)",
         Round(Sum("Value ($)") OVER (ORDER BY date), 2) AS "Cumulative Value ($)"
  FROM   daysums;



-----------------------------------------------------------------------------------------
-- Statements for 2026 Season 
/*
Weight Metric
Display total weight of all crops in the first row and 
crop name and total weight in pounds. 
Sort in descending order 
*/
SELECT   Coalesce(crop_name, 'Total')  AS "Crop",
         Round(Sum(weight) / 453.6, 2) AS "Weight (lb)"
FROM     "Harvests" AS h
         LEFT JOIN "Crops" AS c
         ON h.crop_id = c.crop_id
GROUP BY ROLLUP(crop_name)
ORDER BY Sum(weight) DESC;


/*
Weight Metric
Display total value of all crops in the first row and 
crop name and total value in dollars.
Sort in descending order
*/

SELECT   Coalesce(crop_name, 'Total')           AS "Crop",
         Round(Sum(weight * c.price / 453.6),2) AS "Value ($)"
FROM     "Harvests" AS h
         LEFT JOIN "Crops" AS c
         ON h.crop_id = c.crop_id
GROUP BY ROLLUP(crop_name)
ORDER BY "Value ($)" DESC;

/*
Delta Metrics 
Total weight and value change in the most recent week with a harvest. 
*/
SELECT Coalesce(Round(Sum(weight / 453.6),2), 0)           AS "Weight (lb)",
       Coalesce(Round(Sum(weight * c.price / 453.6),2), 0) AS "Value ($)"
FROM   "Harvests" AS h
       LEFT JOIN "Crops" AS c
       ON h.crop_id = c.crop_id
WHERE  week = (SELECT Max(week)
               FROM   "Harvests");


-----------------------------------------------------------------------------------------
-- Statements for Past 7 Days 
/*
Weight Metric
Display total weight of all crops in the first row and 
crop name and total weight in pounds. 
Sort in descending order 
*/
SELECT    COALESCE(crop_name, 'Total')  AS "Crop",
          Round(Sum(weight) / 453.6, 2) AS "Weight (lb)"
FROM      "Harvests"                    AS h
LEFT JOIN "Crops"                       AS c
ON        h.crop_id = c.crop_id
WHERE     date >= Now() - interval '7 days'
GROUP BY  rollup(crop_name)
ORDER BY  sum(weight) DESC;


/*
Value Metric
Display total value of all crops in the first row and 
crop name and total value in dollars.
Sort in descending order
*/

SELECT    COALESCE(crop_name, 'Total')           AS "Crop",
          Round(Sum(weight * c.price / 453.6),2) AS "Value ($)"
FROM      "Harvests"                             AS h
LEFT JOIN "Crops"                                AS c
ON        h.crop_id = c.crop_id
WHERE     date >= Now() - interval '7 days'
GROUP BY  rollup(crop_name)
ORDER BY  "Value ($)" DESC;

/*
Delta Metrics 
Total weight and value change in the last 1 day. 
*/
SELECT 
         coalesce(Round(Sum(weight / 453.6),2), 0) AS "Weight (lb)",
         coalesce(Round(Sum(weight * c.price / 453.6),2), 0) AS "Value ($)"
FROM     "Harvests" AS h
         LEFT JOIN "Crops" AS c
         ON h.crop_id = c.crop_id
WHERE date >= NOW() - INTERVAL '1 days';

