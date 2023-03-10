import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import selenium
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import os.path
from selenium import webdriver
import time
import glob, os
import os
import openpyxl
import re
#import pinyin
from pypinyin import pinyin, lazy_pinyin, Style
import shutil
from PIL import Image

from pathlib import Path
from pandas.api.types import is_string_dtype
from bs4 import BeautifulSoup
from pandas.api.types import is_numeric_dtype
from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection)


def space_replacer(word):
    return word.replace(" ","_")

def get_dict_df():
    for excel_data_raw in glob.glob("*.xlsx"):
        if excel_data_raw !="class_map.xlsx":
            dict_df = cleanup(pd.read_excel(excel_data_raw, sheet_name=None))
            wb = openpyxl.load_workbook(excel_data_raw)
            return [dict_df,wb]

def create_class_map():
    dict_df,wb=get_dict_df()
    df_class_map=pd.DataFrame(index=dict_df.keys(),columns=dict_df.keys())
    for tab,df in dict_df.items():
        for col in df.columns:
            if "For " in col or "By " in col:
                replaced_col=col.replace("For ","").replace("By ", "")
                df_class_map.at[tab,replaced_col]=1
    df_class_map.to_excel("class_map.xlsx")


def parse_to_json():
    pass

def return_array_related_classes(tab, connections=2):
    result = []
    for excel_data_raw in glob.glob("*.xlsx"):
        if excel_data_raw !="class_map.xlsx":
            dict_df = pd.read_excel(excel_data_raw, sheet_name=None)
            df_tab=dict_df[tab]
            for column in df_tab.columns:
                if "For " in column or "By " in column:
                    result+=[column.replace("For ", "").replace("By ","")]

    neighbbourh_result=[]
    print("outside result is ",result)
    if connections >1:
        for neighbortab in result:
            print("for neightbor ",neighbortab)
            neighbbourh_result=neighbbourh_result+return_array_related_classes(neighbortab, connections=connections-1)

    print("final ",tab," is ", result+neighbbourh_result)
    return list(set(result+neighbbourh_result))


def cleanup(dict_df):

    """
    iterate through all tabs, changes key items with comma to other sign
    1. copy each index as a copy column
    """
    new_dict_df={}
    dict_to_replace={}
    forbidden_chars={"@nio.com":'',
                     "@nio.io":'',
                     ",":'',
                     ".":'_',
                     "/":'_',
                     " ":'_', #still empty space in tab data not converted
                     }
    for tab, df in dict_df.items():
        #create a new helper column
        df["RemoveMe"]=df[tab].copy()

        for item, (index, row) in zip(df["RemoveMe"],df.iterrows()):
            if pd.isna(item):
                continue

            for forbidden_char in forbidden_chars:
                if forbidden_char not in item: #item is already clean, no need to cleanup
                    continue

            correct_item=item
            for forbidden_char, toreplace in forbidden_chars.items():
                correct_item=correct_item.replace(forbidden_char,toreplace)
            df.at[index,"RemoveMe"]=correct_item
            dict_to_replace[item]=correct_item

        # create a new helper column
        df[tab] = df["RemoveMe"]
        df.drop('RemoveMe', axis=1,inplace=True)


    for tab, df in dict_df.items():
        df=df.replace(dict_to_replace,inplace=False)
        new_dict_df[tab]=df


    return new_dict_df


def return_string_gallery(word):
    """returns a fa icon"""
    dict_gallery={
        "Department":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblKZKd1q8wmv6HL&view=vewUx4CSfi",
        "Employee":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblPtBnAeQA82JcL&view=vewbVi02lT",
        "Role":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblvaOn65LfwKZgh&view=vewtB3stx3",
        "User_Process":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblXI11nUP5hraec&view=vewdO1XHOV",
        "Employee_Process":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblmqm1WaKREMzM6&view=vew18ykPxw",
        "Capability":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblaQfACFL2RmmF0&view=vewyHEANB6",
        "System":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblkrJ6NVdCbc10a&view=vewmLZijxy",
        "Strategy": "https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tbleijKoxmfs8WXB&view=vewZfdR1ir",
        "City":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblVk7GzlSl7A3fK&view=vewppJl3ro",
        "Car":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblIjUl8dRCbolCI&view=vewEEtBGbz",
        "KPI":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblKMxqrBjWmaw7f&view=vew2GwzJXf",
        "Business_Model":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tbl8tg5FsGjSKG3Y&view=vewzVWmrso",
        "User_Journey":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblAyuTuEKVVVrZ3&view=vewBZ5BYQK",
        "Employee_Journey":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblgDQkj9F2O3XSd&view=vewxV21Rjf",
        "Country":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblDmXtQ5JPySoUz&view=vewrnTjfGP",
        "Others":"fa-gear",
    }
    return dict_gallery[word]

