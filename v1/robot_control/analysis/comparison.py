from packaging import version
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats
import tensorboard as tb

# Code available here: https://www.tensorflow.org/tensorboard/dataframe_api

major_ver, minor_ver, _ = version.parse(tb.__version__).release
assert major_ver >= 2 and minor_ver >= 3, \
    "This notebook requires TensorBoard 2.3 or later."
print("TensorBoard version: ", tb.__version__)

experiment_id_resnet_50 = "BVG6hRmMTWuqGYVlJOOjHw"
experiment_id_resnet_34 = "ZTKMAiMzR3WfOndfLkC4YQ"
experiment_R50 = tb.data.experimental.ExperimentFromDev(experiment_id_resnet_50)
experiment_R34 = tb.data.experimental.ExperimentFromDev(experiment_id_resnet_34)

df_R50 = experiment_R50.get_scalars()
df_R34 = experiment_R34.get_scalars()
# print(df)


# print(df["run"].unique())
# print(df["tag"].unique())

dfw_R50 = experiment_R50.get_scalars(pivot=True) 
dfw_R34 = experiment_R34.get_scalars(pivot=True) 
# print(dfw)

# csv_path = '/tmp/tb_experiment_1.csv'
# dfw.to_csv(csv_path, index=False)
# dfw_roundtrip = pd.read_csv(csv_path)
# pd.testing.assert_frame_equal(dfw_roundtrip, dfw)

# Filter the DataFrame to only validation data, which is what the subsequent
# analyses and visualization will be focused on.

# dfw_validation = dfw[dfw.run.str.endswith("/validation")]


# Get the optimizer value for each row of the validation DataFrame.

# optimizer_validation = dfw_validation.run.apply(lambda run: run.split(",")[0])



TSBOARD_SMOOTHING = 0.85



# https://stackoverflow.com/questions/60683901/tensorboard-smoothing
plt.figure(figsize=(16, 6))
plt.subplot(1, 2, 1)
sns.lineplot(data=dfw_R50, x="step", y="val_iou_score", alpha=0.3, 
             ).set_title("val_iou_score")
sns.lineplot(data=dfw_R50.ewm(alpha=(1 - TSBOARD_SMOOTHING)).mean(), x="step", y="val_iou_score", 
             ).set_title("val_iou_score")
sns.lineplot(data=dfw_R34, x="step", y="val_iou_score", alpha=0.3, 
             ).set_title("val_iou_score")
sns.lineplot(data=dfw_R34.ewm(alpha=(1 - TSBOARD_SMOOTHING)).mean(), x="step", y="val_iou_score", 
             ).set_title("val_iou_score")

plt.subplot(1, 2, 2)
sns.lineplot(data=dfw_R50, x="step", y="val_loss",
             ).set_title("val_loss")
sns.lineplot(data=dfw_R34, x="step", y="val_loss",
             ).set_title("val_loss")
ax = plt.gca()
# ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 5])
plt.show()