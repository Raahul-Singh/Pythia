from pkg_resources import DistributionNotFound, get_distribution

from pythia import cleaning, eda, learning, net, seo

__all__ = ['cleaning', 'eda', 'learning', 'net', 'seo']

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass  # package is not installed
