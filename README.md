# fapiao_helper

发票整理助手

## 项目介绍

这是一个用于整理发票的Python工具，可以将发票信息提取并整理成Excel格式。

来源：https://zhuanlan.zhihu.com/p/620240165

## 功能特点

- 自动提取PDF发票中的关键信息
- 将提取的信息整理成Excel文件
- 支持批量处理多个发票文件
- 提供图形界面操作

## 依赖项

项目依赖以下Python库：

- `pdfminer.six==20221105` - PDF文本提取
- `xlsxwriter==3.1.9` - Excel文件生成

## 安装依赖

使用提供的打包脚本 `build_exe.py` 可以将Python脚本打包成Windows可执行文件：

```bash
python build_exe.py
```
