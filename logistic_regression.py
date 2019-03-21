"""
Module with my logistic regression implementation based on programming exercise 2 of Machine Learning course on Coursera

Author: Suellen Silva de Almeida (susilvalmeida@gmail.com)
"""

import numpy as np
import scipy.optimize as opt

from util import add_intercept_term_to_X

def sigmoid(z):
    """
    Computes the sigmoid of x
    Formula: 1 / (1+e^(-z))
    Args:
        z (np.array or scalar): the input value or values

    Returns:
        (np.array or scalar): the sigmoid of each value of input z 
    """
    z = np.array(z)
    return 1 / (1+np.exp(-z))

def cost_function(theta, X, y):
    """
    Computs cost and gradient for logistic regression using theta as parameter for logistic regression.
    Args:
        theta (np.array): vector of theta parameters
        X (np.array): matrix of features
        y (np.array): vector with target variable of size

    Returns:
        (float): the cost of using theta as the parameter for logistic regression
        (np.array): the partial derivatives of the cost in each parameter in theta
    """
    m = y.shape[0]
    theta = theta[:, np.newaxis] 
    h = sigmoid(X.dot(theta))
    J = (1/m) * (-y.T.dot(np.log(h)) - (1-y).T.dot(np.log(1-h)))

    diff_hy = h - y
    grad = np.multiply((1/m), diff_hy.T.dot(X))       

    return J, grad

def cost_function_reg(theta, X, y, lambda_reg):
    """
    Computs cost and gradient for logistic regression with regularization using theta as parameter for logistic 
    regression.

    Args:
        theta (np.array): vector of theta parameters
        X (np.array): matrix of features
        y (np.array): vector with target variable of size
        lambda_reg (int): regularization parameters

    Returns:
        (float): the cost of using theta as the parameter for logistic regression
        (np.array): the partial derivatives of the cost in each parameter in theta
    """
    m = y.shape[0]
    theta = theta[:, np.newaxis] 
    h = sigmoid(X.dot(theta))
    J = (1/m) * (-y.T.dot(np.log(h)) - (1-y).T.dot(np.log(1-h))) + (lambda_reg/(2*m)) * np.sum(theta[1:]**2)

    diff_hy = h - y
    grad = (1/m) * diff_hy.T.dot(X) + ((lambda_reg/m) * theta.T)
    grad[0, 0] = (1/m) * diff_hy.T.dot(X[:, 0])

    return J, grad

def fit(X, y, lambda_reg=None):
    """
    Fit the logistic regression model, that is, compute best value of parameteres theta.
    If the lambda regularization parameter is None, fits the logistic regression with regularization and if it's a int,
    fits with regularization.

    Args:
        X (list): matrix of features
        y (list): vector with target variable
        lambda_reg (int): the regularization parameters
    Returns:
        dict: Dictionary with matrix X, theta values, cost of using theta as the parameter for logistic regression
    """
    X = np.array(X, dtype=float)
    if len(X.shape) == 1:
        X = X.reshape(-1, 1)
    X = add_intercept_term_to_X(X)
    y = np.array(y, dtype=float).reshape(-1, 1)

    initial_theta = np.zeros(shape=(X.shape[1]))

    if lambda_reg is None:
        results = opt.minimize(cost_function, initial_theta, args=(X, y), method='TNC',
                               jac=True, options={'maxiter':400})
    else:
        results = opt.minimize(cost_function_reg, initial_theta, args=(X, y, lambda_reg), method='TNC',
                               jac=True, options={'maxiter':400})

    fitted_model = {
        'X': X,
        'theta': results['x'],
        'cost': results['fun']
    }

    return fitted_model

def predict(X, fitted_model):
    """
    Uses the fitted_model dict generated in fit method to predict the class of each example in X.

    Args:
        X (list): matrix of features
        fitted_model (dict): Dictionary generated by the fit method with theta
    Returns:
        list: predicted class of each example in X
    """
    X = np.array(X, dtype=float)
    if len(X.shape) == 1:
        X = X.reshape(-1, 1)

    X = add_intercept_term_to_X(X)

    y_pred = [1 if sigmoid(X[i, :].dot(fitted_model['theta'])) >= 0.5 else 0 for i in range(0, X.shape[0])]
    return y_pred
