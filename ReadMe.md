# Python实现redis(纯学习目的)

## 1. Python实现与C实现的区别
* sds 不保留'\0'结尾(没有复用c string函数族的必要) python底层通过bytearray实现