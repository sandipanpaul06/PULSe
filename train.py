import pulearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, auc
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from pulearn import ElkanotoPuClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.utils import shuffle
import argparse

# Create the main parser for all arguments
parser = argparse.ArgumentParser(description= 'Effect of calibration')
# These arguments are always required
parser.add_argument('-u', type=int, help= 'Number of samples on the unlabeled set', required=True)
parser.add_argument('-l', type=int, help= 'Number of samples on the labeled set', required=True)
parser.add_argument('-lp', type=str, help= 'Labeled positive filename prefix', required=True)
parser.add_argument('-pipeline', type=str, choices=['P1', 'P2'], help='P1 or P2', required=True)
parser.add_argument('-testcase', type=int, choices=[0, 1], help='0: simulated unlabeled set, 1: empirical unlabeled set', required=True)
parser.add_argument('-testname', type=str, help='Test name', required=True)

# These arguments are optional and will be checked conditionally
parser.add_argument('-p', type=int, help= 'Percentage of positives in the unlabeled set (testcase 0 only)')
parser.add_argument('-up', type=str, help='Unlabeled positive filename prefix (testcase 0 only)')
parser.add_argument('-un', type=str, help='Unlabeled negative filename prefix (testcase 0 only)')
parser.add_argument('-emp', type=str, help='Empirical filename (testcase 1 only)')

# Parse all arguments at once
args = parser.parse_args()

# Now, perform the conditional check and raise an error if required arguments are missing
if args.testcase == 0:
    # Check if arguments for simulated test case are provided
    if args.up is None or args.un is None:
        parser.error("For testcase 0, both '-up' and '-un' arguments are required.")
    # Check if arguments for empirical test case are provided
    if args.emp is not None:
        parser.error("For simulated testcase, '-emp' not allowed.")
elif args.testcase == 1:
    # Check if arguments for empirical test case are provided
    if args.emp is None:
        parser.error("For testcase 1, '-emp' required.")
    # Check if arguments for simulated test case are provided
    if args.up is not None or args.un is not None:
        parser.error("For empirical testcase, '-up' and '-un' arguments are not allowed.")




if args.pipeline == 'P1':
    suffix = '0_6163'
elif args.pipeline == 'P2':
    suffix = '1_9163'


LP = np.load(f'./HOG_datasets/{args.lp}_HOGfeatures_{suffix}.npy')[:args.l]
LP = pd.DataFrame(LP)

if args.testcase == 0:

    nP = int(args.u * (args.p/100))
    nN = int(args.u - nP)

    print(f'Unlabeled set: number of positives {nP}, number of negatives {nN}')

    UP = np.load(f'./HOG_datasets/{args.up}_HOGfeatures_{suffix}.npy')[:nP]
    UP = pd.DataFrame(UP)
    UN = np.load(f'./HOG_datasets/{args.un}_HOGfeatures_{suffix}.npy')[:nN]
    UN = pd.DataFrame(UN)

    X_train = pd.concat([LP, UP, UN], ignore_index=True)
    X_train_U = pd.concat([UP, UN], ignore_index=True)
    X_train_L = LP
    
    Y_train = np.array([1]*args.l + [0]*args.u)
    Y_train_U = np.array([1]*nP + [0]*nN)

elif args.testcase == 1:
    EMP = np.load(f'./HOG_datasets/{args.emp}_HOGfeatures_{suffix}.npy')
    EMP = pd.DataFrame(EMP)

    X_train = pd.concat([LP, EMP], ignore_index=True)
    X_train_U = EMP
    X_train_L = LP
    
    Y_train = np.array([1]*args.l + [0]*args.u)



XY_train_df = X_train.copy()
XY_train_df['actual_label'] = Y_train
XY_train_df = XY_train_df.sample(frac = 1)
X_train_shuffled = np.array(XY_train_df.iloc[:,:-1])
Y_train_shuffled = np.array(XY_train_df.iloc[:,-1])



print('training ...')


logreg = LogisticRegression(max_iter=20000)
pu_estimator = ElkanotoPuClassifier(estimator=logreg, hold_out_ratio=0.2)

pu_estimator.fit(X_train_shuffled, Y_train_shuffled)
Y_train_U_pred = pu_estimator.predict_proba(X_train_U)   #X_train_U
y_train_U_proba = Y_train_U_pred/(Y_train_U_pred[0][0] + Y_train_U_pred[0][1])
y_train_U_sweep_proba = y_train_U_proba[:, 1]

if args.testcase == 0:
    sacc = sum(Y_train_U[:nP] == (y_train_U_sweep_proba[:nP] >= 0.5).astype(int))/nP
    nacc = sum(Y_train_U[nP:] == (y_train_U_sweep_proba[nP:] >= 0.5).astype(int))/nN
    precision, recall, _ = precision_recall_curve(Y_train_U, y_train_U_sweep_proba)
    auc_pr = auc(recall, precision)
    print(f'Sweep detection Accuracy: {sacc} , \nNeutral detection Accuracy: {nacc}, \nAUC-PR: {auc_pr}')

np.savetxt(f'./Predictions/PULSe_{args.pipeline}_{args.testname}_predictions_raw.txt', np.array(y_train_U_sweep_proba))

if args.testcase == 0:
    np.savetxt(f'./Predictions/PULSe_{args.pipeline}_{args.testname}_trueLabels.txt', np.array(Y_train_U))

Y_train_L_pred = pu_estimator.predict_proba(X_train_L)   #X_train_U
y_train_L_proba = Y_train_L_pred/(Y_train_U_pred[0][0] + Y_train_U_pred[0][1])
y_probL0 = y_train_L_proba[:, 1]

np.savetxt(f'./Predictions/PULSe_{args.pipeline}_{args.testname}_labeled_predictions.txt', np.array(y_probL0))
