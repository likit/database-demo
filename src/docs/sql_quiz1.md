# เฉลยแบบทดสอบการจัดการข้อมูลด้วยภาษา SQL
## รายวิชา MTID321
### วันที่ 16/9/2565


ข้อใดคือคำสั่งในการดูรายการผู้ป่วยที่เป็นเพศชาย

```SQL
SELECT *
  FROM patients
 WHERE gender = 'm';
 ```

ข้อใดคือคำสั่งสำหรับการดูข้อมูลเพศและวันเดือนปีเกิดของผู้ป่วย

```SQL
SELECT gender,
       dob
  FROM patients;
```

ข้อใดคือคำสั่งเพื่อแสดงรายชื่อแพทย์และสังกัด

```SQL
SELECT firstname,
       lastname,
       department_code
  FROM doctors;
```

ข้อใดคือคำสั่งสำหรับหาจำนวนแพทย์ในสังกัด Orthopedics

```SQL
SELECT count( * ) 
  FROM doctors
 WHERE department_code = 'OTH'
 GROUP BY department_code;
```

หรือใช้ชื่อเต็มของสังกัดในการกำหนดเงื่อนไข ทั้งนี้ต้องทำการ join ข้อมูลกับตาราง departments ด้วยเพื่อสามารถดูชื่อเต็มได้

```SQL
SELECT count( * ) 
  FROM doctors
       JOIN
       departments ON departments.code = doctors.department_code
 WHERE departments.name = 'Orthopedics'
 GROUP BY departments.name;
```


จำนวนผู้ป่วยที่มีชื่อขึ้นต้นด้วย And มีจำนวนเท่าใด

```SQL
SELECT *
  FROM patients
 WHERE firstname LIKE 'And%';
```

ข้อใดคือชื่อผู้ป่วยลำดับที่ 7 หากเรียงจากชื่อจริงตามตัวอักษร

```SQL
SELECT *
  FROM patients
 ORDER BY firstname
 LIMIT 7;
```

ข้อใดคือจำนวนการเข้าโรงพยาบาล (visit) ที่มากที่สุดต่อคน

```SQL
SELECT count( * ) 
  FROM visits
 GROUP BY patient_hn
 ORDER BY count( * ) DESC;
```

ข้อใดคือชื่อผู้ป่วยที่เข้ามาโรงพยาบาลมากที่สุด

```SQL
SELECT count( * ),
       firstname,
       lastname
  FROM visits
       JOIN
       patients ON visits.patient_hn = patients.hn
 GROUP BY patient_hn
 ORDER BY count( * ) DESC;
```

รายการทดสอบใดที่มีจำนวนการสั่งมากที่สุด

```SQL
SELECT count( * ),
       name
  FROM test_lab_order_assoc
       JOIN
       tests ON tests.id = test_lab_order_assoc.test_id
 GROUP BY name
 ORDER BY count( * ) DESC;
```

รายการทดสอบใดมีรายรับมากที่สุด

```SQL
SELECT sum(price),
       name
  FROM test_lab_order_assoc
       JOIN
       tests ON tests.id = test_lab_order_assoc.test_id
 GROUP BY name
 ORDER BY sum(price) DESC;
```

รายการทดสอบใดมีรายรับมากกว่า 15000

```SQL
SELECT sum(price),
       name
  FROM test_lab_order_assoc
       JOIN
       tests ON tests.id = test_lab_order_assoc.test_id
 GROUP BY name
HAVING sum(price) > 15000
 ORDER BY sum(price) DESC;
```

หรือ ตั้งชื่อคอลัมน์ให้มีความหมายเพื่อความสะดวกในการอ่านคำสั่ง ดังตัวอย่างเป็นการตั้งชื่อคอลัมน์ sum(price) เป็น revenue

```SQL
SELECT sum(price) as revenue,
       name
  FROM test_lab_order_assoc
       JOIN
       tests ON tests.id = test_lab_order_assoc.test_id
 GROUP BY name
HAVING revenue > 15000
 ORDER BY revenue DESC;
```

แพทย์ในด้านใดสั่งตรวจทางห้องปฏิบัติการมากที่สุด

```SQL
SELECT count( * ),
       department_code
  FROM lab_orders
       JOIN
       doctors ON doctors.id = lab_orders.doctor_id
 GROUP BY department_code
 ORDER BY count( * ) DESC;
```