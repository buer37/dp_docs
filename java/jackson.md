# springboot jackson 配置

springboot 默认使用jackson 进行序列化和反序列化，当我们引入spring-boot-starter-web 依赖的时候就自动引入了jackson 相关依赖，并且对jackson进行了自动装配，并且有默认的Jackson 配置，自动装配类：JacksonAutoConfiguration

springboot jackson 配置

## **修改jackson配置常用方式**

### **1. 通过 yaml 配置**

只能实现部分配置，没法配置LocalDateTime，Long精度丢失等

```text
spring:
    jackson:
      date-format: yyyy-MM-dd HH:mm:ss # 设置 java.util.Date, Calendar 序列化、反序列化的格式
      locale: zh # 当地时区
      time-zone: GMT+8 # 设置全局时区
      serialization:
        WRITE_DATES_AS_TIMESTAMPS: false # 禁止将 java.util.Date, Calendar 序列化为数字(时间戳)
        FAIL_ON_EMPTY_BEANS: false # 序列化时，对象为 null，是否抛异常
      deserialization:
        FAIL_ON_UNKNOWN_PROPERTIES: false # 反序列化时，json 中包含 pojo 不存在属性时，是否抛异常
```

### **2. 通过@Bean 注入Module对象进行扩展**

```text
    private static final String DEFAULT_DATETIME_PATTERN = "yyyy-MM-dd HH:mm:ss";
    private static final String DEFAULT_DATE_FORMAT = "yyyy-MM-dd";
    private static final String DEFAULT_TIME_FORMAT = "HH:mm:ss";

    @Bean
    public Module javaTimeModule() {
        JavaTimeModule module = new JavaTimeModule();
        // 配置 Jackson 序列化 long类型为String，解决后端返回的Long类型在前端精度丢失的问题
        module.addSerializer(BigInteger.class, BigNumberSerializer.INSTANCE);
        module.addSerializer(Long.class, BigNumberSerializer.INSTANCE);
        module.addSerializer(Long.TYPE, BigNumberSerializer.INSTANCE);

        // 配置 Jackson 序列化 LocalDateTime、LocalDate、LocalTime 时使用的格式
        module.addSerializer(new LocalDateTimeSerializer(DateTimeFormatter.ofPattern(DEFAULT_DATETIME_PATTERN)));
        module.addSerializer(new LocalDateSerializer(DateTimeFormatter.ofPattern(DEFAULT_DATE_FORMAT)));
        module.addSerializer(new LocalTimeSerializer(DateTimeFormatter.ofPattern(DEFAULT_TIME_FORMAT)));


        // 配置 Jackson 反序列化 LocalDateTime、LocalDate、LocalTime 时使用的格式
        module.addDeserializer(LocalDateTime.class, new LocalDateTimeDeserializer(DateTimeFormatter.ofPattern(DEFAULT_DATETIME_PATTERN)));
        module.addDeserializer(LocalDate.class, new LocalDateDeserializer(DateTimeFormatter.ofPattern(DEFAULT_DATE_FORMAT)));
        module.addDeserializer(LocalTime.class, new LocalTimeDeserializer(DateTimeFormatter.ofPattern(DEFAULT_TIME_FORMAT)));
        return module;
    }
```

### **3. 通过@Bean注入 Jackson2ObjectMapperBuilderCustomizer对象进行扩展**

这种方式应该是用的最多的一种