def return_string_icon(word):
    """returns a fa icon"""
    dict_icon={
        "Departments": "fa-sitemap",
        "L1_Department":"fa-folder-tree",
        "Department":"fa-folder-tree",
        "L2_Department":"fa-folder-tree",
        "L3_Department":"fa-folder-tree",
        "Leader":"fa-user-tie",
        "Employee":"fa-user",
        "Role":"fa-user-tag",
        "Process": "fa-repeat",
        "User_Process":"fa-route",
        "Employee_Process":"fa-people-arrows",
        "Capability":"fa-location-crosshairs",
        "System":"fa-screwdriver-wrench",
        "Value":"fa-hand-holding-heart",
        "People": "fa-users",
        "Strategy": "fa-compass",
        "City":"fa-location-dot",
        "Car":"fa-car",
        "KPI":"fa-chart-simple",
        "Business_Model":"fa-money-bill",
        "User_Journey":"fa-route",
        "Employee_Journey":"fa-route",
        "Country":"fa-globe",
        "Others":"fa-gear",
    }
    return dict_icon[word]


def return_string_component(word):
    """returns a fa icon"""
    dict_explainer={
        "Departments": "",
        "L1_Department":"This view shows you what L1 department exists that are relevant for EB.",
        "Department":"This view shows you what L1 department exists that are relevant for EB.",
        "L2_Department":"This view shows you what L2 departments under European Business.",
        "L3_Department":"This view shows you what L3 departments under European Business.",
        "Leader":"This summary shows who are the department leaders and what do they lead.",
        "Employee":"This summary shows all employee details in European Business.",
        "Role":"This view shows the abstract role in European Business and who is working as them.",
        "Process": "This view shows what User_Process is there and what Employee_Process is there.",
        "User_Process":"This view shows what User_Process exists and how are they defined.",
        "Employee_Process":"This view shows what Employee_Process exists and how are they defined.",
        "Capability":"This view shows what Business Capabilities exists and what processes implements these capabilities",
        "System":"This view lists all relevant systems for European Business, how to use them and where to access them.",
        "Value":"This view lists all companies values and how it is reflected in our Business Capabilties.",
        "People": "asd",
        "KPI": "This view lists all relevant KPIs for their processes.",
        "Strategy": "This view shows what high level Strategies exists and which Processes implements these Strategies.",
        "City":"The location view shows what infrastructure is there and which employee is here.",
        "Car":"What model exists for different country and business model",
        "Business_Model":"The location view shows what form of ownership user can have.",
        "User_Journey":"Different types of user journey for different business model",
        "Employee_Journey":"How NIO prepares for the user journey",
        "Country":"Markets where NIO sells car",
        "Others":"sad",
    }
    return dict_explainer[word]


