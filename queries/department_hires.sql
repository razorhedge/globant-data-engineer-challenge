WITH DepartmentHiring AS (
    SELECT 
        d.id AS department_id,
        d.department,
        COUNT(e.id) AS hired
    FROM 
        employees e
    JOIN 
        departments d ON e.department_id = d.id
    GROUP BY 
        d.id
),
AverageHiring AS (
    SELECT 
        AVG(hired) AS avg_hired
    FROM 
        DepartmentHiring
)
SELECT 
    dh.department_id AS id,
    dh.department,
    dh.hired
FROM 
    DepartmentHiring dh
JOIN 
    AverageHiring ah ON dh.hired > ah.avg_hired
ORDER BY 
    dh.hired DESC;