from io import BytesIO
from fpdf import FPDF
import tempfile
import os
import streamlit as st


def add_logo_header(pdf, logo_path, x=10, y=10, w=30):
    """
    Add a logo to the top header of the current page.
    """
    if not os.path.exists(logo_path):
        st.error(f"Logo file not found at: {logo_path}")
        return

    # Add the logo at the top of the page
    pdf.image(logo_path, x=x, y=y, w=w)


def export_graphs(generated_figures):
    if not generated_figures:
        st.error("No graphs to export.")
        return

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    logo_path = os.path.join(os.path.dirname(__file__), "LOGO.jpg")  # Absolute path to the logo

    # Track figures to place two per page
    figures_per_page = 2
    figure_count = 0

    for fig in generated_figures:
        if fig is None:
            continue  # Skip invalid figures

        # Export figure to a PNG using a temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            try:
                fig.write_image(tmp_file.name, format="png")  # Save image to temp file
                tmp_file.close()  # Ensure the file is written before using it

                # Add a new page if needed
                if figure_count % figures_per_page == 0:
                    pdf.add_page()
                    # Add the logo in the header
                    add_logo_header(pdf, logo_path)

                # Position the graphs: Top half for odd, Bottom half for even
                if figure_count % figures_per_page == 0:
                    pdf.image(tmp_file.name, x=10, y=30, w=180)  # Top half
                else:
                    pdf.image(tmp_file.name, x=10, y=150, w=180)  # Bottom half

                figure_count += 1
            except Exception as e:
                st.error(f"Error exporting figure: {e}")
                continue
            finally:
                # Clean up temporary file after usage
                os.unlink(tmp_file.name)

    # Save the PDF to a temporary BytesIO object
    pdf_output = BytesIO()
    pdf.output(dest="S").encode("latin1")  # Save the content to a string
    pdf_output.write(pdf.output(dest="S").encode("latin1"))
    pdf_output.seek(0)  # Reset the pointer to the start of the stream

    # Provide a download button for the PDF
    st.download_button(
        label="Download PDF with Graphs",
        data=pdf_output,
        file_name="exported_graphs.pdf",
        mime="application/pdf",
    )




# from io import BytesIO
# from fpdf import FPDF
# import tempfile
# import os
# import streamlit as st


# def export_graphs(generated_figures):
#     if not generated_figures:
#         st.error("No graphs to export.")
#         return

#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     # Track figures to place two per page
#     figures_per_page = 2
#     figure_count = 0

#     for fig in generated_figures:
#         if fig is None:
#             continue  # Skip invalid figures

#         # Export figure to a PNG using a temporary file
#         with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
#             try:
#                 fig.write_image(tmp_file.name, format="png")  # Save image to temp file
#                 tmp_file.close()  # Ensure the file is written before using it
                
#                 # Add a new page if needed
#                 if figure_count % figures_per_page == 0:
#                     pdf.add_page()
                
#                 # Position the graphs: Top half for odd, Bottom half for even
#                 if figure_count % figures_per_page == 0:
#                     pdf.image(tmp_file.name, x=10, y=20, w=180)  # Top half
#                 else:
#                     pdf.image(tmp_file.name, x=10, y=150, w=180)  # Bottom half

#                 figure_count += 1
#             except Exception as e:
#                 st.error(f"Error exporting figure: {e}")
#                 continue
#             finally:
#                 # Clean up temporary file after usage
#                 os.unlink(tmp_file.name)

#     # Save the PDF to a temporary BytesIO object
#     pdf_output = BytesIO()
#     pdf.output(dest="S").encode("latin1")  # Save the content to a string
#     pdf_output.write(pdf.output(dest="S").encode("latin1"))
#     pdf_output.seek(0)  # Reset the pointer to the start of the stream

#     # Provide a download button for the PDF
#     st.download_button(
#         label="Download PDF with Graphs",
#         data=pdf_output,
#         file_name="exported_graphs.pdf",
#         mime="application/pdf",
#     )



# from io import BytesIO
# from fpdf import FPDF
# import tempfile
# import os
# import streamlit as st


# def export_graphs(generated_figures):
#     if not generated_figures:
#         st.error("No graphs to export.")
#         return

#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     for fig in generated_figures:
#         if fig is None:
#             continue  # Skip invalid figures

#         # Export figure to a PNG using a temporary file
#         with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
#             try:
#                 fig.write_image(tmp_file.name, format="png")  # Save image to temp file
#                 tmp_file.close()  # Ensure the file is written before using it
#                 pdf.add_page()
#                 pdf.image(tmp_file.name, x=10, y=20, w=180)  # Add image to PDF
#             except Exception as e:
#                 st.error(f"Error exporting figure: {e}")
#                 continue
#             finally:
#                 # Clean up temporary file after usage
#                 os.unlink(tmp_file.name)

#     # Save the PDF to a temporary BytesIO object
#     pdf_output = BytesIO()
#     pdf.output(dest="S").encode("latin1")  # Save the content to a string
#     pdf_output.write(pdf.output(dest="S").encode("latin1"))
#     pdf_output.seek(0)  # Reset the pointer to the start of the stream

#     # Provide a download button for the PDF
#     st.download_button(
#         label="Download PDF with Graphs",
#         data=pdf_output,
#         file_name="exported_graphs.pdf",
#         mime="application/pdf",
#     )




# import streamlit as st
# from fpdf import FPDF
# from io import BytesIO
# import tempfile
# import os

# def export_graphs(figures):
#     st.subheader("Export Generated Graphs")

#     if not figures:
#         st.info("No charts to export. Please generate some in the Visualization tab.")
#         return

#     # Create a PDF object
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     with tempfile.TemporaryDirectory() as temp_dir:
#         for i, fig in enumerate(figures):
#             # Create a BytesIO buffer for the figure
#             img_buffer = BytesIO()
#             fig.write_image(img_buffer, format="png")
#             img_buffer.seek(0)

#             # Save the buffer to a temporary PNG file
#             temp_file_path = os.path.join(temp_dir, f"chart_{i}.png")
#             with open(temp_file_path, "wb") as temp_file:
#                 temp_file.write(img_buffer.read())

#             # Add the image to the PDF
#             pdf.add_page()
#             pdf.image(temp_file_path, x=10, y=20, w=180)  # Adjust dimensions if needed

#     # Generate the PDF as a BytesIO object
#     pdf_output = BytesIO()
#     pdf.output(dest="S").encode("latin1")  # Output PDF to BytesIO buffer
#     pdf_output.write(pdf.output(dest="S").encode("latin1"))
#     pdf_output.seek(0)

#     # Provide a Streamlit download button for the generated PDF
#     st.download_button(
#         label="Download PDF with Charts",
#         data=pdf_output.getvalue(),
#         file_name="charts.pdf",
#         mime="application/pdf",
#     )
