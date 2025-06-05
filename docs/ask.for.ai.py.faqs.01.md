## attempted relative import with no known parent package

### 终端输出内容
```terminal
Traceback (most recent call last):
  File "D:\code\python\panz\comfyui-nodes\ymc-node-suite-comfyui\node_demo.py", line 1, in <module>
    from .conf import CURRENT_CATEGORY,CURRENT_FUNCTION
ImportError: attempted relative import with no known parent package
```

### 错误解释
- `Traceback (most recent call last)`：这是 Python 错误堆栈跟踪的起始行，表明 Python 开始回溯错误发生的位置。
- `File "D:\code\python\panz\comfyui-nodes\ymc-node-suite-comfyui\node_demo.py", line 1, in <module>`：指出错误发生在 `node_demo.py` 文件的第 1 行。
- `from .conf import CURRENT_CATEGORY,CURRENT_FUNCTION`：这是出错的代码行，尝试使用相对导入从 `conf` 模块导入 `CURRENT_CATEGORY` 和 `CURRENT_FUNCTION`。
- `ImportError: attempted relative import with no known parent package`：错误类型为 `ImportError`，提示使用相对导入时没有找到已知的父包。相对导入需要在包的上下文中使用，当直接运行脚本时，Python 不会将其视为包的一部分，所以会报错。

### 修复建议
#### 方法一：将项目作为包运行
如果你想使用相对导入，可以将项目作为包运行。在项目根目录下使用 `-m` 选项：
```powershell
python -m ymc-node-suite-comfyui.node_demo
```

#### 方法二：使用绝对导入
修改 `node_demo.py` 文件，将相对导入改为绝对导入：
```python:d:\code\python\panz\comfyui-nodes\ymc-node-suite-comfyui\node_demo.py
# 修改前
# from .conf import CURRENT_CATEGORY,CURRENT_FUNCTION

# 修改后
from ymc_node_suite_comfyui.conf import CURRENT_CATEGORY,CURRENT_FUNCTION
```
请根据实际的包名调整绝对导入路径。 