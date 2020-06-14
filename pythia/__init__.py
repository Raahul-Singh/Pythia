from pythia import cleaning, eda, learning, net, seo

__all__ = ['cleaning', 'eda', 'learning', 'net', 'seo']

from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass  # package is not installed
