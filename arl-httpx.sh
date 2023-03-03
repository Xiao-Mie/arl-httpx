#!/bin/bash
	python arlCheck.py
	wait
	if [ -s temp.txt ];then
	
		python send_vx_message.py "资产收集完成"
		
		python send_vx_message.py "使用httpx探测存活"
				
		httpx -list temp.txt -silent -probe -o newurls.txtls  &> /dev/null           
		wait
		grep "SUCCESS" newurls.txtls | awk '{print $1}' > output.txtls
		wait
		python send_vx_message.py "httpx共找到存活资产 $(wc -l < output.txtls) 个"

		if [ ! -d "back" ]; then
  			mkdir -p "back"
		fi
		wait
		cat output.txtls >back/new-active-$(date +%F-%T).txt #保存新增资产记录
		
		python send_vx_message.py "已将存活资产存在加入到历史缓存 $(date +%F-%T)" 
		
		rm -rf output.txtls
		rm -rf newurls.txtls
		rm -rf temp.txt

	else
		python send_vx_message.py "无新域 $(date +%F-%T)" 
		rm -rf temp.txt
		
	fi


