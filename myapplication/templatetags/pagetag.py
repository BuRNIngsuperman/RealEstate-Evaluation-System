# _*_coding:utf-8 _*_
from  django import  template
register = template.Library()

from django.utils.html import format_html
@register.simple_tag
def circle_page(curr_page,loop_page):
    offset = abs(curr_page-loop_page)
    if offset<3:
        if curr_page==loop_page:
            page_ele='<li class="active"><a href="?page=%s">%s</a></li>'%(loop_page,loop_page)
        else:
            page_ele='<li><a href="?page=%s">%s</a></li>'%(loop_page,loop_page)
        return format_html(page_ele)
    else:
        return ''

@register.simple_tag
def circle_pagesearch(curr_page,loop_page,search):
    offset = abs(curr_page-loop_page)
    if offset<3:
        if curr_page==loop_page:
            page_ele='<li class="active"><a href="?page=%s&localarea=%s">%s</a></li>'%(loop_page,search,loop_page)
        else:
            page_ele='<li><a href="?page=%s&localarea=%s">%s</a></li>'%(loop_page,search,loop_page)
        return format_html(page_ele)
    else:
        return ''
