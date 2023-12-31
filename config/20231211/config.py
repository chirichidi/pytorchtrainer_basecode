import torch
import torch.nn as nn
import torchmetrics

from torchmetrics.classification import BinaryAccuracy, BinaryPrecision, BinaryRecall, BinaryF1Score, BinaryAUROC
from models.ann import ANN

from sklearn.impute import KNNImputer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler 
from sklearn.preprocessing import OneHotEncoder
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE


numerical = ['HE_chol', 'HE_HCT', 'HE_RBC', 'HE_HB', 'HE_Uph', 'HE_dbp', 'HE_crea', 'HE_Bplt', 'HE_alt', 'HE_glu', 'HE_TG', 'age', 'HE_HDL_st2', 'HE_Usg', 'HE_WBC', 'HE_ast', 'HE_BUN', 'HE_wt', 'ainc', 'HE_sbp', 'HE_ht', 'HE_wc']
onehot = ['HE_Uglu', 'HE_Unitr', 'sex', 'educ', 'HE_obe', 'DI2_pt', 'DI3_pt', 'BH2_61', 'npins', 'BM1_3', 'marri_1', 'DI1_pt', 'BO1_1', 'HE_Upro', 'BM1_6', 'LQ1_sb', 'BM1_4', 'DJ4_pr', 'HE_Ubil', 'BM1_7', 'HE_Uket', 'BM1_1', 'BM1_2', 'LQ2_ab', 'HE_Ubld', 'BM1_5', 'DE1_pr', 'BS9_2', 'DE1_pt', 'tins', 'EC_occp', 'BD1', 'HE_rPLS', 'live_t', 'HE_Uro', 'D_2_1', 'BO1', 'LQ4_00', 'DJ4_pt', 'EC_stt_1', 'DI3_pr', 'BH1', 'occp', 'DI2_pr', 'BH9_11', 'EC_stt_2', 'BS8_2', 'BM1_8', 'BO2_1', 'DI1_pr']
label = ['BA2_13', 'house', 'ho_incm', 'DI3_2', 'cfam', 'BE5_1', 'edu', 'BD1_11', 'incm', 'ho_incm5', 'D_1_1', 'BA2_12', 'incm5', 'BS3_1', 'BD2_1', 'BE3_31']


y_related =["BP_PHQ_1","BP_PHQ_2","BP_PHQ_3","BP_PHQ_4","BP_PHQ_5","BP_PHQ_6","BP_PHQ_7","BP_PHQ_8","BP_PHQ_9","mh_PHQ_S","BP6_10","BP6_31","DF2_pr","DF2_pt","BP1"]
y = "depressed"

config = {
    "name": "train_X_231211",
    "model": {
        "class": ANN,
        "module_list": nn.ModuleList([
            nn.Linear(220, 32), # 220
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1),
            nn.Sigmoid()
        ]),
    },
    "data": {
        "train_X": {
            "path": "data/train_X_231211.csv",
            "index_col": None,
        },
        "train_y": {
            "path": "data/train_y_231211.csv",
            "index_col": None,
        },
        "test_X": {
            "path": "data/test_X_231211.csv",
            "index_col": None,
        },
        "test_y": {
            "path": "data/test_y_231211.csv",
            "index_col": None,
        },
        "transform": {
            "steps": [
                {
                    KNNImputer: {
                        "params": {
                            "n_neighbors": 5,
                            "weights": "uniform",
                            "missing_values": float("nan"),
                        },
                        "fit_transform_cols": numerical
                    }
                },
                {
                    SimpleImputer: {
                        "params": {
                            "missing_values": float("nan"),
                            "strategy": "most_frequent",
                        },
                        "fit_transform_cols": onehot
                    }
                },
                {
                    SimpleImputer: {
                        "params": {
                            "strategy": "most_frequent",
                        },
                        "fit_transform_cols": label
                    }
                },
                {
                    MinMaxScaler: {
                        "params": {
                            "feature_range": (0, 1),
                        },
                        "fit_transform_cols": numerical
                    }
                },
                {
                    OneHotEncoder: {
                        "params": {
                            "sparse": False,
                        },
                        "fit_transform_cols": onehot
                    }
                },
                {
                    RandomUnderSampler: {
                        "params": {
                            "sampling_strategy": 0.5,
                            "random_state": 42,
                        },
                    }
                },
                {
                    SMOTE: {
                        "params": {
                            "random_state": 42,
                        },
                    }
                }
            ],
        },
        "output_dir": "output/",
    },
    "hyper_params": {
        "data_loader_params": {
            "batch_size": 128,
            "shuffle": True,
        },
        "loss": nn.BCELoss(),
        "optim": torch.optim.Adam,
        "optim_params": {
            "lr": 0.0001,
        },
        "metrics": torchmetrics.MetricCollection({
            'accuracy': BinaryAccuracy(),
            'precision': BinaryPrecision(),
            'recall': BinaryRecall(),
            'f1score': BinaryF1Score(),
            'auroc': BinaryAUROC(),
        }),
        "device": "cuda"
        if torch.cuda.is_available()
        else "cpu",
        "epochs": 10,
        'cv_params':{
            'n_split': 5,
        },
    },
}
