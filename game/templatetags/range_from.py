from django import template

register = template.Library()

@register.filter(name='range_from')
def range_from(num, arg):
    """Provides numerical ranges.
    
    Filters over an integer giving the number of elements to generate.
    
    Examples:
        5|range_from:"0" - produces 5 integers starting from 0.
        3|range_from:"5:10" - produces 3 integers starting from 5, with increments of 10.
    """
    num = int(num)
    arg = arg.split(',')
    fr = int(arg[0])
    by = int(arg[1]) if len(arg) > 1 else 1
    return range(fr, fr + num * by, by)