```text
 @Bean
 public Jackson2ObjectMapperBuilderCustomizer customizer() {
        return builder -> {
            // 这部分也可以在 yaml 中配置
            builder
                    // 序列化时，对象为 null，是否抛异常
                    .failOnEmptyBeans(false)
                    // 反序列化时，json 中包含 pojo 不存在属性时，是否抛异常
                    .failOnUnknownProperties(false)
                    // 禁止将 java.util.Date, Calendar 序列化为数字(时间戳)
                    .featuresToDisable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
                    // 设置 java.util.Date, Calendar 序列化、反序列化的格式
                    .dateFormat(new SimpleDateFormat(DEFAULT_DATETIME_PATTERN))
                    // 设置 java.util.Date、Calendar 序列化、反序列化的时区
                    .timeZone(TimeZone.getTimeZone("GMT+8"))
            ;
            // 配置 Jackson 序列化 BigDecimal 时使用的格式
            builder.serializerByType(BigDecimal.class, ToStringSerializer.instance);

            // 配置 Jackson 序列化 long类型为String，解决后端返回的Long类型在前端精度丢失的问题
            builder.serializerByType(BigInteger.class, BigNumberSerializer.INSTANCE);
            builder.serializerByType(Long.class, BigNumberSerializer.INSTANCE);
            builder.serializerByType(Long.TYPE, BigNumberSerializer.INSTANCE);

            // 配置 Jackson 序列化 LocalDateTime、LocalDate、LocalTime 时使用的格式
            builder.serializers(new LocalDateTimeSerializer(DateTimeFormatter.ofPattern(DEFAULT_DATETIME_PATTERN)));
            builder.serializers(new LocalDateSerializer(DateTimeFormatter.ofPattern(DEFAULT_DATE_FORMAT)));
            builder.serializers(new LocalTimeSerializer(DateTimeFormatter.ofPattern(DEFAULT_TIME_FORMAT)));


            // 配置 Jackson 反序列化 LocalDateTime、LocalDate、LocalTime 时使用的格式
            builder.deserializerByType(LocalDateTime.class, new LocalDateTimeDeserializer(DateTimeFormatter.ofPattern(DEFAULT_DATETIME_PATTERN)));
            builder.deserializerByType(LocalDate.class, new LocalDateDeserializer(DateTimeFormatter.ofPattern(DEFAULT_DATE_FORMAT)));
            builder.deserializerByType(LocalTime.class, new LocalTimeDeserializer(DateTimeFormatter.ofPattern(DEFAULT_TIME_FORMAT)));
            log.info("init jackson config");
        };
 }
```

## **扩展web Jackson自动装配**

扩展Jackson自动装配，做成自动配置common包，其它需要Jackson配置的模块，只需要导入相关包即可，主要如下

### **创建common-json包，创建自动配置类**

```text
/**
 * jackson 配置
 * 注意需要在 JacksonAutoConfiguration.class 之前进行装配，如果在它之后装配，注入的Jackson2ObjectMapperBuilderCustomizer不生效
 * @author LGC
 */
@Slf4j
@AutoConfiguration(before = JacksonAutoConfiguration.class)
public class JsonAutoConfiguration {

    private static final String DEFAULT_DATETIME_PATTERN = "yyyy-MM-dd HH:mm:ss";
    private static final String DEFAULT_DATE_FORMAT = "yyyy-MM-dd";
    private static final String DEFAULT_TIME_FORMAT = "HH:mm:ss";

  /**
     * springboot 在构建ObjectMapper时默认使用这个构建器
     *
     * @return
     */
    @Bean
    public Jackson2ObjectMapperBuilderCustomizer customizer() {
        return builder -> {
            // 这部分也可以在 yaml 中配置
            builder
                    // 序列化时，对象为 null，是否抛异常
                    .failOnEmptyBeans(false)
                    // 反序列化时，json 中包含 pojo 不存在属性时，是否抛异常
                    .failOnUnknownProperties(false)
                    // 禁止将 java.util.Date, Calendar 序列化为数字(时间戳)
                    .featuresToDisable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
                    // 设置 java.util.Date, Calendar 序列化、反序列化的格式
                    .dateFormat(new SimpleDateFormat(DEFAULT_DATETIME_PATTERN))
                    // 设置 java.util.Date、Calendar 序列化、反序列化的时区
                    .timeZone(TimeZone.getTimeZone("GMT+8"))
            ;
            // 配置 Jackson 序列化 BigDecimal 时使用的格式
            builder.serializerByType(BigDecimal.class, ToStringSerializer.instance);

            // 配置 Jackson 序列化 long类型为String，解决后端返回的Long类型在前端精度丢失的问题
            builder.serializerByType(BigInteger.class, BigNumberSerializer.INSTANCE);
            builder.serializerByType(Long.class, BigNumberSerializer.INSTANCE);
            builder.serializerByType(Long.TYPE, BigNumberSerializer.INSTANCE);

            // 配置 Jackson 序列化 LocalDateTime、LocalDate、LocalTime 时使用的格式
            builder.serializers(new LocalDateTimeSerializer(DateTimeFormatter.ofPattern(DEFAULT_DATETIME_PATTERN)));
            builder.serializers(new LocalDateSerializer(DateTimeFormatter.ofPattern(DEFAULT_DATE_FORMAT)));
            builder.serializers(new LocalTimeSerializer(DateTimeFormatter.ofPattern(DEFAULT_TIME_FORMAT)));


            // 配置 Jackson 反序列化 LocalDateTime、LocalDate、LocalTime 时使用的格式
            builder.deserializerByType(LocalDateTime.class, new LocalDateTimeDeserializer(DateTimeFormatter.ofPattern(DEFAULT_DATETIME_PATTERN)));
            builder.deserializerByType(LocalDate.class, new LocalDateDeserializer(DateTimeFormatter.ofPattern(DEFAULT_DATE_FORMAT)));
            builder.deserializerByType(LocalTime.class, new LocalTimeDeserializer(DateTimeFormatter.ofPattern(DEFAULT_TIME_FORMAT)));
            log.info("init jackson config");
        };
    }

}
```

