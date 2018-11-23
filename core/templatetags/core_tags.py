from django.template import Library
from tasks.views import check_write_comment as check_write_comment_method

register = Library()

@register.simple_tag
def check_write_comment(task, user):
    return check_write_comment_method(task, user)