-- create database job_application;
use job_application;
CREATE TABLE jobseeker (
    jobseeker_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    phone_number VARCHAR(15),
    address VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(25)
);

CREATE TABLE company (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    location VARCHAR(200)
);

CREATE TABLE job (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(50),
    job_type VARCHAR(30),
    job_description TEXT,
    job_salary VARCHAR(10),
    company_id INT,
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);

CREATE TABLE profile (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    jobseeker_id INT,
    college VARCHAR(50),
    department VARCHAR(50),
    education VARCHAR(50),
    FOREIGN KEY (jobseeker_id) REFERENCES jobseeker(jobseeker_id)
);

CREATE TABLE resume (
    resume_id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    jobseeker_id INT,
    FOREIGN KEY (jobseeker_id) REFERENCES jobseeker(jobseeker_id)
);

CREATE TABLE apply (
    jobseeker_id INT,
    job_id INT,
    FOREIGN KEY (jobseeker_id) REFERENCES jobseeker(jobseeker_id),
    FOREIGN KEY (job_id) REFERENCES job(job_id)
);

CREATE TABLE result (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    jobseeker_id INT,
    job_id INT,
    status VARCHAR(10),
    FOREIGN KEY (jobseeker_id) REFERENCES jobseeker(jobseeker_id),
    FOREIGN KEY (job_id) REFERENCES job(job_id)
);
CREATE TABLE interview (
	interview_num INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT,
    date DATE,
    time TIME,
    jobseeker_id INT,
    FOREIGN KEY (jobseeker_id) REFERENCES jobseeker(jobseeker_id),
    FOREIGN KEY (job_id) REFERENCES job(job_id)
);

-- Inserting companies
INSERT INTO company (name, location) VALUES ('Tech Solutions Inc', 'San Francisco');
INSERT INTO company (name, location) VALUES ('Innovate Labs', 'New York');
INSERT INTO company (name, location) VALUES ('CodeCrafters Ltd', 'Seattle');
INSERT INTO company (name, location) VALUES ('DataMinds Corporation', 'Los Angeles');
INSERT INTO company (name, location) VALUES ('WebGenius Innovations', 'Austin');

-- Inserting jobs for each company
-- Assuming the company_id values are assigned sequentially starting from 1
INSERT INTO job (job_title, job_type, job_description, job_salary, company_id) VALUES
  ('Software Engineer', 'Full-time', 'Develop and maintain software applications.', '80000', 1);
  
INSERT INTO job (job_title, job_type, job_description, job_salary, company_id) VALUES
  ('Data Scientist', 'Part-time', 'Analyze and interpret complex data sets.', '70000', 2);

INSERT INTO job (job_title, job_type, job_description, job_salary, company_id) VALUES
  ('Web Developer', 'Full-time', 'Build and maintain websites and web applications.', '75000', 3);

INSERT INTO job (job_title, job_type, job_description, job_salary, company_id) VALUES
  ('Network Engineer', 'Full-time', 'Design and implement computer networks.', '85000', 4);

INSERT INTO job (job_title, job_type, job_description, job_salary, company_id) VALUES
  ('UX/UI Designer', 'Part-time', 'Create user-friendly and visually appealing interfaces.', '70000', 5);
  
CREATE TABLE employer (
    employer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    phone_number VARCHAR(15),
    email VARCHAR(255),
    password VARCHAR(25),
    company_id INT,
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);

DELIMITER //
CREATE TRIGGER apply_insert_trigger
AFTER INSERT
ON apply FOR EACH ROW
BEGIN
DECLARE interview_date DATE;
DECLARE interview_time TIME;
SET interview_date = DATE_ADD(CURDATE(), INTERVAL 7 DAY);
SET interview_time = '10:00:00';
INSERT INTO interview (job_id, date, time, jobseeker_id)
VALUES (NEW.job_id, interview_date, interview_time, NEW.jobseeker_id);
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER apply_insert_trigger_result
AFTER INSERT
ON apply FOR EACH ROW
BEGIN
DECLARE sts varchar(10);
SET sts="Pending";
INSERT INTO result (jobseeker_id, job_id, status)
VALUES (NEW.jobseeker_id, NEW.job_id, sts);
END //
Delimiter ;