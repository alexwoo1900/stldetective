README: [ENGLISH](https://github.com/alexwoo1900/stldetective/blob/master/README.md) | [简体中文](https://github.com/alexwoo1900/stldetective/blob/master/README_CN.md)

## STLDetective用来处理什么问题
这个小脚本用来计算STL模型的包围盒，输出包围盒的长宽高参数。

## 什么是包围盒
如同下图所示：

![bounding-box-sample](https://raw.githubusercontent.com/alexwoo1900/stldetective/master/docs/assets/bounding-box-sample.png)

假如图片涉及到版权问题，请立即联系我。

## 如何使用这个小脚本
如果想直接使用代码，请参看以下例子
```python
detective = STLDetective()
detective.load_file(stlFullPath)
detective.getModelBBox() # print 20.2 50.0 100.5
```
如果想以其他形式输出，请修改getModelBBox的返回值

如果将其当作一个外部工具被其他程序调用，编译好脚本之后使用以下指令即可
```bash
STLDetective.exe cat.stl
```