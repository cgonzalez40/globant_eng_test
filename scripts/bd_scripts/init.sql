CREATE TABLE IF NOT EXISTS training.departments
(
  id INT,
  department STRING
);

CREATE TABLE IF NOT EXISTS training.jobs
(
  id INT,
  job STRING
);

CREATE TABLE IF NOT EXISTS training.employees
(
  id INT,
  name STRING,
  dt TIMESTAMP,
  department_id INT,
  job_id INT

);