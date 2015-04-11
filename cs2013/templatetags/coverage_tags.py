from django import template

register = template.Library()

def _coverage_fraction(covered, total):
    if total:
        return "{}/{}".format(covered, total)
    else:
        return "&mdash;"

def _coverage_class(covered, total):
    if total == 0:
        return ""
    elif covered == 0:
        return "bg-danger"
    elif covered < total:
        return "bg-warning"
    else:
        return "bg-success"

@register.simple_tag
def unit_coverage_fraction(unit_coverage, tier=None):
    return _coverage_fraction(unit_coverage.covered(tier),
                              unit_coverage.total(tier))

@register.simple_tag
def unit_coverage_class(unit_coverage, tier=None):
    return _coverage_class(unit_coverage.covered(tier),
                           unit_coverage.total(tier))

@register.simple_tag
def area_coverage_fraction(area_coverage):
    return _coverage_fraction(area_coverage['covered'],
                              area_coverage['total'])

@register.simple_tag
def area_coverage_class(area_coverage):
    return _coverage_class(area_coverage['covered'],
                           area_coverage['total'])
