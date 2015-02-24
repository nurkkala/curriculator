from django import template

register = template.Library()

@register.simple_tag
def coverage_data(coverage, tier=None):
    if coverage.total(tier):
        return "{}/{}".format(coverage.covered(tier),
                              coverage.total(tier))
    else:
        return "--"


@register.simple_tag
def coverage_class(coverage, tier=None):
    cov = coverage.covered(tier)
    tot = coverage.total(tier)

    if tot == 0:
        return ""
    elif cov == 0:
        return "bg-danger"
    elif cov < tot:
        return "bg-warning"
    else:
        return "bg-success"