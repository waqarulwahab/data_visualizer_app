
---

# **GraphX: A New Lens on Your Data**

GraphX is a powerful data visualization tool designed to help users analyze and explore datasets with ease. It provides an intuitive interface for importing, viewing, and visualizing data from various formats such as CSV and Excel. The app allows users to upload their datasets, analyze them with the MitoSheet functionality, and visualize key insights with a variety of built-in features.

## **Features**

- **Data Upload**: Allows users to upload CSV and Excel files for analysis.
- **Data Analysis**: Powered by MitoSheet, the app enables users to perform interactive data analysis directly within the interface.
- **Easy Visualizations**: Quickly visualize your data to identify trends, patterns, and outliers.
- **User-Friendly Interface**: Designed with simplicity in mind, the interface is straightforward and easy to navigate.
- **Customizable Sidebar**: Upload files, add logos, and modify the appearance of the sidebar to suit your needs.

## **How to Run Locally**

To run this project locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/waqarulwahab/data_visualizer_app.git
cd GraphX
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```

### 3. Install Required Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App

After installing the dependencies, run the Streamlit app with:

```bash
streamlit run app.py
```

The app will open in your default web browser.

## **Project Structure**

```
GraphX/
├── app.py               # Main Streamlit app
├── data/                # Directory for storing uploaded data files
├── LOGO.jpg             # Logo image for the sidebar
├── requirements.txt     # List of required Python packages
├── README.md            # Project overview
└── .gitignore           # Git ignore file
```

## **Libraries Used**

- **Streamlit**: A fast and easy way to build interactive data applications.
- **MitoSheet**: A spreadsheet interface for interactive data analysis.
- **Pandas**: A powerful data manipulation library.
- **Matplotlib / Seaborn**: For visualizations (if used within the app).

## **How It Works**

1. **Data Upload**: 
   Users can upload their CSV or Excel file through the sidebar. The file is saved to the `data/` folder, making it accessible for analysis.

2. **Data Analysis with MitoSheet**:
   The uploaded file is analyzed using MitoSheet, an interactive spreadsheet tool embedded in the app. Users can modify, visualize, and manipulate the dataset directly in the app.

3. **Visualization**:
   The app allows for the display of data and analysis code, helping users to explore the dataset in a more engaging and intuitive way.

4. **Custom CSS**:
   The app includes custom CSS to style the interface, including hiding the Pro upgrade section of MitoSheet.

## **Contributing**

We welcome contributions! If you find a bug, or want to propose a feature or improvement, feel free to open an issue or submit a pull request.

### Steps to Contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Commit and push your changes to your fork.
5. Open a pull request.

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