### **超出 JS 最大最小值序列化**

```text
/**
 * 超出 JS 最大最小值 处理
 *
 * @author LGC
 */
@JacksonStdImpl
public class BigNumberSerializer extends NumberSerializer {

    /**
     * 根据 JS Number.MAX_SAFE_INTEGER 与 Number.MIN_SAFE_INTEGER 得来
     */
    private static final long MAX_SAFE_INTEGER = 9007199254740991L;
    private static final long MIN_SAFE_INTEGER = -9007199254740991L;

    /**
     * 提供实例
     */
    public static final BigNumberSerializer INSTANCE = new BigNumberSerializer(Number.class);

    public BigNumberSerializer(Class<? extends Number> rawType) {
        super(rawType);
    }

    @Override
    public void serialize(Number value, JsonGenerator gen, SerializerProvider provider) throws IOException {
        // 超出范围 序列化位字符串
        if (value.longValue() > MIN_SAFE_INTEGER && value.longValue() < MAX_SAFE_INTEGER) {
            super.serialize(value, gen, provider);
        } else {
            gen.writeString(value.toString());
        }
    }
}
```

### **spring 自动配置类导入**

META-INF.spring目录下创建 org.springframework.boot.autoconfigure.AutoConfiguration.imports 文件

加入 JsonAutoConfiguration 配置类全路径即可

## **jackson 封装成工具类**

jackson 封装成工具类，让其它使用jackson进行序列化和反序列的地方都使用jackson工具类，达到统一效果 比如：

1. Spring Web对传参的反序列化和返回值的序列化
2. springboot cache redis 缓存序列化和反序列化操作*RedisCacheConfiguration*
3. redis 存储对象时序列化和获取对象时反序列化
4. 业务代码中使用ObjectMapper进行对象与json字符串进行相互转换

工具类如下：

