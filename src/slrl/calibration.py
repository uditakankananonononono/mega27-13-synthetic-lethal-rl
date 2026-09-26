"""Monogenic model calibration on development cell lines only.

No single-perturbation dataset can identify pair/triple epistasis or normal selectivity.
"""
import numpy as np

def normalize_dependency_matrix(matrix):
    """Map CERES gene effect to log-loss proxy after clipping and return coverage mask.

    Fixed transform avoids claiming viability units. CERES -1 is typical core essential;
    0 is nonessential. Proxy scale is arbitrary and must be calibrated independently.
    """
    x=np.asarray(matrix,float)
    if x.ndim!=2:raise ValueError('model-by-gene matrix required')
    valid=np.isfinite(x)
    if not valid.all(axis=1).any():raise ValueError('no complete model')
    proxy=np.where(valid,np.clip(-x,0,2),np.nan)
    return proxy,valid

def holdout_models(proxy,heldout_indices):
    heldout=set(heldout_indices)
    if not heldout or any(x<0 or x>=len(proxy) for x in heldout):raise ValueError('bad holdout indices')
    train=np.array([i for i in range(len(proxy)) if i not in heldout])
    test=np.array(sorted(heldout))
    if not len(train):raise ValueError('no training models')
    return proxy[train],proxy[test]

def shrink_gene_mean(train,prior=0.2):
    """Transparent no-learning baseline; estimate uncertainty from development contexts."""
    x=np.asarray(train,float)
    if x.ndim!=2 or x.shape[0]<2:raise ValueError('>=2 development models required')
    finite=np.isfinite(x);count=finite.sum(axis=0)
    mean=np.divide(np.nansum(x,axis=0),count,out=np.zeros(x.shape[1]),where=count>0)
    shrunk=mean*count/(count+prior)
    variance=np.divide(np.nansum(np.where(finite,(x-mean)**2,0),axis=0),np.maximum(1,count-1))
    uncertainty=np.sqrt(variance+1/np.maximum(count,1))
    uncertainty[count==0]=np.inf
    return shrunk,uncertainty,count
