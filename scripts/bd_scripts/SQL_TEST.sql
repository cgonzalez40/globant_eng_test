--SQL 1
SELECT D.department ,
J.job,
count(distinct CASE  WHEN extract(QUARTER fROM dt)  = 1 THEN E.ID END) Q1,
count(distinct CASE  WHEN extract(QUARTER fROM dt)  = 2 THEN E.ID END) Q2,
count(distinct CASE  WHEN extract(QUARTER fROM dt)  = 3 THEN E.ID END) Q3,
count(distinct CASE  WHEN extract(QUARTER fROM dt)  = 4 THEN E.ID END) Q4
FROM `poc-accionclimatica-agrilac.training.employees` E
INNER JOIN `poc-accionclimatica-agrilac.training.jobs` J ON J.id = E.job_id
INNER JOIN `poc-accionclimatica-agrilac.training.departments` D ON D.id = E.department_id
where extract(YEAR fROM dt)  = 2021
GROUP BY 
D.department ,
J.job
ORDER BY 1,2;


-- SQL 2
WITH TB_HIRED AS (
SELECT 
D.id,
D.department,
COUNT(DISTINCT E.ID ) HIRED
FROM `poc-accionclimatica-agrilac.training.employees` E
INNER JOIN `poc-accionclimatica-agrilac.training.jobs` J ON J.id = E.job_id
INNER JOIN `poc-accionclimatica-agrilac.training.departments` D ON D.id = E.department_id
where extract(YEAR fROM dt)  = 2021
GROUP BY 
D.id,
D.department
ORDER BY 3 DESC)

SELECT *
FROM TB_HIRED
WHERE HIRED > (SELECT AVG(HIRED) FROM TB_HIRED);