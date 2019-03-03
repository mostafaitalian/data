from io import StringIO
from django import template
from ..models import Post

register = template.Library()

'''@register.simple_tag
def format_post_list(post_list):
    indent = ' '
    output = StringIO()
    output.write('<ul>\n')
    for post in post_list:
        output.write('{}<li><a href={}>\n'.format(indent, post.get_absolute_url()))
        output.write('{}{}\n'.format(indent*2,post.title.title()))
        output.write('</a></li>\n')
        output.write('</ul>\n')
    return output.getvalue()'''
@register.inclusion_tag('blog/partial_post_list.html')
def format_post_list(post_list):
    return{'post_list':post_list}
    
    
@register.inclusion_tag('blog/partial_post_list.html', takes_context=True)
def forrmat_post_list(context, detail_object):
    request = context.get('request')
    if request.user.has_perm('blog.view_future_post'):
        post_list = detail_object.blog_posts.all()
    else:
        post_list = detail_object.published_posts()
    return {'post_list':post_list}