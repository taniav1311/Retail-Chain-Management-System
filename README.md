# Retail-Chain-Management-System
*Oct 2025 -  Advanced Database Management Systems Course Project*

Multi-location retail chain requires distributed management of employees, payroll, and sales data across stores. This system addresses scalability challenges in centralized databases by implementing fragmentation techniques while providing intuitive GUI access. Core objectives include full CRUD operations, data normalization, and optimized storage/retrieval for retail operations. Targets store managers tracking employee productivity and sales performance across locations like Store A and Store B.

## Key Features
- Employee CRUD with department assignment (Sales/Retail/Distribution).
- One-time payroll entry (salary + bank details) preventing redundant updates.
- Per-store sales logging (50+ shoe products, quantity, date) linked to employees.
- Real-time dashboard views joining fragmented data without backend exposure.

## Database Design
**Entities:** EmployeeBasic (id, name, department), EmployeePayroll (id, salary, bank_info), Sales (sale_id, store, product, qty, date, emp_id). Relationships via foreign keys ensure referential integrity. Normalization separates personal/contact data; sales partitioned by location. EmployeeFull view consolidates for GUI display. 

## Fragmentation Strategy
Implements distributed database optimization: **vertical** splits attributes by access patterns (EmployeeBasic_Personal vs _Contact), **horizontal** partitions sales rows by store (sales_storea/storeb). Further vertical fragmentation on sales (main: product/qty; meta: store/date/emp_id). Enables parallel processing/scalability across locations. Reconstruction via JOINs (vertical) and UNION ALL (horizontal). 

## CRUD Operations
- **CREATE:** INSERT EmployeeBasic → auto-ID; one-time EmployeePayroll; new Sales records.
- **READ:** EmployeeFull view; Sales JOIN EmployeeBasic (name visible, no sale_id).
- **UPDATE:** None (payroll immutable; matches real-world policy).
- **DELETE:** None (audit trail preservation).
