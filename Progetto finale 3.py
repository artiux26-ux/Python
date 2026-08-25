import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.model_selection import (
    train_test_split,
    KFold,
    cross_val_score,
    GridSearchCV,
    learning_curve
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import PCA


# Caricamento dataset Diabetes
diabetes = load_diabetes(as_frame=True)
df = diabetes.frame.copy()

print("========== DATASET ==========")
print(df.head())

print("\nDimensioni dataset:")
print(df.shape)

print("\n========== ANALISI DESCRITTIVA ==========")
print(df.describe())

print("\n========== VALORI MANCANTI ==========")
print(df.isnull().sum())


# ----------------------------
# Istogrammi
# ----------------------------

df.hist(
    figsize=(14, 10),
    bins=20
)

plt.suptitle("Istogrammi - Dataset Diabetes")
plt.tight_layout()
plt.show()

df.plot(
    kind="box",
    figsize=(14, 6),
    rot=45
)

plt.title("Boxplot - Dataset Diabetes")
plt.tight_layout()
plt.show()


pd.plotting.scatter_matrix(
    df,
    figsize=(14, 14),
    diagonal="hist",
    alpha=0.6
)

plt.suptitle(
    "Scatter Matrix - Dataset Diabetes",
    y=1.02
)

plt.show()

X = df.drop(columns="target")
y = df["target"]



X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\n========== TRAIN / TEST ==========")
print("Training set:", X_train.shape)
print("Test set:", X_test.shape)


models = {

    "Regressione Lineare":
        Pipeline([
            ("model", LinearRegression())
        ]),

    "Decision Tree":
        Pipeline([
            ("model", DecisionTreeRegressor(
                random_state=42
            ))
        ]),

    "Ridge":
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", Ridge())
        ]),

    "Lasso":
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", Lasso(
                max_iter=10000
            ))
        ]),

    "K-Nearest Neighbor":
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", KNeighborsRegressor())
        ]),

    "Support Vector Machine":
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", SVR())
        ])
}


kf = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

cv_results = []

for name, model in models.items():

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=kf,
        scoring="neg_mean_squared_error"
    )

    cv_results.append({
        "Modello": name,
        "NMSE medio": scores.mean(),
        "Deviazione standard NMSE": scores.std(),
        "MSE medio": -scores.mean()
    })


cv_df = pd.DataFrame(cv_results)

cv_df = cv_df.sort_values(
    by="NMSE medio",
    ascending=False
)

print("\n========== CONFRONTO CROSS-VALIDATION ==========")
print(cv_df.to_string(index=False))


param_grids = {

    "Regressione Lineare": {},

    "Decision Tree": {
        "model__max_depth":
            [2, 3, 4, 5, 6, 8, 10, None]
    },

    "Ridge": {
        "model__alpha":
            [0.001, 0.01, 0.1, 1, 10, 100]
    },

    "Lasso": {
        "model__alpha":
            [0.0001, 0.001, 0.01, 0.1, 1, 10]
    },

    "K-Nearest Neighbor": {
        "model__n_neighbors":
            [3, 5, 7, 9, 11, 15, 20]
    },

    "Support Vector Machine": {
        "model__C":
            [0.1, 1, 10, 100],

        "model__epsilon":
            [0.01, 0.1, 0.2]
    }
}



grid_results = []

for name, model in models.items():

    grid = GridSearchCV(
        estimator=model,
        param_grid=param_grids[name],
        scoring="neg_mean_squared_error",
        cv=kf,
        n_jobs=-1
    )

    grid.fit(
        X_train,
        y_train
    )

    grid_results.append({
        "Modello": name,
        "Migliori parametri": grid.best_params_,
        "Miglior NMSE": grid.best_score_,
        "Best Estimator": grid.best_estimator_
    })


grid_df = pd.DataFrame(grid_results)

print("\n========== GRID SEARCH ==========")

print(
    grid_df[
        [
            "Modello",
            "Migliori parametri",
            "Miglior NMSE"
        ]
    ].to_string(index=False)
)



best_idx = grid_df[
    "Miglior NMSE"
].idxmax()

best_model_name = grid_df.loc[
    best_idx,
    "Modello"
]

best_model = grid_df.loc[
    best_idx,
    "Best Estimator"
]

best_params = grid_df.loc[
    best_idx,
    "Migliori parametri"
]

print("\n========== MODELLO OTTIMIZZATO ==========")
print("Modello:", best_model_name)
print("Parametri:", best_params)


best_model.fit(
    X_train,
    y_train
)

y_pred = best_model.predict(
    X_test
)

