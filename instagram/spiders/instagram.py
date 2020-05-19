# -*- coding: utf-8 -*-
import scrapy
import time
import json
import os
import oss2
from urllib import request
from instagram_db import select_instagram_star,select_ins_id,set_instagram_log

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com']

    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth('user', 'pass')
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'zhuaqu')

    def parse(self, response):
        # print(response.text)
        star_list = select_instagram_star()
        for star in star_list:
            u = 'https://www.instagram.com/'+star[2]+'/'
            # u = 'https://www.instagram.com/kasumi_arimura.official/'
            yield scrapy.Request(url=u,callback=self.get_page,meta={'id':star[0],'name':star[1],'url':star[2],'memberid':star[3],'username':star[4],'type_name':star[5]})

    def get_page(self, response):
        # print(response.body)
        # time.sleep(1)
        # url = response.url
        sid = int(response.meta.get('id',{}))
        sname = response.meta.get('name',{})
        surl = response.meta.get('url',{})
        smemberid = int(response.meta.get('memberid',{}))
        susername = response.meta.get('username',{})
        stype_name = response.meta.get('type_name',{})
        scripts = response.xpath('//script/text()').extract()
        for script in scripts:
            time.sleep(1)
            s = script.rpartition(' = ')
            if(s[0]=='window._sharedData'):
                s_josn = s[2].replace(';','')
                s_josn = json.loads(s_josn)
                s_list = s_josn['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
                for s_l in s_list:
                    ins_id = s_l['node']['id']
                    thumb_img_src = s_l['node']['thumbnail_resources'][0]['src']
                    thumb_img_width = s_l['node']['thumbnail_resources'][0]['config_width']
                    thumb_img_height = s_l['node']['thumbnail_resources'][0]['config_height']

                    img_src = s_l['node']['thumbnail_resources'][3]['src']
                    img_width = s_l['node']['thumbnail_resources'][3]['config_width']
                    img_height = s_l['node']['thumbnail_resources'][3]['config_height']

                    shortcode = s_l['node']['shortcode']
                    text = ''
                    if(len(s_l['node']['edge_media_to_caption']['edges'])>0):
                        text = s_l['node']['edge_media_to_caption']['edges'][0]['node']['text']

                    row = select_ins_id(ins_id)
                    if(len(row)>0):
                        break

                    thumb_img_file_name = thumb_img_src.rpartition('/')
                    thumb_img_file_name = thumb_img_file_name[2]
                    thumb_img_file_name = thumb_img_file_name.rpartition('?')
                    thumb_img_file_name = thumb_img_file_name[0]

                    thumb_img_dir = './zhuaqu/instagram/'+str(sid)+'/thumb_img'
                    # is_thumb_img_dir = os.path.exists(thumb_img_dir)
                    # if not is_thumb_img_dir:
                    #     os.makedirs(thumb_img_dir)
                    thumb_img_file = thumb_img_dir+'/'+thumb_img_file_name
                    thumb_img_url = 'http://v3img.ifensi.com/instagram/'+str(sid)+'/thumb_img/'+thumb_img_file_name
                    thumb_content = request.urlopen(thumb_img_src).read()
                    # with open(thumb_img_file, 'wb') as thumb_img:
                    #     thumb_img.write(thumb_content)
                    thumb_oss_name = 'instagram/'+str(sid)+'/thumb_img/'+thumb_img_file_name
                    self.bucket.put_object(thumb_oss_name, thumb_content)

                    img_dir = './zhuaqu/instagram/'+str(sid)+'/img'
                    # is_img_dir = os.path.exists(img_dir)
                    # if not is_img_dir:
                    #     os.makedirs(img_dir)
                    img_file = img_dir+'/'+thumb_img_file_name
                    img_url = 'http://v3img.ifensi.com/instagram/'+str(sid)+'/img/'+thumb_img_file_name
                    content = request.urlopen(img_src).read()
                    # with open(img_file, 'wb') as img:
                    #     img.write(content)
                    oss_name = 'instagram/'+str(sid)+'/img/'+thumb_img_file_name
                    self.bucket.put_object(oss_name, content)

                    create_time = int(time.time())

                    set_instagram_log(sid, sname, surl, smemberid, susername, stype_name, ins_id, thumb_img_src, thumb_img_width, thumb_img_height, thumb_img_url, img_src, img_width, img_height, img_url, shortcode, text, create_time)

                    print(sid,ins_id,thumb_img_src,thumb_img_width,thumb_img_height,img_src,img_width,img_height,len(row),thumb_img_file,shortcode,sname,surl,smemberid,susername,stype_name,text,create_time)