```text
/**
 * JSON 工具类
 *
 * @author LGC
 */
@Slf4j
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class JsonUtils {
    private static final String DEFAULT_DATETIME_PATTERN = "yyyy-MM-dd HH:mm:ss";
    private static final String DEFAULT_DATE_FORMAT = "yyyy-MM-dd";
    private static final String DEFAULT_TIME_FORMAT = "HH:mm:ss";

    public static final Jackson2ObjectMapperBuilderCustomizer CUSTOMIZER = jackson2ObjectMapperBuilderCustomizer();

    public static final ObjectMapper OBJECT_MAPPER = getObjectMapper();

    /**
     * 构建 Jackson 自定义配置
     *
     * @return
     */
    public static Jackson2ObjectMapperBuilderCustomizer jackson2ObjectMapperBuilderCustomizer() {
        return builder -> {
            // 这部分也可以在 yaml 中配置
            builder
                    // 序列化时，对象为 null，是否抛异常
                    .failOnEmptyBeans(false)
                    // 反序列化时，json 中包含 pojo 不存在属性时，是否抛异常
                    .failOnUnknownProperties(false)
                    // 禁止将 java.util.Date, Calendar 序列化为数字(时间戳)
                    .featuresToDisable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
                    // 设置 java.util.Date, Calendar 序列化、反序列化的格式
                    .dateFormat(new SimpleDateFormat(DEFAULT_DATETIME_PATTERN))
                    // 设置 java.util.Date、Calendar 序列化、反序列化的时区
                    .timeZone(TimeZone.getTimeZone("GMT+8"))
            ;
            // 配置 Jackson 序列化 BigDecimal 时使用的格式
            builder.serializerByType(BigDecimal.class, ToStringSerializer.instance);

            // 配置 Jackson 序列化 long类型为String，解决后端返回的Long类型在前端精度丢失的问题
            builder.serializerByType(BigInteger.class, BigNumberSerializer.INSTANCE);
            builder.serializerByType(Long.class, BigNumberSerializer.INSTANCE);
            builder.serializerByType(Long.TYPE, BigNumberSerializer.INSTANCE);

            // 配置 Jackson 序列化 LocalDateTime、LocalDate、LocalTime 时使用的格式
            builder.serializers(new LocalDateTimeSerializer(DateTimeFormatter.ofPattern(DEFAULT_DATETIME_PATTERN)));
            builder.serializers(new LocalDateSerializer(DateTimeFormatter.ofPattern(DEFAULT_DATE_FORMAT)));
            builder.serializers(new LocalTimeSerializer(DateTimeFormatter.ofPattern(DEFAULT_TIME_FORMAT)));


            // 配置 Jackson 反序列化 LocalDateTime、LocalDate、LocalTime 时使用的格式
            builder.deserializerByType(LocalDateTime.class, new LocalDateTimeDeserializer(DateTimeFormatter.ofPattern(DEFAULT_DATETIME_PATTERN)));
            builder.deserializerByType(LocalDate.class, new LocalDateDeserializer(DateTimeFormatter.ofPattern(DEFAULT_DATE_FORMAT)));
            builder.deserializerByType(LocalTime.class, new LocalTimeDeserializer(DateTimeFormatter.ofPattern(DEFAULT_TIME_FORMAT)));
            log.info("init jackson config");
        };
    }

    /**
     * 根据 Jackson 自定义配置 构建 ObjectMapper
     *
     * @return ObjectMapper
     */
    public static ObjectMapper getObjectMapper() {
        Jackson2ObjectMapperBuilder builder = new Jackson2ObjectMapperBuilder();
        CUSTOMIZER.customize(builder);
        return builder.build();
    }


    public static String toJsonString(Object object) {
        if (ObjectUtil.isNull(object)) {
            return null;
        }
        try {
            return OBJECT_MAPPER.writeValueAsString(object);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    public static <T> T parseObject(String text, Class<T> clazz) {
        if (StrUtils.isEmpty(text)) {
            return null;
        }
        try {
            return OBJECT_MAPPER.readValue(text, clazz);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static <T> T parseObject(byte[] bytes, Class<T> clazz) {
        if (ArrayUtil.isEmpty(bytes)) {
            return null;
        }
        try {
            return OBJECT_MAPPER.readValue(bytes, clazz);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static <T> T parseObject(String text, TypeReference<T> typeReference) {
        if (StrUtils.isBlank(text)) {
            return null;
        }
        try {
            return OBJECT_MAPPER.readValue(text, typeReference);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static Dict parseMap(String text) {
        if (StrUtils.isBlank(text)) {
            return null;
        }
        try {
            return OBJECT_MAPPER.readValue(text, OBJECT_MAPPER.getTypeFactory().constructType(Dict.class));
        } catch (MismatchedInputException e) {
            // 类型不匹配说明不是json
            return null;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static List<Dict> parseArrayMap(String text) {
        if (StrUtils.isBlank(text)) {
            return null;
        }
        try {
            return OBJECT_MAPPER.readValue(text, OBJECT_MAPPER.getTypeFactory().constructCollectionType(List.class, Dict.class));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static <T> List<T> parseArray(String text, Class<T> clazz) {
        if (StrUtils.isEmpty(text)) {
            return new ArrayList<>();
        }
        try {
            return OBJECT_MAPPER.readValue(text, OBJECT_MAPPER.getTypeFactory().constructCollectionType(List.class, clazz));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

}
```

