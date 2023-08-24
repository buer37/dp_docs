### 查询

1. mysql中的关联查询(全外连接)

   1. 全外连接,顾名思义，把两张表的字段都查出来，没有对应的值就显示null，但是注意：mysql是没有全外连接的(mysql中没有full outer join关键字)，想要达到全外连接的效果，可以使用union关键字连接左外连接和右外连接。例如：
   
   ```sql
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
   ```

### 索引

1. 数据一样导致索引失效

   索引:

   ```
     KEY `idx_company_dep1_createtime` (`user_company_id`,`dep_lev_1_id`,`create_time`) USING BTREE COMMENT '公司-层级1-创建时间',
   ```

   sql:

   ```sql
   select ROUND(IFNULL(SUM(out_call_duration), 0)/60, 2) outCount , ROUND(IFNULL(SUM(in_call_duration), 0)/60, 2) inCount, create_time createTime from yunke_statement 
   where user_company_id =  '1avvm7' 
   and  dep_lev_1_id = '06224DE3F2CB47AA814E6C8097CC561A' 
   and create_time >= '2023-08-17' and create_time <= '2023-08-23' 
   group BY create_time  order by create_time asc
   ```

   - 因为user_company_id，dep_lev_1_id和字段数据完全一样，导致不能走联合索引idx_company_dep1_createtime