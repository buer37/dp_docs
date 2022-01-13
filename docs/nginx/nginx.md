1. nginx

   ```
   nginx中的location ~ .*，请问这个.*是什么意思？
   location ~ .*.(jpg|jpeg|JPG|png|gif|icon)$ {
   	...
   }
   
   ```

   

   `~` 表示大小写敏感正则匹配，`.` 表示任意字符，`*` 表示出现0或者任意次

   上面的正则中包含`.*`是多余的，第2个`.`需要加上转义字符

   修改后的匹配规则

   `location ~ \.(jpg|jpeg|JPG|png|gif|icon)$`