## **对扩展web jackson自动装配修改**

```text
/**
 * jackson 配置
 *
 * @author LGC
 */
@Slf4j
@AutoConfiguration(before = JacksonAutoConfiguration.class)
public class JsonAutoConfiguration {

  /**
     * springboot 在构建ObjectMapper时默认使用这个构建器
     *
     * @return
     */
    @Bean
    public Jackson2ObjectMapperBuilderCustomizer customizer() {
        return JsonUtils.CUSTOMIZER;
    }

}
```

## **测试**

简单创建一个springboot项目，引入common-json 依赖包，创建一个controller

```text
/**
 * @author LGC
 */
@RestController
public class JsonTestController {
    @GetMapping("/testJson")
    public User testJson() {
        User user = new User(999999922222222223L, "lgc", new Date(), LocalDateTime.now());
        System.out.println(JsonUtils.toJsonString(user));
        return user;
    }

}

// 请求后输出都为
{"userId":"999999922222222223","username":"lgc","birthDay":"2023-12-20 15:16:45","birthDay2":"2023-12-20 15:16:45"}
```

## **扩展**

### **springboot cache redis 缓存修改**

```text
/**
 * Cache 配置类，基于 Redis 实现
 *
 * @author LGC
 */
@AutoConfiguration
@EnableConfigurationProperties({CacheProperties.class})
@EnableCaching
public class CacheAutoConfiguration {

    /**
     * RedisCacheConfiguration Bean
     *
     * @see org.springframework.boot.autoconfigure.cache.RedisCacheConfiguration 的 createConfiguration 方法
     */
    @Bean
    @Primary
    public RedisCacheConfiguration redisCacheConfiguration(CacheProperties cacheProperties) {
        // 设置使用 JSON 序列化方式
        RedisCacheConfiguration config = RedisCacheConfiguration.defaultCacheConfig();

        config = config.serializeKeysWith(RedisSerializationContext.SerializationPair.fromSerializer(RedisSerializer.string()));
        config = config.serializeValuesWith(RedisSerializationContext.SerializationPair.fromSerializer(redisSerializer()));

        // 设置 CacheProperties.Redis 的属性
        CacheProperties.Redis redisProperties = cacheProperties.getRedis();
        if (redisProperties.getTimeToLive() != null) {
            config = config.entryTtl(redisProperties.getTimeToLive());
        }
        if (redisProperties.getKeyPrefix() != null) {
            config = config.prefixCacheNameWith(redisProperties.getKeyPrefix());
        }
        if (!redisProperties.isCacheNullValues()) {
            config = config.disableCachingNullValues();
        }
        if (!redisProperties.isUseKeyPrefix()) {
            config = config.disableKeyPrefix();
        }
        return config;
    }


    /**
     * redis 序列化器
     *
     * @return
     */
    public GenericJackson2JsonRedisSerializer redisSerializer() {
        return new GenericJackson2JsonRedisSerializer(JsonUtils.OBJECT_MAPPER);
    }
}
```

### **RedisTemplate 配置修改**

```text
  /**
     * 创建 RedisTemplate 
     */
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
        RedisTemplate<String, Object> redisTemplate = new RedisTemplate<>();
        redisTemplate.setConnectionFactory(factory);
        // 使用 String 序列化方式，序列化 KEY 。
        redisTemplate.setKeySerializer(RedisSerializer.string());
        redisTemplate.setHashKeySerializer(RedisSerializer.string());
        // 值的序列化方式
        redisTemplate.setValueSerializer(redisSerializer());
        redisTemplate.setHashValueSerializer(redisSerializer());
        return redisTemplate;
    }

    /**
     * redis 序列化器
     *
     * @return
     */
    public GenericJackson2JsonRedisSerializer redisSerializer() {
         return new GenericJackson2JsonRedisSerializer(JsonUtils.OBJECT_MAPPER);
    }
```

