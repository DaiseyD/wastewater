


import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import statsmodels.formula.api as smf

def process_summary_files(root_dir, summaryFileName="summaryInfo.json", inputParamFileName="inputParams.json"):


    print(f"Starting search for '{summaryFileName}' in subdirectories of: {root_dir}\n")
    
    alldata = []
    for root, dirs, files in os.walk(root_dir):
        # We only want to process the file if it's found in the current folder ('root')
        if summaryFileName in files:
            # Construct the full path to the file
            file_path = os.path.join(root, summaryFileName)


            try:
                # Open the file for reading ('r')
                with open(file_path, 'r') as summaryFile:
                    # Attempt to load the JSON content
                    summary = json.load(summaryFile)
                    alldata.append([summary['total Simulations'], summary['total fields changed'], summary['Scenariosetup']] )           

            except Exception as e:
                pass
                # print(f"An unexpected error occurred while processing {file_path}: {e}")
    column_names = ['nSims', 'fieldsChanged', 'setupTime']
    df = pd.DataFrame(columns=column_names, data=alldata)
    return df


basepath = "C:\\Users\\dijks\\Documents\\wastewatersimulation\\wastewater\\results"
df  = process_summary_files(basepath)
df= df.sort_values(by="fieldsChanged")
print(df)
df.plot(x="fieldsChanged", y="setupTime")
plt.show()
df= df.sort_values(by="nSims")
df.plot(x="nSims", y="setupTime")

# 2. Perform Multiple Linear Regression
# The formula specifies: Z is dependent on X and Y
model = smf.ols(formula='setupTime ~ nSims + fieldsChanged ', data=df)
results = model.fit()

# Print the model summary (optional, but good for checking fit)
print("--- Regression Results Summary ---")
print(results.summary().as_text())
print("----------------------------------")

# --- Visualization Setup ---

# 3. Create a meshgrid for the fitted plane
# Create a grid of points over the range of X and Y data
x_range = np.linspace(df['nSims'].min(), df['nSims'].max(), 20)
y_range = np.linspace(df['fieldsChanged'].min(), df['fieldsChanged'].max(), 20)
X_surf, Y_surf = np.meshgrid(x_range, y_range)

# 4. Predict Z values on the meshgrid using the fitted model
# The prediction needs a DataFrame with column names matching the formula
df_surf = pd.DataFrame({'nSims': X_surf.ravel(), 'fieldsChanged': Y_surf.ravel()})
Z_surf = results.predict(df_surf).values.reshape(X_surf.shape)

# --- 3D Plotting ---

# 5. Create the 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot of the original data points
ax.scatter(df['nSims'], df['fieldsChanged'], df['setupTime'], c='blue', marker='o', label='Original Data (Z)')

# Plot the fitted regression plane
ax.plot_surface(X_surf, Y_surf, Z_surf, alpha=0.5, color='red', label='Fitted Plane')

# Set labels and title
ax.set_xlabel('Independent Variable nSims')
ax.set_ylabel('Independent Variable fieldsChanged')
ax.set_zlabel('Dependent Variable setupTime')
ax.set_title('Least Squares Plane Fitting (setupTime ~ nSims + fieldsChanged)')

# Add a legend for clarity (though plot_surface handles it differently)
# Custom legend handling for the surface plot
from matplotlib.patches import Patch
custom_legend = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Original Data'),
    Patch(facecolor='red', alpha=0.5, label='Fitted Plane')
]
ax.legend(handles=custom_legend)

plt.show()