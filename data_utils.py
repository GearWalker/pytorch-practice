import gzip
import os
from os import path
import numpy as np
import tarfile

import sys
if sys.version_info.major < 3:
    import urllib
else:
    import urllib.request as request


DATASET_DIR = 'datasets/'

MNIST_FILES = ["train-images-idx3-ubyte.gz", "train-labels-idx1-ubyte.gz",
               "t10k-images-idx3-ubyte.gz", "t10k-labels-idx1-ubyte.gz"]

FASHION_MNIST_FILES =  ["train-images-idx3-ubyte.gz", "train-labels-idx1-ubyte.gz",
                        "t10k-images-idx3-ubyte.gz", "t10k-labels-idx1-ubyte.gz"]

def download_file(url, local_path):
    dir_path = path.dirname(local_path)
    if not path.exists(dir_path):
        print("Creating the directory '%s' ..." % dir_path)
        os.makedirs(dir_path)

    print("Downloading from '%s' ..." % url)
    if sys.version_info.major < 3:
        urllib.URLopener().retrieve(url, local_path)
    else:
        request.urlretrieve(url, local_path)


def download_mnist(local_path):
    url_root = "http://yann.lecun.com/exdb/mnist/"
    for f_name in MNIST_FILES:
        f_path = os.path.join(local_path, f_name)
        if not path.exists(f_path):
            download_file(url_root + f_name, f_path)

def download_fashion_mnist(local_path):
    url_root = "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/"
    for f_name in FASHION_MNIST_FILES:
        f_path = os.path.join(local_path, f_name)
        if not path.exists(f_path):
            download_file(url_root + f_name, f_path)

def download_rt(local_path):
    url = "http://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.tar.gz"
    data_file = os.path.join(local_path,'rt-polaritydata.tar.gz')
    download_file(url, data_file)
    
    tar = tarfile.open(data_file)
    tar.extractall(path=local_path)
    tar.close()
            
def one_hot(x, n):
    if type(x) == list:
        x = np.array(x)
    x = x.flatten()
    o_h = np.zeros((len(x), n))
    o_h[np.arange(len(x)), x] = 1
    return o_h


def load_mnist(ntrain=60000, ntest=10000, onehot=True):
    data_dir = os.path.join(DATASET_DIR, 'mnist/')
    if not path.exists(data_dir):
        download_mnist(data_dir)
    else:
        # check all files
        checks = [path.exists(os.path.join(data_dir, f)) for f in MNIST_FILES]
        if not np.all(checks):
            download_mnist(data_dir)

    with gzip.open(os.path.join(data_dir, 'train-images-idx3-ubyte.gz')) as fd:
        buf = fd.read()
        loaded = np.frombuffer(buf, dtype=np.uint8)
        trX = loaded[16:].reshape((60000, 28 * 28)).astype(float)

    with gzip.open(os.path.join(data_dir, 'train-labels-idx1-ubyte.gz')) as fd:
        buf = fd.read()
        loaded = np.frombuffer(buf, dtype=np.uint8)
        trY = loaded[8:].reshape((60000))

    with gzip.open(os.path.join(data_dir, 't10k-images-idx3-ubyte.gz')) as fd:
        buf = fd.read()
        loaded = np.frombuffer(buf, dtype=np.uint8)
        teX = loaded[16:].reshape((10000, 28 * 28)).astype(float)

    with gzip.open(os.path.join(data_dir, 't10k-labels-idx1-ubyte.gz')) as fd:
        buf = fd.read()
        loaded = np.frombuffer(buf, dtype=np.uint8)
        teY = loaded[8:].reshape((10000))

    trX /= 255.
    teX /= 255.

    trX = trX[:ntrain]
    trY = trY[:ntrain]

    teX = teX[:ntest]
    teY = teY[:ntest]

    if onehot:
        trY = one_hot(trY, 10)
        teY = one_hot(teY, 10)
    else:
        trY = np.asarray(trY)
        teY = np.asarray(teY)

    return trX, teX, trY, teY

def load_fashion_mnist(ntrain=60000, ntest=10000, onehot=True):
    data_dir = os.path.join(DATASET_DIR, 'fashion_mnist/')
    if not path.exists(data_dir):
        download_fashion_mnist(data_dir)
    else:
        # check all files
        checks = [path.exists(os.path.join(data_dir, f)) for f in FASHION_MNIST_FILES]
        if not np.all(checks):
            download_mnist(data_dir)

    with gzip.open(os.path.join(data_dir, 'train-images-idx3-ubyte.gz')) as fd:
        buf = fd.read()
        loaded = np.frombuffer(buf, dtype=np.uint8)
        trX = loaded[16:].reshape((60000, 28 * 28)).astype(float)

    with gzip.open(os.path.join(data_dir, 'train-labels-idx1-ubyte.gz')) as fd:
        buf = fd.read()
        loaded = np.frombuffer(buf, dtype=np.uint8)
        trY = loaded[8:].reshape((60000))

    with gzip.open(os.path.join(data_dir, 't10k-images-idx3-ubyte.gz')) as fd:
        buf = fd.read()
        loaded = np.frombuffer(buf, dtype=np.uint8)
        teX = loaded[16:].reshape((10000, 28 * 28)).astype(float)

    with gzip.open(os.path.join(data_dir, 't10k-labels-idx1-ubyte.gz')) as fd:
        buf = fd.read()
        loaded = np.frombuffer(buf, dtype=np.uint8)
        teY = loaded[8:].reshape((10000))

    trX /= 255.
    teX /= 255.

    trX = trX[:ntrain]
    trY = trY[:ntrain]

    teX = teX[:ntest]
    teY = teY[:ntest]

    if onehot:
        trY = one_hot(trY, 10)
        teY = one_hot(teY, 10)
    else:
        trY = np.asarray(trY)
        teY = np.asarray(teY)

    return trX, teX, trY, teY

def load_rt():
    data_dir = os.path.join(DATASET_DIR, 'rt/')
    
    if not (path.exists(data_dir+'rt-polaritydata/rt-polarity.pos') and path.exists(data_dir+'rt-polaritydata/rt-polarity.neg')):
        download_rt(data_dir)
    
    positive_data_file = data_dir+'rt-polaritydata/rt-polarity.pos'
    negative_data_file = data_dir+'rt-polaritydata/rt-polarity.neg'
    
    # Load data from files
    positive_examples = list(open(positive_data_file, "rb").readlines())
    positive_examples = [s.strip() for s in positive_examples]
    negative_examples = list(open(negative_data_file, "rb").readlines())
    negative_examples = [s.strip() for s in negative_examples]
            
    positive_examples = [p.decode("latin-1") for p in positive_examples]
    negative_examples = [n.decode("latin-1") for n in negative_examples]

    return positive_examples, negative_examples