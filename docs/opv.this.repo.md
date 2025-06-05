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
## opv - features
```bash
# use ymc suite/text/cutoff
git add modules/text/node_cutoff_region.py ; git commit -m "feat(core): rename category for reading"
# use ymc suite/text/plain
git add modules/text/node_plain.py ; git commit -m "feat(core): use suite/text/plain"

git add modules/text/node_pyio.py ; git commit -m "feat(core): use suite/text/io"
git add modules/text/node_region.py ; git commit -m "feat(core): use suite/text/region"

git add modules/text/node_cutoff*.py ; git commit -m "build(core): use cutoff as filename"
git add modules/text/node_prompt*.py ; git commit -m "build(core): use category in itself"
```

## opv - docs
```bash
git add README.md ; git commit -m "docs(core): put usage"
git add . ; git commit -m "build(core): use shotscreen"
git add docs/opv.*.md ; git commit -m "docs(core): put note"

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
sh -c "mkdir -p shotscreen"

sh -c "cp -r /o/app/ComfyUI/my_workflows/nodes*.png shotscreen/"

```

## changelog


## clog - gen feat of from source code

```powershell
# yours edit-docs -h
yours feat --field feat --src-file modules/text/node_plain.py --out-file CHANGELOG.md --mode overide

yours feat --field feat --src-file modules/text/node_prompt.py --out-file CHANGELOG.md --mode tail

yours feat --field feat --src-file modules/text/node_pyio.py --out-file CHANGELOG.md --mode tail

yours feat --field feat --src-file modules/text/node_region.py --out-file CHANGELOG.md --mode tail

yours feat --field feat --src-file modules/text/node_cutoff_region.py --out-file CHANGELOG.md --mode tail

# add commit msg for this work:
# git add CHANGELOG.md ; git commit -m "chore(core): gen feat of from source code"
```

## clog - code size/feat/docs - name

```powershell
# set description in markdown file ?
# yours edit-docs --tpl-file docs.template.md --data "$pkgdesc" --label "<!-- inject-desc -->" --out-file README.md --workspace "$wsroot/$pkgsloc/$name"

yours edit-docs --tpl-file docs.template.md --data "$pkgdesc" --label "{description}" --out-file README.md --workspace "$wsroot/$pkgsloc/$name"

# set file size in markdown file ?
# yours edit-docs --tpl-file README.md --data-file lib-size.md --label "<!-- inject-file-size -->" --out-file README.md --workspace "$wsroot/$pkgsloc/$name"

# set features in markdown file ?
yours edit-docs --tpl-file README.md --data-file CHANGELOG.md --label "<!-- inject-features -->" --out-file README.md --workspace "$wsroot/$pkgsloc/$name"

# set installing package in markdown file ?
yours edit-docs --tpl-file README.md --data "$name" --label "{package}" --out-file README.md --workspace "$wsroot/$pkgsloc/$name"


# set demo in markdown file ?
# yours edit-docs --tpl-file README.md --data-file examples/main.py --label "<!-- inject-demo -->" --out-file README.md --workspace "$wsroot/$pkgsloc/$name"

# set demo in markdown file ? (demo.md)
yours edit-docs --tpl-file README.md --data-file demo.md --label "<!-- inject-demo -->" --out-file README.md --workspace "$wsroot/$pkgsloc/$name"


# add and set msg for this
# git add "packages/$name/*.md" ; git commit -m "docs(core): gen docs";

# git add "packages/$name/*.md" ; git commit -m "docs(core): put docs";
```

## opv - tags
```powershell
# add tags
git tag -a v1.0.0 -m "v1.0.0"

# git push ghg v1.0.0

git log --oneline 
git tag


#$ver=yours version/bump --file pyproject.toml --name "tool.poetry.version" --method minor 

#$ver=yours version/bump --file pyproject.toml --name "project.version" --method minor 
$ver="3.0.0"
# add tags to some hash
git tag v$ver 73da0b9;

git tag v$ver HEAD;

# add/commit/tag
git add . ; git commit -m "build(core): put verison";git tag v$ver HEAD;
# git add . ; git commit -m "v$ver";git tag v$ver HEAD;

# add/commit with version? do
git add . ; git commit -m "$ver";

# git push ghg main --tags --force
# git push ghg main --tags --force
# git push ghg v$ver
```
## opv - workflow files
```powershell
# touch

yours touch .github/workflows/publish_to_comfy.yml
# edit
# ...

# add secret form comfy
# ...

git add .github/workflows/publish_to_comfy.yml; git commit -m "build(core): add publish to comfy workflow";
git add .github/workflows/publish_to_comfy.yml; git commit -m "build(core): check node in comfy";

git tag -d v$ver
```