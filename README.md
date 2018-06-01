README: [ENGLISH](https://github.com/alexwoo1900/stldetective/blob/master/README.md) | [简体中文](https://github.com/alexwoo1900/stldetective/blob/master/README_CN.md)

## What is STLDetective used for
It's a mini script for calculating the bounding box of a STL model. The output is width/depth/height of the bounding box.

## What is bounding box
Like the following image showed:

![bounding-box-sample](https://raw.githubusercontent.com/alexwoo1900/stldetective/master/docs/assets/bounding-box-sample.png)

If this picture involved copyright issues, please contact me.

## How to use it
If you want to use the code, the following demo will be helpful.
```python
detective = STLDetective()
detective.load_file(stlFullPath)
detective.getModelBBox() # print 20.2 50.0 100.5
```
Or you can modify the return of function getModelBBox to be compatible with your own program.

If you want the tool can be executed by other processors, after compiling this script, you can call it in command line
```bash
STLDetective.exe cat.stl
```