test_mse = mean_squared_error(
    y_test,
    y_pred
)

test_r2 = r2_score(
    y_test,
    y_pred
)

print("\n========== VALUTAZIONE FINALE ==========")
print("MSE:", test_mse)
print("R2:", test_r2)


train_sizes, train_scores, validation_scores = learning_curve(

    best_model,

    X_train,

    y_train,

    cv=kf,

    scoring="neg_mean_squared_error",

    train_sizes=np.linspace(
        0.1,
        1.0,
        10
    ),

    n_jobs=-1
)


train_mse = -train_scores.mean(
    axis=1
)

validation_mse = -validation_scores.mean(
    axis=1
)


plt.figure(
    figsize=(9, 6)
)

plt.plot(
    train_sizes,
    train_mse,
    marker="o",
    label="Training MSE"
)

plt.plot(
    train_sizes,
    validation_mse,
    marker="o",
    label="Validation MSE"
)

plt.xlabel(
    "Numero di campioni di training"
)

plt.ylabel(
    "MSE"
)

plt.title(
    f"Learning Curve - {best_model_name}"
)

plt.legend()

plt.grid(True)

plt.show()



print("\n========== ANALISI BIAS / VARIANZA ==========")

final_train_mse = train_mse[-1]
final_validation_mse = validation_mse[-1]

gap = final_validation_mse - final_train_mse

if (
    final_train_mse > 0.9 * final_validation_mse
):
    print(
        "Il modello mostra una tendenza all'UNDERFITTING."
    )

elif (
    gap > 0.25 * final_validation_mse
):
    print(
        "Il modello mostra una tendenza all'OVERFITTING."
    )

else:
    print(
        "Il modello mostra un compromesso "
        "bias-varianza ragionevole."
    )



# Standardizzazione
scaler_pca = StandardScaler()

X_train_scaled = scaler_pca.fit_transform(
    X_train
)

X_test_scaled = scaler_pca.transform(
    X_test
)



pca = PCA(
    n_components=2
)

X_train_pca = pca.fit_transform(
    X_train_scaled
)

X_test_pca = pca.transform(
    X_test_scaled
)


print("\n========== PCA ==========")

print(
    "Varianza spiegata PC1:",
    pca.explained_variance_ratio_[0]
)

print(
    "Varianza spiegata PC2:",
    pca.explained_variance_ratio_[1]
)

print(
    "Varianza spiegata totale:",
    pca.explained_variance_ratio_.sum()
)


plt.figure(
    figsize=(9, 7)
)

scatter = plt.scatter(

    X_train_pca[:, 0],

    X_train_pca[:, 1],

    c=y_train,

    alpha=0.75
)

plt.xlabel("PC1")

plt.ylabel("PC2")

plt.title(
    "PCA - Dataset Diabetes"
)

plt.colorbar(
    scatter,
    label="Target"
)

plt.grid(True)

plt.show()


# Modello ottimizzato applicato alle due componenti PCA
pca_model = Pipeline([
    ("model", best_model)
])

pca_model.fit(
    X_train_pca,
    y_train
)


pc1_min = X_train_pca[:, 0].min()
pc1_max = X_train_pca[:, 0].max()

pc2_min = X_train_pca[:, 1].min()
pc2_max = X_train_pca[:, 1].max()


pc1_grid, pc2_grid = np.meshgrid(

    np.linspace(
        pc1_min,
        pc1_max,
        40
    ),

    np.linspace(
        pc2_min,
        pc2_max,
        40
    )
)


grid_points = np.c_[

    pc1_grid.ravel(),

    pc2_grid.ravel()
]


z_grid = pca_model.predict(
    grid_points
).reshape(
    pc1_grid.shape
)


fig = plt.figure(
    figsize=(10, 7)
)

ax = fig.add_subplot(
    111,
    projection="3d"
)


ax.scatter(

    X_train_pca[:, 0],

    X_train_pca[:, 1],

    y_train,

    alpha=0.7,

    label="Dati"
)


ax.plot_surface(

    pc1_grid,

    pc2_grid,

    z_grid,

    alpha=0.35
)


ax.set_xlabel(
    "PC1"
)

ax.set_ylabel(
    "PC2"
)

ax.set_zlabel(
    "Target"
)

ax.set_title(
    f"Piano di regressione - {best_model_name}"
)

plt.show()


print("\n========== RIEPILOGO FINALE ==========")

print(
    "Modello ottimizzato:",
    best_model_name
)

print(
    "Parametri ottimali:",
    best_params
)

print(
    "MSE Test:",
    test_mse
)

print(
    "R2 Test:",
    test_r2
)