def return_string_editurl(word):
    """returns a fa icon"""
    dict_url={
        "Department":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblyxOzBlxXbfgFi&view=vewgFkOi9f",
        "L1_Department":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblyxOzBlxXbfgFi&view=vewgFkOi9f",
        "L2_Department":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblcnQTN78GEt3nR&view=vewjua7iRe",
        "L3_Department":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblyxoLGbBcp1yUZ&view=vew8hBjN9a",
        "Leader":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblPFljTQ27fSZnc&view=vewNiWsvzO",
        "Employee":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblPtBnAeQA82JcL&view=vewM4stVK8",
        "Role":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblvaOn65LfwKZgh&view=vewwt7M9id",
        "User_Process":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblXI11nUP5hraec&view=vewX0IOZ4B",
        "Employee_Process":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblmqm1WaKREMzM6&view=vewAvMXYfY",
        "Capability":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblaQfACFL2RmmF0&view=vewKr0PzLw",
        "System":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblkrJ6NVdCbc10a&view=vewmLZijxy",
        "Value":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblIoyKb5UMTmu09&view=vewRvuZf3B",
        "Strategy": "https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tbleijKoxmfs8WXB&view=vewj6vLShZ",
        "City":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblVk7GzlSl7A3fK&view=vewppJl3ro",
        "Car":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblIjUl8dRCbolCI&view=vewYO6qS8t",
        "KPI":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblKMxqrBjWmaw7f&view=vewAteOLwS",
        "Business_Model":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tbl8tg5FsGjSKG3Y&view=vewBKzxKpU",
        "User_Journey":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblAyuTuEKVVVrZ3&view=vew6pEQzqw",
        "Employee_Journey":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblgDQkj9F2O3XSd&view=vewpiLPhLI",
        "Country":"https://nio.feishu.cn/wiki/wikcnHtTpp2T1YilHB3jiT3tiLf?table=tblDmXtQ5JPySoUz&view=vewSKuK63B",
    }
    return dict_url[word]








def return_global_navbar():
    dict_nav = {
        "Departments": ["Department"],
        "People": [ "Employee", "Role"],
        "Process": ["User_Process", "Employee_Process", "KPI", "User_Journey", "Employee_Journey"],
        "Strategy": ["Strategy", "Capability", "Business_Model"],
        "Others": ["System", "City", "Country", "Car"],
    }

    navbar_template='<nav class="navbar navbar-expand-lg navbar-dark bg-primary" aria-label="Eighth navbar example"> <div class="container">  <a href="../../mc2/index/index.html" class="navbar-brand"> <img src="../../img/nio light.png" height="28" alt="CoolBrand"> </a>  <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarinstance" aria-controls="navbarinstance" aria-expanded="false" aria-label="Toggle navigation"> <span class="navbar-toggler-icon"></span> </button> <div class="collapse navbar-collapse" id="navbarinstance"> <ul class="navbar-nav me-auto mb-2 mb-lg-0"> {} </ul> </div> </div> </nav>'
    navbar_content = "" #for li in url template
    for key, array in dict_nav.items():
        navbar_content_li_template = f'<li class="nav-item dropdown"> <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> <i class="fa-solid {return_string_icon(key)}"></i> {key} </a> <div class="dropdown-menu" aria-labelledby="navbarDropdown">' + '{}</div></li>'
        navbar_content_li_content=""
        for counter,label in enumerate(array):
            navbar_content_li_content=navbar_content_li_content+f'<a class="dropdown-item" href="../../mc2/{label}/{label}.html"><i class="fa-solid {return_string_icon(label)}"></i> {label}</a>'
            if counter+1<len(array):#add divider
                navbar_content_li_content = navbar_content_li_content + f'<div class="dropdown-divider"></div>'

        #add new li to previous li
        navbar_content=navbar_content+navbar_content_li_template.format(navbar_content_li_content)

    global global_navbar
    global_navbar= navbar_template.format(navbar_content)





def return_global_html():
    #create data
    dict_df,wb = get_dict_df()

    all_json = ''
    for tab, df in dict_df.items():
        one_json = df.to_json(orient="records")
        one_json = f'"{tab}"' + ": " + one_json + ","
        all_json = all_json + one_json
    all_json = ' var data={' + all_json + "};"
    with open(fr"paste to github/bootstrap/js/data.js", "w", encoding="utf-8") as file:
        file.write(str(all_json))

    js_jquery = '<script src="https://code.jquery.com/jquery-3.3.1.min.js" crossorigin="anonymous"></script>'
    js_popperjs = '<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>'
    js_bootstrap = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>'
    js_fa = '<script defer src="https://use.fontawesome.com/releases/v5.15.4/js/all.js" integrity="sha384-rOA1PnstxnOBLzCLMcre8ybwbTmemjzdNlILg8O7z1lUkLXozs4DHonlDtnE7fpc" crossorigin="anonymous"></script>'
    js_cytoscape = '<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.23.0/cytoscape.min.js" integrity="sha512-gEWKnYYa1/1c3jOuT9PR7NxiVI1bwn02DeJGsl+lMVQ1fWMNvtjkjxIApTdbJ/wcDjQmbf+McWahXwipdC9bGA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>'
    js_cj = '<script  src="../../bootstrap/js/cj.js"  ></script>'
    js_data = '<script  src="../../bootstrap/js/data.js"  ></script>'

    css_fa = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css">'
    css_bootstrap = '<link href="../../bootstrap/css/bootstrap.css" rel="stylesheet">'
    css_cj = '<link href="../../bootstrap/css/cj.css" rel="stylesheet">'

    favicon='<link rel="icon" href="../../img/nio.ico">'

    head = '<head>{}</head>'.format(css_fa +css_bootstrap + css_cj+favicon)
    body = "<body>"+global_navbar +"<div class='container'>{content}</div> "+js_jquery + js_popperjs + js_bootstrap + js_fa+js_cytoscape+"{jsinclude}"+js_cj+js_data+"</body>"
    bottomspacer='<div class="p-5 m-5"></div>'
    footer='<footer class="py-0 my-0 fixed-bottom"><p class="text-center text-muted px-3" style="float:right;">&copy; 2023 made by CJ</p></footer>'



    global template
    template = head+body+bottomspacer




