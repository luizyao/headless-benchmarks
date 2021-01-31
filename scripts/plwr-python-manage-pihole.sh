#!/usr/bin/env zsh

# time 命令默认格式是 “%J %U user %S system %P cpu %*E total”，这里只显示总时间
export TIMEFMT=$'%*E'

export PIHOLEPASSWORD="12345678"

# 清空上一次的结果
: >../results/playwright-python-manage.txt
: >../results/playwright-python-manage-status.txt

for i in {1..$1}; do
    echo $i
    {time pipenv run python playwright-python/manage.py } 2>>../results/playwright-python-manage.txt
    echo $? >>../results/playwright-python-manage-status.txt
done
