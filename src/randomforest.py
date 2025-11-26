import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
import io

def run_rf_multiclass(dataMatrix, class_col="var", auc_outfile=None, report_txt=None):
    
    """
    Train/test split (80/20) among non-patient controls, then test on Patient samples.
    Saves ROC/AUC plot if auc_outfile is given.
    """

    buffer = io.StringIO()
    out_stream = open(report_txt, "w") if report_txt else None
    target = out_stream if out_stream else buffer

    auc_fig = None
    confusion_mat = None
    patient_preds = None

    with redirect_stdout(target):
        non_patient_df = dataMatrix[dataMatrix[class_col] != "Patient"].copy()
        patient_df = dataMatrix[dataMatrix[class_col] == "Patient"].copy()

        X = non_patient_df.drop(columns=[class_col])
        y = non_patient_df[class_col].astype("category")

        # Stratified train/test split for controls
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=100, stratify=y
        )

        rf = RandomForestClassifier(random_state=100)
        param_grid = {
            "n_estimators": [200, 500],
            "max_features": ["sqrt", "log2"],
            "max_depth": [None, 20, 40],
        }
        grid = GridSearchCV(
            rf,
            param_grid,
            scoring="accuracy",
            cv=5,
            n_jobs=-1
        )

        print("\nFitting model on non-patient train samples...")
        grid.fit(X_train, y_train)
        best_rf = grid.best_estimator_

        print("\nPREDICTING 20% HELD-OUT NON-PATIENT SAMPLES:")
        y_pred = best_rf.predict(X_test)
        confusion_mat = confusion_matrix(y_test, y_pred)
        print("\nConfusion Matrix (non-patient test):")
        print(confusion_mat)
        print("\nClassification Report (non-patient test):")
        print(classification_report(y_test, y_pred, zero_division=0))

        # ROC curve
        if len(best_rf.classes_) > 2:
            probs = best_rf.predict_proba(X_test)
            classes = list(best_rf.classes_)
            colors = ["#F60239","#008607","#9400E6"]
            auc_fig = plt.figure(figsize=(5,5))
            for i, cls in enumerate(classes):
                true_binary = (y_test == cls).astype(int)
                pred_prob = probs[:, i]
                fpr, tpr, _ = roc_curve(true_binary, pred_prob)
                roc_auc = auc(fpr, tpr)
                plt.plot(fpr, tpr, label=f"{cls} (AUC={roc_auc:.2f})", color=colors[i % len(colors)])
            plt.plot([0,1], [0,1], 'k--')
            plt.xlabel("False Positive Rate")
            plt.ylabel("True Positive Rate")
            plt.title("ROC Curves — 20% Non-Patient Test")
            plt.legend()
            plt.tight_layout()
            if auc_outfile:
                plt.savefig(auc_outfile, dpi=300)
                print(f"ROC curve saved to {auc_outfile}")

        # Patient predictions
        if not patient_df.empty:
            X_patient = patient_df.drop(columns=[class_col])
            y_patient = patient_df[class_col].astype("category")
            print("\nTesting trained model on Patient samples:")
            patient_preds = best_rf.predict(X_patient)
            print("Predictions:", list(patient_preds))
            print("\nClassification Report (patients):")
            print(classification_report(y_patient, patient_preds, zero_division=0))

    if out_stream:
        out_stream.close()
    else:
        print(buffer.getvalue())

    return auc_fig, confusion_mat, patient_preds
