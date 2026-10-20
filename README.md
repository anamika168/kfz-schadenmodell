# Kfz-Schadenmodell: GLM vs gradient boosting

An independent project on public data: the expected claim cost per contract and year (pure premium) for a
French motor third-party liability portfolio, as the basis of a fair premium. A Poisson × Gamma GLM and a
Poisson × Gamma gradient boosting model (GBM) are compared on identical cross-validation folds, with
exposure-weighted Tweedie deviance, Gini and calibration by customer group.

## Result in brief

| | GLM (final model) | GBM (benchmark) |
|---|---|---|
| Deviance, 5-fold CV on the training part (lower is better) | 73.899 | **72.868** |
| D² (deviance explained), CV | 5.08 % | **6.40 %** |
| Gini, CV | 0.315 | **0.343** |
| Drivers aged 18–20: actual / predicted cost, CV (502 claims) | **0.998** | 1.284 |
| D² on the held-out test part | 4.78 % | **5.56 %** |

* **Data check:** 9,116 contracts declare claims that have no claim amount, almost all in one block of policy
  IDs (`IDpol` ≤ 25,000). With the declared count, brand-new vehicles would look 4.4 times as risky as they
  are. The claim count used is the number of claims with an amount.
* **Accuracy vs calibration:** the GBM has the lower deviance in all five folds, but it is worse calibrated in
  sparse groups: the youngest drivers cost 1.28 times their GBM premium. The GLM prices every age, Bonus-Malus
  and vehicle-age band and every area within ±2.5 % of its cost, except vehicle age 20+ (1.059).
* **Decision:** the transparent GLM is the final model; the GBM stays as the benchmark. On the test part the
  GBM is again slightly more accurate (bootstrap 95 % interval of the deviance difference 0.045 to 1.154).
* **Output:** tariff factors, permutation importance, a fairness check on the test part and a risk premium per
  contract (median 138.48 per year).

## Data

`freMTPL2freq` (678,013 policies) and `freMTPL2sev` (26,639 claims) from the R package
[CASdatasets](https://github.com/dutangc/CASdatasets) (A. Charpentier, C. Dutang), release of January 2017.
OpenML hosts the same release (data IDs 41214 and 41215). Releases from 2022 onwards removed the
inconsistencies that notebook 01 finds, so `get_data.py` pins the 2017 release to one commit. The data is
not stored in this repository; `get_data.py` downloads it into `data/`.

## Notebooks

| notebook | content |
|---|---|
| `01_eda.ipynb` | data problems (claims without a policy, the ID block, exposure above one year, large claims), one-way risk factors, correlations |
| `02_feature_engineering.ipynb` | one row per contract, claims capped at 100,000, frequency and severity targets, bands for the GLM, 80/20 split |
| `03_model_comparison.ipynb` | constant vs GLM vs GBM, 5-fold cross-validation, deviance, D², Gini, calibration by group, decision |
| `04_model_building.ipynb` | final GLM, large-claim loading, test part, bootstrap, fairness, permutation importance, tariff factors, risk premium, improvement ideas, limitations |

Headings and short introductions are in German, code and findings in English. Every finding states only what the cells above it print.

## Reproduce

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python get_data.py
cd notebooks
for nb in 01_eda 02_feature_engineering 03_model_comparison 04_model_building; do
  ../.venv/bin/jupyter nbconvert --to notebook --execute --inplace "$nb.ipynb"
done
```

Run the notebooks in this order; together they take about two minutes. Notebooks 03 and 04 read
`data/model_data.parquet`, which notebook 02 writes.

## Limitations

* One year of data: training and test part are random samples of the same year, so performance on a later
  year is not tested.
* The large-claim loading (1.2573) rests on 36 claims above 100,000 in the training part.
* The cheapest tenth of the customers is priced too low by both models.
* The GBM settings are fixed and not tuned.

## License

Code: MIT, see `LICENSE`. The data is not redistributed here.
