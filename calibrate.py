import numpy as np
from sklearn.utils import shuffle
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve, precision_recall_curve, matthews_corrcoef, auc
import argparse

parser = argparse.ArgumentParser(description='PULSe calibration')
parser.add_argument('-testname', type=str, help='Test name', required = True)
parser.add_argument('-pipeline', type=str, choices=['P1', 'P2'], help='P1 or P2', required=True)
parser.add_argument('-testcase', type=int, choices=[0, 1], help='0: simulated unlabeled set, 1: empirical unlabeled set', required=True)
parser.add_argument('-T', type=float, help='Calibration threshold', required = True)



args = parser.parse_args()

def calibrate_with_isotonic_threshold(y_iso, y_prob0, y_probL, threshold=0.5):
    y_prob0_selected = y_prob0[y_prob0 <= threshold]
    X_iso = np.concatenate([y_prob0_selected, y_probL])
    label_iso = np.array([0] * len(y_prob0_selected) + [1] * len(y_probL))
    X_iso, label_iso = shuffle(X_iso, label_iso, random_state=42)
    iso_model = IsotonicRegression(out_of_bounds='clip').fit(X_iso.reshape(-1, 1), label_iso)
    y_prob1 = iso_model.predict(y_iso.reshape(-1, 1))
    return y_prob1


y_prob = np.loadtxt(f'./Predictions/PULSe_{args.pipeline}_{args.testname}_predictions_raw.txt')
y_probL = np.loadtxt(f'./Predictions/PULSe_{args.pipeline}_{args.testname}_labeled_predictions.txt')
y_prob1 = calibrate_with_isotonic_threshold(y_prob, y_prob, y_probL, threshold=args.T)


if args.testcase ==0:
    y_true0 = np.loadtxt(f'./Predictions/PULSe_{args.pipeline}_{args.testname}_trueLabels.txt')
    y_prob1_binary = (y_prob1 >= 0.5).astype(int)
    mcc = matthews_corrcoef(y_true0, y_prob1_binary)
    precision, recall, _ = precision_recall_curve(y_true0, y_prob1)
    auprc = auc(recall, precision)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(len(y_prob1_binary)):
        if y_true0[i] ==1 and y_prob1_binary[i] ==1:
            tp+=1
        elif y_true0[i] ==0 and y_prob1_binary[i] ==0:
            tn+=1
        elif y_true0[i] ==1 and y_prob1_binary[i] ==0:
            fn+=1
        if y_true0[i] ==0 and y_prob1_binary[i] ==1:
            fp+=1
    print(f'Sweep Accuracy: {tp/(tp+fn)}')
    print(f'Neutral Accuracy: {tn/(tn+fp)}')
    print(f"MCC: {mcc:.4f}")
    print(f"AUPRC: {auprc:.4f}")

np.savetxt(f'./Predictions/PULSe_{args.pipeline}_{args.testname}_predictions_calibrated.txt', np.array(y_prob1))