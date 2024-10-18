SELECT 
    d.department AS department,
    j.job AS job,
    SUM(CASE WHEN EXTRACT(QUARTER FROM e.hire_datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
    SUM(CASE WHEN EXTRACT(QUARTER FROM e.hire_datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
    SUM(CASE WHEN EXTRACT(QUARTER FROM e.hire_datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
    SUM(CASE WHEN EXTRACT(QUARTER FROM e.hire_datetime) = 4 THEN 1 ELSE 0 END) AS Q4
FROM 
    employees e
JOIN 
    departments d ON e.department_id = d.id
JOIN 
    jobs j ON e.job_id = j.id
WHERE 
    EXTRACT(YEAR FROM e.hire_datetime) = 2021
GROUP BY 
    d.department, j.job
ORDER BY 
    d.department, j.job;