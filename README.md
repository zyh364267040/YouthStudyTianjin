# YouthStudyTianjin
天津青年大学习刷人数工具。

**<u>本工具仅供交流学习使用,请勿用于非法用途</u>**

## 使用方法
```shell
python main.py --cookie
```

### 示例
```shell
python main.py -c 7F5335ADA32F865C5F2E662589BD4B6B
```

## 参数

main.py

* `-c` `--cookie`  cookie

## 如何获取cookie

可以通过Fiddle/Charles(电脑)或HttpCanary(手机)抓取访问青年大学习时的cookie, 然后将"JSESSIONID="后边的部分截取下来作为参数传入`--cookie`

## 文件导入

首先在 `section_id_dic` 中添加相对应的团支部id,可以通过Fiddle/Charles(电脑),在青年大学习页面中点击修改人员信息,选择自己的团支部,然后到Fiddle/Charles上复制到自己团支部的代码

xlsx文件格式要第一行不要存放信息,或者当表头使用,序号 团支部 姓名 手机号,按照这个格式存放信息,序号从1开始往下排,团支部写存放在 `section_id_dic` 中sectionId的 `key`

## 注意

这个脚本是使用一个微信去学习,会过滤掉已经学习的人,但其他人都是这一个微信的头像.

使用的时候人数够了就不要多刷,本着完成任务的的心理使用,刷的太多被封了,就没得玩了.