def return_content_instance(instance, row, tab, dict_df):
    h1=f'<h2 class="pt-5 pb-1" id="header" data-current_class="{tab}"  data-current_instance="{instance}">  <i class="fa-solid {return_string_icon(tab)} fa-xl"></i> {tab}: {instance} </h2> <a href="{return_string_editurl(tab)}" style="font-size:1.25rem;" target="_blank" type="button" class="btn btn-primary btn-sm fs-3 float-right mt-3" ><i class="fa-solid fa-edit"></i> edit</a>  <a href="../../mc2/{tab}/{tab}.html" style="font-size:1.25rem;"  type="button" class="btn btn-primary btn-sm fs-3 mr-1 float-right mt-3" ><i class="fa-solid {return_string_icon(tab)}"></i> More {tab}</a> <hr/> '
    #h1 = f'<h2 class="pt-5 pb-1" id="header" data-current_class="{tab}"><div style="max-width:85%;"><i class="fa-solid {return_string_icon(tab)} fa-xl"></i> {tab}   </div> <a href="{return_string_editurl(tab)}" style="float:right;font-size:1.25rem;" target="_blank" type="button" class="btn btn-primary btn-sm fs-3" ><i class="fa-solid fa-edit"></i> edit</a></h2>'

    ul="<ul>{}</ul>"
    lis=""
    real_instance=instance
    for instance, val in row.items():
        if "For" in instance or "By" in instance:
            for_what=instance.replace("For ", "").replace("By ", "")
            if pd.isna(val):
                continue
            if "," not in val:
                lis = lis + f"<li>{instance}: <a href='../{for_what}/{space_replacer(val)}.html'>{val}</a></li>"
            else:
                ul2 = "<ul>{}</ul>"
                lis2 = ""
                for val_item in val.split(","):
                    lis2=lis2+f"<li><a href='../{for_what}/{space_replacer(val_item)}.html'>{val_item}</a></li>"
                lis = lis + f"<li>{instance}: {ul2.format(lis2)}</li>"
        else:
            lis=lis+f"<li>{instance}: {val}</li>"


    component_cy, component_cy_js = return_component_cy(dict_df=dict_df, highlight_classes=[tab],  only_nodes=[x for x in dict_df.keys()], height="height50")

    label_direct_attribute=return_component_small_header(True)
    label_indirect_attribute=return_component_small_header(False)
    header = return_component_header(df=pd.DataFrame(), tab=tab, dict_df=dict_df, instance=real_instance)
    spacer= return_component_spacer()
    template_card=return_template_card()
    indirect_chart=return_indirect_chart()

    direct_part=(spacer+ label_direct_attribute+ ul.format(lis))
    indirect_part= spacer+ label_indirect_attribute+  component_cy +indirect_chart

    content=header + direct_part + indirect_part
    return template.format(content=content, jsinclude=component_cy_js)


def return_template_card():
    result="""
    <div class="card" style="width: 100%;">
  <div class="card-body">
    {}
  </div>
</div>
    """
    return result

def return_component_spacer():
    result = '<p class="mt-5"></p>'
    return result

def return_indirect_chart():
    return '<p>todo<p/>'

