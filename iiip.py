import streamlit as st
import img2pdf
from tempfile import NamedTemporaryFile

def generate_ordered_pdf(image_order):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf_bytes = img2pdf.convert(image_order)
        tmp.write(pdf_bytes)
        return tmp.name

def main():
    st.title("Image to PDF Converter with Custom Page Order")
    
    uploaded_files = st.file_uploader("Upload .jpg images", type="jpg", accept_multiple_files=True)

    if uploaded_files:
        st.subheader("Specify the page order for each image:")
        
        image_order = []
        for i, uploaded_file in enumerate(uploaded_files):
            with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(uploaded_file.read())
                tmp.seek(0)
                image_path = tmp.name
                st.image(image_path, caption=f"Image {i + 1}")
                page_number = st.number_input(f"Page number for Image {i + 1}", min_value=1, value=i + 1)
                image_order.append((page_number, image_path))
        
        # Sort images based on the specified order
        image_order.sort()

        if st.button("Convert to PDF"):
            ordered_images = [img for _, img in image_order]
            pdf_path = generate_ordered_pdf(ordered_images)
            
            st.success("PDF generated successfully!")
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="output.pdf")

if __name__ == "__main__":
    main()
