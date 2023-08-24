在工作中遇到，使用console.log()输出对象信息时，出现输出的信息跟自己想的不一样的问题，导致调试bug时，思路走偏。
当时参考了别人的[issues](https://github.com/Mmzer/think/issues/30)已经讲的很清楚了。
这里自己再记录一下

**问题描述**：

> 即使我直接在赋值语句`const obj = {age: 20}`后面紧跟console.log(obj)，
> 在浏览器的控制台，看到的age字段，也不一定是20。
>
> 因为，如果在后面的代码中，修改了age字段的值，那控制台看到的就不是20了。

比如执行如下代码：

```js
let obj = {age: 20};
console.log(obj);
obj.age = 30;
```

得到的输出如下：

![img](新建文本文档.assets/1388863-20190916203912680-663159596.jpg)

可以看到，**不展开obj对象，看到的是我们预期的20，展开对象，看到的却是30**。

**如果我们输出一个字段很多的对象，那必须展开才能看到属性值，就会被非预期的属性值误导。**

**原因分析**：

- 不展开对象看时，console.log()是按照代码执行顺序，同步地输出了对象当时的快照。所以我们看到的是预期的值。
- 展开对象时，它其实是重新去内存中读取对象的属性值，此时对象属性已被更改，所以展开对象后，可能看到的不是预期值了。

**浏览器或者开发者工具(F12)为什么出现这种情况？**

这个问题，在《你不知道的javascript中卷》第二部分异步和性能1.1节一部控制台部分有提及：

> There is no specification or set of requirements around how the console.* methods work -- they are not officially part of JavaScript, but are instead added to JS by the hosting environment (see the Types & Grammar title of this book series).
> So, different browsers and JS environments do as they please, which can sometimes lead to confusing behavior.
> In particular, there are some browsers and some conditions that console.log(..) does not actually immediately output what it's given. The main reason this may happen is because I/O is a very slow and blocking part of many programs (not just JS). So, it may perform better (from the page/UI perspective) for a browser to handle console I/O asynchronously in the background, without you perhaps even knowing that occurred.

翻译：

> 并没有什么规范或一组需求指定console.* 方法族如何工作——它们并不是JavaScript 正式的一部分，而是由宿主环境（请参考本书的“类型和语法”部分）添加到JavaScript 中的。因此，不同的浏览器和JavaScript 环境可以按照自己的意愿来实现，有时候这会引起混淆。
> 尤其要提出的是，**在某些条件下，某些浏览器的console.log(..) 并不会把传入的内容立即输出。出现这种情况的主要原因是，在许多程序（不只是JavaScript）中，I/O 是非常低速的阻塞部分。**所以，（从页面/UI 的角度来说）浏览器在后台异步处理控制台I/O 能够提高性能，这时用户甚至可能根本意识不到其发生。

**结论**

console.log()打印出来的内容并不是一定百分百可信的内容。一般对于基本类型`number、string、boolean、null、undefined`的输出是可信的。但对于`Object`等引用类型来说，则就会出现上述异常打印输出。

**建议**

- 尽量不要直接输出对象，先将对象序列化`JSON.stringify()`为字符串再输出
- 最好使用打断点(debugger)的方式来调试。