def return_component_small_header(is_direct=True):
    if is_direct:
        result='<h4>1. Direct Information:</h4>'
    else:
        result='<h4>2. Indirect Information: </h4>'
    return result

def return_word_class_url(class_tab):
    return fr"../../mc2/{class_tab}/{class_tab}.html"

def return_word_instance_url(class_tab, instance):
    return fr"../../mc2/{class_tab}/{instance}.html"

def return_component_header(df,tab, dict_df, instance):
    try:
        count = len(df[df[tab].notna()])
        classcount = f'<span class="badge badge-pill badge-secondary">{count} items</span> '
    except:
        classcount=""

    h1_icon=f'<a href="{return_word_class_url(class_tab=tab)}"><i class="fa-solid {return_string_icon(tab)} fa-xl"></i></a>'
    edit=f'<a href="{return_string_editurl(tab)}" style="font-size:1.25rem;" target="_blank" type="button" class="btn btn-primary btn-sm fs-3" ><i class="fa-solid fa-edit"></i></a>'
    other_classes=""
    if instance:
        explainer=f''
    else:
        explainer = f'<p class="fs-1 pb-1 text-secondary">{return_string_component(tab)}</p>'

    header_text= f'{tab}: {instance}' if instance else tab
    h1 = f'<h2 class="pt-5 pb-1" id="header" data-current_class="{tab}">{h1_icon} {header_text} {classcount} {edit} </h2>' +explainer

    return h1+"<hr/>"


def return_content_class(tab, df,dict_df):
    cards=''
    for (fakekey, row),key in zip(df.iterrows(),df[tab]):
        if pd.isna(key) or key is None:
            continue
        cardstart=f'<div id="{space_replacer(key)}" class="card m-1 mb-5 " style="width: 32%;float:left;">  <div class="card-body">    <h5 class="card-title"><a href="../../mc2/{tab}/{key}.html">{key}</a></h5>'+'{}</div></div>'
        cardmiddle=""
        for row_key, row_item in row.items():
            if row_key!=tab:
                row_entry=f"<li class='entry {space_replacer(row_key)}_entry'>{row_key}: {row_item}</li>"
                row_entry=""
                cardmiddle=cardmiddle+row_entry

        cardmiddle=f"<ul class='card_ul' data-instance='{space_replacer(key)}_ul' id='{space_replacer(key)}_ul'>{cardmiddle}</ul>"
        cards=cards+cardstart.format(cardmiddle)

    #add filter button before card start
    component_filter,component_filter_js=return_component_filter(tab, df)
    component_filter=component_filter+"<hr/>"

    #component_cy, component_cy_js=return_component_cy(dict_df=dict_df, highlight_classes=[tab], only_nodes=[tab]+return_array_related_classes(tab=tab,connections=2),height="height50")
    component_cy, component_cy_js=return_component_cy(dict_df=dict_df, highlight_classes=[tab], only_nodes=[x for x in dict_df.keys()],height="height50")



    iframe=f"<iframe src='{return_string_gallery(tab)}' height='100%' width='100%'  style='margin-left=-50px !important; margin-right=-50px !important;'></iframe><hr/>"

    if "Department" in tab:
        iframe = "<iframe src='https://nio.feishu.cn/wiki/wikcnE50PKAKxW6u0IaIOyxyzTd#mindmap' height='100%' width='100%' ></iframe><hr/>" +iframe

    direct_relation_label=return_component_small_header(is_direct=True)
    indirect_relation_label=return_component_small_header(is_direct=False)
    header=return_component_header(df,tab, dict_df, instance="")
    template_card=return_template_card()

    part_direct=(return_component_spacer()+direct_relation_label+iframe)
    part_inddirect=(return_component_spacer()+indirect_relation_label+component_cy+cards)

    content= header+part_direct+part_inddirect
    return template.format(content=content  ,
                           jsinclude=component_cy_js+component_filter_js)






