from collections import namedtuple
from functional import seq
import os
import yaml

POST_CONFIG_FILE = 'post.yml'
POST_FIELDS = [
    'path',
    'publish_date',
    'title',
    'author'
]
POST_DEFAULTS = {
    'path': 'index.html'
}

Directory = namedtuple('Directory', ['path', 'dirnames', 'filenames'])
PostClassTemplate = namedtuple('Post', POST_FIELDS)
class Post(PostClassTemplate):

    @classmethod
    def from_directory(cls, directory):
        # Load Config File
        config_path = os.path.join(directory.path, POST_CONFIG_FILE)
        with open(config_path, 'r') as infile:
            config = yaml.load(infile)
        
        # Load config defaults
        for (key, default) in POST_DEFAULTS.iteritems():
            if key not in config:
                config[key] = default

        # Reject malformed config
        missing_fields = list(filter(
                lambda field: field not in config.keys(),
                POST_FIELDS
        ))

        if missing_fields:
            logger.warn(
                "Post described in {} missing: {}"
                .format(config_path, ", ".join(missing_fields))
            )
            return None
        else:
            return cls(**config)


def _get_posts(path):
    return (
        seq(os.walk(path))
        .map(lambda d: Directory(*d))
        .filter(lambda d: POST_CONFIG_FILE in d.filenames)
        .map(Post.from_directory)
    )


def build_index(path):
    posts = _get_posts(path)
    return(posts)





# def flatten_filepath(dirpath, filenames):
#     return map(lambda f: os.path.join(dirpath, f), filenames)
# 
