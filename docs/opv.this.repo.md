```powershell
# 1
python __init__.py

python nodes.py


# 
python -m main; # run module main done
python main.py; # run module main done

# python node_demo.py

python -m ymc_node_suite_comfyui.node_demo

# yours touch docs/ask.for.ai.py.faqs.01.md
# yours touch docs/ask.for.ai.py.faqs.02.md

yours touch docs/ask.for.ai.node-01-the-old-nodes.md
yours touch docs/ask.for.ai.node-02-refactor-nodes.md

yours touch nodes/text/__init__.py
yours touch nodes/text/conf.py
yours touch nodes/text/join.py
yours touch nodes/text/search.py
yours touch nodes/text/random.py
yours touch nodes/text/loop.py
yours touch nodes/text/switch.py
yours touch nodes/text/prompts.py #join,std,del,dup,shuffle
yours touch nodes/text/input.py 

yours touch nodes/area/__init__.py
yours touch nodes/area/conf.py
yours touch nodes/area/from_center_and_size.py
yours touch nodes/area/from_lefttop_and_size.py
yours touch nodes/area/padd.py

# canvas cal size

yours touch nodes/image/__init__.py
yours touch nodes/image/conf.py
yours touch nodes/image/get_image_size.py
yours touch nodes/image/switch_image.py


yours touch nodes/utils/__init__.py
yours touch nodes/utils/conf.py
yours touch nodes/utils/random_num.py
yours touch nodes/utils/text_to_int.py
yours touch nodes/utils/basic_pipe.py

yours touch nodes/file/__init__.py
yours touch nodes/file/conf.py
yours touch nodes/file/get_file_list.py
yours touch nodes/file/get_text_of_file_list.py


yours touch nodes/cutoff/__init__.py
sh -c "cp  nodes/text/__init__.py nodes/cutoff/__init__.py"
sh -c "cp  nodes/text/conf.py nodes/cutoff/conf.py"

yours touch nodes/cutoff/text_from.py
yours touch nodes/cutoff/text_list_color.py

python -c "import sys;print(sys.path)"

# sh -c "rm -rf nodes/text/{input,join,loop,random,search,switch}.py"
# sh -c "rm -rf nodes/cutoff"

# sh -c "rm -rf nodes/cutoff"

```
## fags
- ImportError: attempted relative import with no known parent package


## depoy to comfyui (local + debug)
```bash
# del local nodes in comfyui custom_nodes
sh -c "rm -rf /o//app/ComfyUI/custom_nodes/ymc-node-suite-comfyui"
# copy local nodes to comfyui custom_nodes
sh -c "cp -r /d/code/python/panz/comfyui-nodes/ymc-node-suite-comfyui /o/app/ComfyUI/custom_nodes/"


# conda activate sdwa;cd O:\app\ComfyUI;python main.py;
```

## opv - docs
```bash
git add README.md ; git commit -m "docs(core): put usage"


git add . ; git commit -m "refactor(core): reset dirs"
git add . ; git commit -m "refactor(core): rename nodes map"
git add . ; git commit -m "refactor(core): rename nodes display name"

git add . ; git commit -m "refactor(core): put dirs and category"

# get git msg log with oneline and short hash and msg head and time
git log --pretty=format:"%h %ad %s" --date=short -n 5

git log --oneline -n 5

git rm CHANGELOG.*.md
git rm conf.py 
git mv node_demo.py docs/node_demo.py.md
git rm README.*.md 
```

## opv - shotscreen
```bash

```