def return_content_index(dict_df):
    h1 = f'<h2 class="pt-5 pb-1"><i class="fa-solid fa-face-smile-wink fa-xl"></i> What is to mc?? system?</h2>'
    explainer = f'<p class="fs-1 pb-3 text-secondary">mc?? is a system made by <b>CJ</b> to understand complex relations within NIO Europe: such as process relations, user journey, strategy to process relations and more. Mc?? stands for Energy and is derived from the famous equation E=mc??. The mission is to enable all people and give them energy.</p><hr/>'
    p = f'<p class="fs-1  text-secondary">  <ul><b>How to Use:</b><li> <b>Left Click</b>: move entity around.</li><li><b>Right Click</b>: jump to the details page.</li><li><b>Mouse Wheel</b>: zoom in and out.</li></ul></p>'
    p2 = f'<p class="fs-1  text-secondary">  <ul><b>Useful Examples:</b><li> <b>Employee -> Employee Process -> KPI</b>: Show all relevant KPIs to one employee from his perspective. </li><li><b>KPI -> Employee Process -> Employee</b>: See all relevant People related to one KPI. Useful for leaders. </li><li><b>Role -> Employee -> System</b>: See all systems that a particular role is using</li></ul></p>'

    cy,chart_js=return_component_cy(dict_df, highlight_classes=[x for x in dict_df.keys()], only_nodes=[x for x in dict_df.keys()])
    return template.format(content=h1 + explainer + p + cy + p2 , jsinclude=chart_js)





def return_component_filter(tab, df):
    template_filter="""<div class="dropdown"> <button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton" style="width:100%;"    data-bs-toggle="dropdown" aria-expanded="false">Select Direct Attribute</button>   <ul class="dropdown-menu" id='filter_ul' aria-labelledby="dropdownMenuButton">       {}    </ul>    </div>"""
    items=""
    for col in df.columns:
        if col !=tab:
            item=f"""<li class="dropdown-item"><div class="form-check">
                    <input class="form-check-input big-checkbox" type="checkbox" value="{space_replacer(col)}_filter" id="{space_replacer(col)}_filter" checked />
                    <label class="form-check-label" for="{space_replacer(col)}_filter">&nbsp;{col}</label>
                </div></li>"""
            items=items+item

    js_part=""
    for col in df.columns:
        if col != tab:
            js_part_entry=""" $('#"""+f"{space_replacer(col)}_filter"+ """').change(function() {if(this.checked) { $('."""+f"{space_replacer(col)}_entry"+"""').show();}else{  $("."""+f"{space_replacer(col)}_entry"+"""").hide();  } }); """
            js_part=js_part+js_part_entry
    js_part=f"<script>{js_part}</script>"


    indirect_class = """
    <select class="form-select" aria-label="Default select example" id="indirect_class">
    <option selected>Select Indirect Attribute</option>
    </select>
    """

    indirect_attribute = """
        <select class="form-select" aria-label="Default select example" id="indirect_attribute">
        </select>
        """


    return [template_filter.format(items),js_part]



