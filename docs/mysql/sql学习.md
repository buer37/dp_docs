1. mysql中的关联查询(全外连接)

   1. 全外连接,顾名思义，把两张表的字段都查出来，没有对应的值就显示null，但是注意：mysql是没有全外连接的(mysql中没有full outer join关键字)，想要达到全外连接的效果，可以使用union关键字连接左外连接和右外连接。例如：


      select e.empName,d.deptName
         FROM t_employee e 
         left JOIN t_dept d
         ON e.dept = d.id
      UNION
      select e.empName,d.deptName
         FROM t_employee e 
         RIGHT JOIN t_dept d
         ON e.dept = d.id;

      如果在oracle中，直接就使用full outer join关键字连接两表就行了