def return_component_cy(dict_df, only_nodes=[],highlight_classes=["Employee"], height="height100"):
    """cy=cytoscape.js"""
    cy = f"<div id='cy' lul='lol' class='border border-secondary border-5 rounded mb-3 {height}'></div>"

    js_partstart = """
    $(document).ready(function () {
    var cy = cytoscape({
      container: document.getElementById('cy'), // container to render in
    wheelSensitivity:0.05,
     autounselectify: false,
      elements: [ // list of graph elements to start with
        """
    js_middle = ""

    dict_df={x: dict_df[x] for x in only_nodes}

    # add nodes
    for tab, df in dict_df.items():
        js_middle = js_middle + '{ data: { id: "' + tab + f'",  label:"{tab.replace("_", " ")}", href: "' + f'../../mc2/{tab}/{tab}.html' + '"} },'

    checklist = []
    # add edges
    for tab, df in dict_df.items():
        for column in df.columns:
            if "For " in column or "By " in column:
                entity = column.replace("For ", "").replace("By ", "")

                if entity in dict_df:
                    if f"{entity}_{tab}" not in checklist:
                        checklist += [f"{entity}_{tab}", f"{tab}_{entity}"]
                        js_middle = js_middle + "{ data: { id: '" + tab + "" + entity + "', " + f"source:'{tab}', " + f"target:'{entity}'" + '   }},'

                else:
                    print(tab, entity)

    lyioytu = """
    { // edge ab
      data: { id: 'egal', source: 'Department', target: 'Employee' }
    }
    """

    js_partend = """

      ],

      style: [ // the stylesheet for the graph
        {
          selector: 'node',
          style: {
            'background-color': '#999',
            'shape':'round-rectangle',
            'label': 'data(label)',
            'width': '90px',
            'height': '50px',
            'color': '#fff',
            'text-halign': 'center',
            'text-valign': 'center',
            'text-wrap': 'wrap',
            'text-max-width': "5px",
            'text-overflow-wrap': "whitespace",
          }
        },
        {
          selector: '.red',
          css: {
            'background-color': 'red',
            'line-color': 'red',
            'z-index': 99999,
          }
        },
        
        {
          selector: '.blue',
          css: {
            'background-color': '#0099ff',
          }
        },
        
        {
          selector: 'edge.blue',
          css: {
            'line-color': 'red',
          }
        },
        
        {
          selector: '.edge_default',
          css: {
            'line-color': '#eee',
            'z-index':-1,
          }
        },


        {
          selector: 'edge',
          style: {
            'width': 4,
            'target-arrow-color': '#ccc',
            'target-arrow-shape': '',
            'curve-style': 'bezier'
          }
        }
      ],

      layout: {
        name: 'breadthfirst', 
        spacingFactor: 0.85, 
        avoidOverlap: true,
        animate: true,
        animationDuration: 1000,
      },
      ready: function(){
        
      }

    });



    //initialization
    var current_class =get_current_class();
    var current_class_attributes=return_attributes(current_class);
    cy.$('edge').addClass('edge_default');
    cy.$('"""+ ",".join(["#"+x for x in highlight_classes])+ """').addClass('blue');
    if (current_class){traverse_to(current_class,current_class,cy);}
  
    
    
    
    // right click even to jump to next page
    cy.on('cxttap', 'node', function(){
      try { // your browser may block popups
        window.open( this.data('href') ,"_self");
      } catch(e){ // fall back on url change
        window.location.href = this.data('href');
      }
    }); 

    // bind tapstart to edges and highlight the connected nodes
    cy.bind('tapstart', 'edge', function(event) {
      var connected = event.target.connectedNodes();
      //connected.addClass('blue');
    });


    // bind tapend to edges and remove the highlight from the connected nodes
    cy.bind('tapend', 'edge', function(event) {
      var connected = event.target.connectedNodes();
      //connected.removeClass('blue');
    });
    
    // bind tapend to node and remove the highlight from the connected nodes
    cy.bind('tapstart', 'node', function(event) { 
    update_card_display(cy,event);  
    });//end of binding
    
});//end of jquery.ready
"""

    chart_js = js_partstart + js_middle + js_partend
    return [cy,f"<script>{chart_js}</script>"]


def create_html():
    #classes
    dict_df,wb=get_dict_df()
    dict_extrawurst = {}
    for tab, df in dict_df.items():
        Path(f"paste to github/mc2/{tab}").mkdir(parents=True, exist_ok=True)
        if tab in dict_extrawurst:
            result=dict_extrawurst[tab](tab,df,dict_df)
        else:
            result=return_content_class(tab=tab, df=df,dict_df=dict_df)
        with open(fr"paste to github/mc2/{tab}/{tab}.html", "w", encoding="utf-8") as file:
            file.write(str(result))


    #instances
    for tab, df in dict_df.items():
        Path(f"paste to github/mc2/{tab}").mkdir(parents=True, exist_ok=True)
        try:
            df.set_index(tab, inplace=True)
        except:
            pass
        for instance, row in df.iterrows():
            if instance and not pd.isna(instance) and instance is not None:
                result = return_content_instance(instance=instance, row=row, tab=tab, dict_df=dict_df)
                # change the word primary to success
                result = result.replace("primary", 'primary')
                with open(fr"paste to github/mc2/{tab}/{instance}.html", "w", encoding="utf-8") as file:
                    file.write(str(result))

    #index html
    Path(f"paste to github/mc2/index").mkdir(parents=True, exist_ok=True)
    result = return_content_index(dict_df)


    with open(fr"paste to github/mc2/index/index.html", "w", encoding="utf-8") as file:
        file.write(str(result))






if __name__ == '__main__':

    create_class_map()
    return_global_navbar()
    return_global_html()
    create_html()





